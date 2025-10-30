"""
Profile

Get Userprofiles by XUID or Gamertag
"""

from typing import List

from pythonxbox.api.provider.ratelimitedprovider import RateLimitedProvider
from pythonxbox.api.provider.profile.models import ProfileResponse, ProfileSettings


class ProfileProvider(RateLimitedProvider):
    PROFILE_URL = "https://profile.xboxlive.com"
    HEADERS_PROFILE = {"x-xbl-contract-version": "3"}
    SEPARATOR = ","

    RATE_LIMITS = {"burst": 10, "sustain": 30}

    async def get_profiles(self, xuid_list: List[str], **kwargs) -> ProfileResponse:
        """
        Get profile info for list of xuids

        Args:
            xuid_list (list): List of xuids

        Returns:
            :class:`ProfileResponse`: Profile Response
        """
        post_data = {
            "settings": [
                ProfileSettings.GAME_DISPLAY_NAME,
                ProfileSettings.APP_DISPLAY_NAME,
                ProfileSettings.APP_DISPLAYPIC_RAW,
                ProfileSettings.GAMERSCORE,
                ProfileSettings.GAMERTAG,
                ProfileSettings.GAME_DISPLAYPIC_RAW,
                ProfileSettings.ACCOUNT_TIER,
                ProfileSettings.TENURE_LEVEL,
                ProfileSettings.XBOX_ONE_REP,
                ProfileSettings.PREFERRED_COLOR,
                ProfileSettings.LOCATION,
                ProfileSettings.BIOGRAPHY,
                ProfileSettings.WATERMARKS,
                ProfileSettings.REAL_NAME,
            ],
            "userIds": xuid_list,
        }
        url = self.PROFILE_URL + "/users/batch/profile/settings"
        resp = await self.client.session.post(
            url,
            json=post_data,
            headers=self.HEADERS_PROFILE,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return ProfileResponse(**resp.json())

    async def get_profile_by_xuid(self, target_xuid: str, **kwargs) -> ProfileResponse:
        """
        Get Userprofile by xuid

        Args:
            target_xuid: XUID to get profile for

        Returns:
            :class:`ProfileResponse`: Profile Response
        """
        url = self.PROFILE_URL + f"/users/xuid({target_xuid})/profile/settings"
        params = {
            "settings": self.SEPARATOR.join(
                [
                    ProfileSettings.GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG_SUFFIX,
                    ProfileSettings.UNIQUE_MODERN_GAMERTAG,
                    ProfileSettings.REAL_NAME_OVERRIDE,
                    ProfileSettings.BIOGRAPHY,
                    ProfileSettings.LOCATION,
                    ProfileSettings.GAMERSCORE,
                    ProfileSettings.GAME_DISPLAYPIC_RAW,
                    ProfileSettings.TENURE_LEVEL,
                    ProfileSettings.ACCOUNT_TIER,
                    ProfileSettings.XBOX_ONE_REP,
                    ProfileSettings.PREFERRED_COLOR,
                    ProfileSettings.WATERMARKS,
                    ProfileSettings.IS_QUARANTINED,
                ]
            )
        }
        resp = await self.client.session.get(
            url,
            params=params,
            headers=self.HEADERS_PROFILE,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return ProfileResponse(**resp.json())

    async def get_profile_by_gamertag(self, gamertag: str, **kwargs) -> ProfileResponse:
        """
        Get Userprofile by gamertag

        Args:
            gamertag: Gamertag to get profile for

        Returns:
            :class:`ProfileResponse`: Profile Response
        """
        url = self.PROFILE_URL + f"/users/gt({gamertag})/profile/settings"
        params = {
            "settings": self.SEPARATOR.join(
                [
                    ProfileSettings.GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG_SUFFIX,
                    ProfileSettings.UNIQUE_MODERN_GAMERTAG,
                    ProfileSettings.REAL_NAME_OVERRIDE,
                    ProfileSettings.BIOGRAPHY,
                    ProfileSettings.LOCATION,
                    ProfileSettings.GAMERSCORE,
                    ProfileSettings.GAME_DISPLAYPIC_RAW,
                    ProfileSettings.TENURE_LEVEL,
                    ProfileSettings.ACCOUNT_TIER,
                    ProfileSettings.XBOX_ONE_REP,
                    ProfileSettings.PREFERRED_COLOR,
                    ProfileSettings.WATERMARKS,
                    ProfileSettings.IS_QUARANTINED,
                ]
            )
        }
        resp = await self.client.session.get(
            url,
            params=params,
            headers=self.HEADERS_PROFILE,
            rate_limits=self.rate_limit_read,
            **kwargs,
        )
        resp.raise_for_status()
        return ProfileResponse(**resp.json())
