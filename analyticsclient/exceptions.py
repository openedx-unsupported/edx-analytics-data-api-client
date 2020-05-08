class ClientError(Exception):
    """Common base class for all client errors."""


class NotFoundError(ClientError):
    """URL was not found."""


class InvalidRequestError(ClientError):
    """The API request was invalid."""


class TimeoutError(ClientError):  # pylint: disable=redefined-builtin
    """The API server did not respond before the timeout expired."""
