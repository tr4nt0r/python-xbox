"""
Mediahub - Fetch screenshots and gameclips
"""

from typing import ClassVar

from pythonxbox.api.provider.baseprovider import BaseProvider
from pythonxbox.api.provider.mediahub.models import (
    MediahubGameclips,
    MediahubScreenshots,
)


class MediahubProvider(BaseProvider):
    MEDIAHUB_URL = "https://mediahub.xboxlive.com"
    HEADERS: ClassVar = {"x-xbl-contract-version": "3"}

    async def fetch_own_clips(
        self, skip: int = 0, count: int = 500, **kwargs
    ) -> MediahubGameclips:
        """
        Fetch own clips

        Args:
            skip: Number of items to skip
            count: Max entries to fetch

        Returns:
            :class:`MediahubGameclips`: Gameclips
        """
        url = f"{self.MEDIAHUB_URL}/gameclips/search"
        post_data = {
            "max": count,
            "query": f"OwnerXuid eq {self.client.xuid}",
            "skip": skip,
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS, **kwargs
        )
        resp.raise_for_status()
        return MediahubGameclips.model_validate_json(resp.text)

    async def fetch_own_screenshots(
        self, skip: int = 0, count: int = 500, **kwargs
    ) -> MediahubScreenshots:
        """
        Fetch own screenshots

        Args:
            skip: Number of items to skip
            count: Max entries to fetch

        Returns:
            :class:`MediahubScreenshots`: Screenshots
        """
        url = f"{self.MEDIAHUB_URL}/screenshots/search"
        post_data = {
            "max": count,
            "query": f"OwnerXuid eq {self.client.xuid}",
            "skip": skip,
        }
        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS, **kwargs
        )
        resp.raise_for_status()
        return MediahubScreenshots.model_validate_json(resp.text)
