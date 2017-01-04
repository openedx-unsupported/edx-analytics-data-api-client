class ClientError(Exception):
    """Common base class for all client errors."""

    pass


class NotFoundError(ClientError):
    """URL was not found."""

    pass


class InvalidRequestError(ClientError):
    """The API request was invalid."""

    pass


class TimeoutError(ClientError):
    """The API server did not respond before the timeout expired."""

    pass
