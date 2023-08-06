""" ASGI-Tools -- Tools to make ASGI Applications """

__version__ = "0.41.5"
__license__ = "MIT"

import logging


asgi_logger: logging.Logger = logging.getLogger('asgi-tools')


class ASGIError(Exception):
    """Base class for ASGI-Tools Errors."""

    pass


class ASGIConnectionClosed(ASGIError):
    """ASGI-Tools connection closed error."""

    pass


class ASGIDecodeError(ASGIError, ValueError):
    """ASGI-Tools decoding error."""

    pass


class ASGINotFound(ASGIError):
    """Raise when http handler not found."""

    pass


class ASGIMethodNotAllowed(ASGIError):
    """Raise when http method not found."""

    pass


DEFAULT_CHARSET: str = 'utf-8'

from .request import Request  # noqa
from .response import (  # noqa
    Response, ResponseHTML, ResponseJSON, ResponseText, ResponseRedirect,
    ResponseError, ResponseStream, ResponseFile, ResponseWebSocket, parse_response
)
from .middleware import (  # noqa
    RequestMiddleware, ResponseMiddleware, LifespanMiddleware,
    RouterMiddleware, StaticFilesMiddleware
)
from .app import App, HTTPView  # noqa

from http_router import NotFound, MethodNotAllowed  # noqa
