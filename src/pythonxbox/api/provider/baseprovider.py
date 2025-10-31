"""
BaseProvider

Subclassed by every *real* provider
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pythonxbox.api.client import XboxLiveClient


class BaseProvider:
    def __init__(self, client: "XboxLiveClient") -> None:
        """
        Initialize an the BaseProvider

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        self.client = client
