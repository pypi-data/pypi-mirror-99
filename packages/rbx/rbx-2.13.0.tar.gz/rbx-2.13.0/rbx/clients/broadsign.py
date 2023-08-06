import logging
from urllib.parse import quote, parse_qs, urlparse

import arrow

from ..utils import smart_url
from . import Client, HttpAuth
from ..exceptions import ClientError, Unauthorized

logger = logging.getLogger(__name__)


class BroadsignClient(Client):
    """Client for Broadsign Reach APIs.

    The API documentation can be found on Google Drive:
    https://drive.google.com/file/d/16qS-xkOl5fcJaB26bf7STKn4qxkaZ6Mx/view

    """
    AUTH_ENDPOINT = 'https://auth.broadsign.com'
    AUTH_PATH = '/oauth/token'
    CLIENT_ID = 'dIJ179dH1A2Wn9j9ia4rYGICNmuJMMYb'
    ENDPOINT = 'https://servssp.broadsign.com/'
    IF_MODIFIED_SINCE_FORMAT = 'ddd, DD MMM YYYY HH:mm:ss [GMT]'
    TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'
    EXPIRY_TIME = 'expires_in'

    def __init__(self, dsp_id, dsp_name):
        super().__init__()
        self.csrftoken = None
        self.dsp_id = dsp_id
        self.dsp_name = dsp_name
        self.token_expiry = None
        self.refresh_token = None

    @property
    def auth(self):
        """Broadsign uses Digest Authentication."""
        return HttpAuth(f'Bearer {self.token}', key='Authorization')

    def login(self, username, password):
        """Authenticate and set the access token and refresh token on success.

        If the Client is already authenticated, the login process will be skipped.
        """
        if self.is_authenticated:
            return

        response = self._request(
            'post',
            self.AUTH_PATH,
            endpoint=self.AUTH_ENDPOINT,
            data={
                'username': username,
                'password': password,
                'grant_type': 'http://auth0.com/oauth/grant-type/password-realm',
                'client_id': self.CLIENT_ID,
                'realm': 'Username-Password-Authentication',
                'audience': 'https://platform.broadsign.com/',
                'scope': 'offline_access'
            }
        )

        self.credentials = {
            'username': username,
            'password': password,
        }
        self.token = response.get(self.TOKEN)
        self.refresh_token = response.get(self.REFRESH_TOKEN)
        self.token_expiry = arrow.get().shift(seconds=response.get(self.EXPIRY_TIME))
        logger.debug(f'Logged in <Token: {self.token}> <Refresh Token: {self.refresh_token}>')

    def get_message(self, response):
        return response.text

    def request(self, method, path, content_type='application/json', data=None,
                endpoint=None, headers=None):
        """Attempt to refresh if the token has expired.

        Note that the Client must be logged in first for this to work.
        """
        assert self.is_authenticated, 'You must login first'

        if self.token_expiry <= arrow.now():
            logger.debug('Token expired... refreshing')
            self.refresh_access_token()

        try:
            return self._request(method=method, path=path, content_type=content_type, data=data,
                                 endpoint=endpoint, headers=headers)
        except Unauthorized:
            logger.debug('Received Unauthorised... refreshing')
            try:
                self.refresh_access_token()
            except ClientError:
                logger.debug('Unable to refresh... re-authenticating')
                self.login(**self.credentials)

            return self._request(method=method, path=path, content_type=content_type, data=data,
                                 endpoint=endpoint, headers=headers)

    def refresh_access_token(self):
        """Retrieve access token and refresh token from Broadsign with previous refresh token."""
        response = self._request(
            'post',
            self.AUTH_PATH,
            endpoint=self.AUTH_ENDPOINT,
            data={
                'grant_type': 'refresh_token',
                'client_id': self.CLIENT_ID,
                'refresh_token': self.refresh_token
            }
        )

        self.token = response.get(self.TOKEN)
        self.refresh_token = response.get(self.REFRESH_TOKEN)
        self.token_expiry = arrow.get().shift(seconds=response.get(self.EXPIRY_TIME))
        logger.debug(f'Refreshed <Token: {self.token}> <Refresh Token: {self.refresh_token}>')

    def create_advertiser(self, name):
        """Create an Advertiser object."""
        response = self.request('post', '/api/advertisers/', data={
            'name': name,
            'dsp': {
                'id': self.dsp_id,
                'name': self.dsp_name
            },
        })
        return {
            'id': response['id'],
            'name': response['name'],
        }

    def create_creative(self, advertiser, creative_id, category, creative_type, creative_url, name,
                        publishers):
        """Create a Creative object.

        Note that the 'original_url' requires the protocol, or the API request will fail.
        """
        response = self.request('post', '/api/entity_creatives/', data={
            'advertiser': advertiser,
            'external_id': str(creative_id),
            'iab_categories': [category],
            'name': name,
            'original_url': smart_url(creative_url, force_https=True),
            'publishers': publishers,
            'type': 'VideoCreative' if creative_type == 'video' else 'ImageUrlCreative',
        })

        return {
            'id': int(response['external_id']),
            'name': response['name'],
            'status': response['status'],
            'type': response['type'],
        }

    def get_advertiser(self, name):
        """Retrieve an Advertiser object by name."""
        path = '/api/advertisers/?name={}'.format(quote(name))
        response = self.request('get', path)
        if response.get('count', 0) > 0:
            return {
                'id': response['results'][0]['id'],
                'name': response['results'][0]['name'],
            }

    def get_category(self, code):
        """Retrieve a Category object by code."""
        path = '/api/categories/?code={}'.format(code)
        response = self.request('get', path)
        if response.get('count', 0) > 0:
            return {
                'id': response['results'][0]['id'],
                'name': response['results'][0]['name'],
            }

    def get_creative(self, creative_id, as_entity=False):
        """Retrieve a Creative object by ID.

        Passing the as_entity flag as True will return the object as returned by the system.
        """
        path = '/api/entity_creatives/?external_id={}'.format(creative_id)
        response = self.request('get', path)
        if response.get('count', 0) > 0:
            entity = response['results'][0]
            if as_entity:
                return entity

            return {
                'id': int(entity['external_id']),
                'name': entity['name'],
                'status': entity['status'],
                'type': entity['type'],
            }

    def get_publishers(self, ad_type=None, page=None):
        """Retrieve a list of Publisher objects.

        The list may be further refined by ad_type, one of 'html', 'static', or 'video'.
        The API does not allow filtering by query string, so we have to resort to filtering the
        final results ourselves.

        Note that when a publisher has no ad types defined (i.e.: 'allowed_ad_types': []), we
        include the publisher. According to Broadsign, this happens when the details on the
        publisher haven't made it to the API yet, so we should add them.
        """
        if ad_type:
            assert ad_type in ('html', 'static', 'video'), f'Invalid Ad Type: "{ad_type}"'

        path = '/api/publishers/'
        params = {'page_size': 100}
        if page:
            params['page'] = page

        publishers = []
        response = self.request('get', path, data=params)
        if response.get('count', 0) > 0:
            publishers.extend(response['results'])

        if response.get('next'):
            try:
                page = int(parse_qs(urlparse(response.get('next')).query)['page'][0])
            except (KeyError, ValueError):
                pass
            else:
                publishers.extend(self.get_publishers(page=page))

        if ad_type:
            publishers[:] = [
                publisher for publisher in publishers
                if not publisher['allowed_ad_types'] or ad_type in [
                    allowed_ad_type['name'].lower()
                    for allowed_ad_type in publisher['allowed_ad_types']
                ]
            ]

        publishers.sort(key=lambda x: x['name'])

        return publishers

    def get_screens(self, last_modified=None, page=None):
        """Retrieve all screens from Broadsign.

        The list may be further refined using the last_modified date, which will cause the API to
        return only those screens that were modified after the specified date.
        """
        path = '/api/screens/'
        params = {'page_size': 100}
        if page:
            params['page'] = page

        headers = None

        if last_modified:
            utc = arrow.get(last_modified).to('utc')
            headers = {'If-Modified-Since': utc.format(self.IF_MODIFIED_SINCE_FORMAT)}

        screens = []
        response = self.request('get', path, data=params, headers=headers)
        if response.get('count', 0) > 0:
            screens.extend(response['results'])

        if response.get('next'):
            try:
                page = int(parse_qs(urlparse(response.get('next')).query)['page'][0])
            except (KeyError, ValueError):
                pass
            else:
                screens.extend(self.get_screens(last_modified=last_modified, page=page))

        return screens

    def update_creative(self, entity_id, payload):
        """Update a Creative object.

        Note that updating requires the entity_id, which is the ID of the Creative in the supplier
        system.
        """
        self.request('put', f'/api/entity_creatives/{entity_id}/', data=payload)
