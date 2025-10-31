"""
RateLimitedProvider

Subclassed by providers with rate limit support
"""

from typing import TYPE_CHECKING
from pythonxbox.api.provider.baseprovider import BaseProvider
from pythonxbox.common.exceptions import XboxException
from pythonxbox.common.ratelimits import CombinedRateLimit
from pythonxbox.common.ratelimits.models import LimitType, ParsedRateLimit, TimePeriod

if TYPE_CHECKING:
    from pythonxbox.api.client import XboxLiveClient


class RateLimitedProvider(BaseProvider):
    # dict -> Dict (typing.dict) https://stackoverflow.com/a/63460173
    RATE_LIMITS: dict[str, int | dict[str, int]]

    def __init__(self, client: "XboxLiveClient") -> None:
        """
        Initialize Baseclass

        Args:
            client (:class:`XboxLiveClient`): Instance of XboxLiveClient
        """
        super().__init__(client)

        # Check that RATE_LIMITS set defined in the child class
        if hasattr(self, "RATE_LIMITS"):
            # Note: we cannot check (type(self.RATE_LIMITS) == dict) as the type hints have already defined it as such
            if "burst" and "sustain" in self.RATE_LIMITS:
                # We have the required keys, attempt to parse.
                # (type-checking for the values is performed in __parse_rate_limit_key)
                self.__handle_rate_limit_setup()
            else:
                raise XboxException(
                    "RATE_LIMITS object missing required keys 'burst', 'sustain'"
                )
        else:
            raise XboxException(
                "RateLimitedProvider as parent class but RATE_LIMITS not set!"
            )

    def __handle_rate_limit_setup(self) -> None:
        # Retrieve burst and sustain from the dict
        burst_key = self.RATE_LIMITS["burst"]
        sustain_key = self.RATE_LIMITS["sustain"]

        # Parse the rate limit dict values
        burst_rate_limits = self.__parse_rate_limit_key(burst_key, TimePeriod.BURST)
        sustain_rate_limits = self.__parse_rate_limit_key(
            sustain_key, TimePeriod.SUSTAIN
        )

        # Instanciate CombinedRateLimits for read and write respectively
        self.rate_limit_read = CombinedRateLimit(
            burst_rate_limits, sustain_rate_limits, type=LimitType.READ
        )
        self.rate_limit_write = CombinedRateLimit(
            burst_rate_limits, sustain_rate_limits, type=LimitType.WRITE
        )

    def __parse_rate_limit_key(
        self, key: int | dict[str, int], period: TimePeriod
    ) -> ParsedRateLimit:
        if isinstance(key, int) and not isinstance(key, bool):
            # bool is a subclass of int, hence the explicit check
            return ParsedRateLimit(read=key, write=key, period=period)
        elif isinstance(key, dict):
            # TODO: schema here?
            # Since the key-value pairs match we can just pass the dict to the model
            return ParsedRateLimit(**key, period=period)
            # return ParsedRateLimit(read=key["read"], write=key["write"])
        else:
            raise XboxException(
                "RATE_LIMITS value types not recognised. Must be one of 'int, 'dict'."
            )
