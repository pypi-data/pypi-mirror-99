"""Common RBX exceptions."""


class FatalException(Exception):
    """Raise this exception for non-transient errors.

    These exceptions can be given an extra details object, which may be used by the caller to log
    this as extra information.
    """
    message = 'Something went wrong!'

    def __init__(self, message=None, details=None):
        super().__init__(message or self.message)
        self.details = details

    def to_dict(self):
        rv = {
            'message': str(self)
        }

        if self.details:
            rv['details'] = self.details

        return rv


class HTTPException(FatalException):
    """A FatalException with ani optional HTTP status code and a URL."""
    STATUS_CODE = 500

    def __init__(self, message, status_code=None, url=None, **kwargs):
        super().__init__(message, **kwargs)
        self.status_code = status_code or self.STATUS_CODE
        self.url = url

    def to_dict(self):
        rv = super().to_dict()
        rv['status_code'] = self.status_code
        if self.url:
            rv['url'] = self.url

        return rv


class AWSException(Exception):
    """Raised when an unexpected error occurs using boto3."""


class BadRequest(HTTPException):
    """Convenience Exception to use from within a Flask service/blueprint.

    Raising this exception will be caught by the error handler and formatted as an HTTP response,
    using the provided status_code.
    """
    STATUS_CODE = 400


class ClientException(HTTPException):
    """Raised from within the rbx.clients package, caused by third-party APIs.

    This exception is fatal and considered non-transient.
    """


class ClientError(ClientException):
    """4xx client errors."""


class ServerError(ClientException):
    """5xx server errors."""


class TransientServerError(ClientException):
    """Transient 5xx server errors."""


class Unauthorized(ClientException):
    STATUS_CODE = 401


class RetryError(ClientException):
    """Raised when a function has exhausted all of its available retries.

    Parameters:
        message (str):
            The exception message.
        cause (Exception):
            The last exception raised when retring the function.
    """

    def __init__(self, message, cause, status_code=None, url=None):
        super().__init__(message, status_code=status_code, url=url)
        self.message = message
        self.cause = cause

    def __str__(self):
        return f'{self.message}, last exception: {self.cause}'


class TransientException(Exception):
    """Raise this exception when we know the cause is transient (e.g.: connection errors,
    consistency error, ...).
    """
