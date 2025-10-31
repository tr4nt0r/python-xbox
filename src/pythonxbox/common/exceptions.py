"""
Special Exception subclasses
"""

from typing import Any
from pythonxbox.common.ratelimits import RateLimit
from httpx import Response


class XboxException(Exception):
    """Base exception for all Xbox exceptions to subclass"""

    pass


class AuthenticationException(XboxException):
    """Raised when logging in fails, likely due to incorrect auth credentials"""

    pass


class TwoFactorAuthRequired(XboxException):
    def __init__(self, message: str, server_data: dict[str, Any]) -> None:
        """
        Raised when 2FA is required

        Args:
            message (str): Exception message
            server_data (dict): Server data dict, extracted js object from windows live auth request
        """
        super().__init__(message)
        self.server_data = server_data


class InvalidRequest(XboxException):
    def __init__(self, message: str, response: Response) -> None:
        """
        Raised when something is wrong with the request

        Args:
            message (str): error message returned by the server
            response (requests.Response): Instance of :class:`requests.Response`

        """
        self.message = message
        self.response = response


class NotFoundException(XboxException):
    """Any exception raised due to a resource being missing will subclass this"""

    pass


class RateLimitExceededException(XboxException):
    def __init__(self, message: str, rate_limit: RateLimit) -> None:
        self.message = message
        self.rate_limit = rate_limit
        self.try_again_in = rate_limit.get_reset_after()
