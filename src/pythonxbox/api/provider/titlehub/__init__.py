"""
Titlehub - Get Title history and info
"""

from typing import TYPE_CHECKING

from pythonxbox.api.provider.baseprovider import BaseProvider
from pythonxbox.api.provider.titlehub.models import TitleFields, TitleHubResponse

if TYPE_CHECKING:
    from pythonxbox.api.client import XboxLiveClient


class TitlehubProvider(BaseProvider):
    TITLEHUB_URL = "https://titlehub.xboxlive.com"
    SEPARATOR = ","

    def __init__(self, client: "XboxLiveClient") -> None:
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super().__init__(client)
        self._headers = {
            "x-xbl-contract-version": "2",
            "x-xbl-client-name": "XboxApp",
            "x-xbl-client-type": "UWA",
            "x-xbl-client-version": "39.39.22001.0",
            "Accept-Language": self.client.language.locale,
        }

    async def get_title_history(
        self,
        xuid: str,
        fields: list[TitleFields] | None = None,
        max_items: int | None = 5,
        **kwargs,
    ) -> TitleHubResponse:
        """
        Get recently played titles

        Args:
            xuid: Xuid
            fields: List of titlefield
            max_items: Maximum items

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = f"{self.TITLEHUB_URL}/users/xuid({xuid})/titles/titlehistory/decoration/{fields}"
        params = {"maxItems": max_items}
        resp = await self.client.session.get(
            url, params=params, headers=self._headers, **kwargs
        )
        resp.raise_for_status()
        return TitleHubResponse.model_validate_json(resp.text)

    async def _get_title_info(
        self, moniker: str, fields: list[TitleFields] | None = None, **kwargs
    ) -> TitleHubResponse:
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.ALTERNATE_TITLE_ID,
                TitleFields.DETAIL,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = f"{self.TITLEHUB_URL}/users/xuid({self.client.xuid})/titles/{moniker}/decoration/{fields}"
        resp = await self.client.session.get(url, headers=self._headers, **kwargs)
        resp.raise_for_status()
        return TitleHubResponse.model_validate_json(resp.text)

    async def get_title_info(
        self, title_id: str, fields: list[TitleFields] | None = None, **kwargs
    ) -> TitleHubResponse:
        """
        Get info for specific title

        Args:
            title_id: Title Id
            fields: List of title fields

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        return await self._get_title_info(f"titleid({title_id})", fields, **kwargs)

    async def get_title_info_by_pfn(
        self, pfn: str, fields: list[TitleFields] | None = None, **kwargs
    ) -> TitleHubResponse:
        """
        Get info for specific title by PFN

        Args:
            pfn: Package family name
            fields: List of title fields

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        return await self._get_title_info(f"pfn({pfn})", fields, **kwargs)

    async def get_titles_batch(
        self, pfns: list[str], fields: list[TitleFields] | None = None, **kwargs
    ) -> TitleHubResponse:
        """
        Get Title info via PFN ids

        Args:
            pfns: List of Package family names (e.g. 'Microsoft.XboxApp_8wekyb3d8bbwe')
            fields: List of title fields

        Returns:
            :class:`TitleHubResponse`: Title Hub Response
        """
        if not fields:
            fields = [
                TitleFields.ACHIEVEMENT,
                TitleFields.DETAIL,
                TitleFields.IMAGE,
                TitleFields.SERVICE_CONFIG_ID,
            ]
        fields = self.SEPARATOR.join(fields)

        url = self.TITLEHUB_URL + f"/titles/batch/decoration/{fields}"
        post_data = {"pfns": pfns, "windowsPhoneProductIds": []}
        resp = await self.client.session.post(
            url, json=post_data, headers=self._headers, **kwargs
        )
        resp.raise_for_status()
        return TitleHubResponse.model_validate_json(resp.text)
