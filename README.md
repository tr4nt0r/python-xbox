# python-xbox

[![PyPi - latest](https://img.shields.io/pypi/v/python-xbox.svg)](https://pypi.python.org/pypi/python-xbox/)
[![Build](https://github.com/tr4nt0r/python-xbox/actions/workflows/build.yml/badge.svg)](https://github.com/tr4nt0r/python-xbox/actions/workflows/build.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/python-xbox?style=flat&label=pypi%20downloads)
[!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/tr4nt0r)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub-Sponsor-blue?logo=github)](https://github.com/sponsors/tr4nt0r)

python-xbox is a python library to authenticate with Xbox Network via your Microsoft Account and provides Xbox related Web-API.

Authentication is supported via OAuth2.

- Register a new application in [Azure AD](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
  - Name your app
  - Select "Personal Microsoft accounts only" under supported account types
  - Add <http://localhost/auth/callback> as a Redirect URI of type "Web"
- Copy your Application (client) ID for later use
- On the App Page, navigate to "Certificates & secrets"
  - Generate a new client secret and save for later use

## Dependencies

- Python >= 3.11

## How to use

### Install

```bash
pip install python-xbox
```

### Authentication

> [!NOTE]
> You must use non child account (> 18 years old)

Token save location: If tokenfile is not provided via cmdline, fallback of `<platformdirs.user_data_dir>/tokens.json` is used as save-location

Specifically:

Windows: `C:\\Users\\<username>\\AppData\\Local\\OpenXbox\\xbox`

Mac OSX: `/Users/<username>/Library/Application Support/xbox/tokens.json`

Linux: `/home/<username>/.local/share/xbox`

For more information, see: <https://pypi.org/project/platformdirs> and module: `python-xbox.scripts.constants`

```bash
xbox-authenticate --client-id <client-id> --client-secret <client-secret>
```

Example: Search Xbox Live via cmdline tool

```bash
  # Search Xbox One Catalog
  xbox-searchlive "Some game title"
```

API usage

```python
import asyncio
import sys

from httpx import HTTPStatusError

from pythonxbox.api.client import XboxLiveClient
from pythonxbox.authentication.manager import AuthenticationManager
from pythonxbox.authentication.models import OAuth2TokenResponse
from pythonxbox.common.signed_session import SignedSession
from pythonxbox.scripts import CLIENT_ID, CLIENT_SECRET, TOKENS_FILE

"""
This uses the global default client identification by OpenXbox
You can supply your own parameters here if you are permitted to create
new Microsoft OAuth Apps and know what you are doing
"""
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
tokens_file = TOKENS_FILE

"""
For doing authentication, see pythonxbox/scripts/authenticate.py
"""


async def async_main():
    # Create a HTTP client session
    async with SignedSession() as session:
        """
        Initialize with global OAUTH parameters from above
        """
        auth_mgr = AuthenticationManager(session, client_id, client_secret, "")

        """
        Read in tokens that you received from the `xbox-authenticate`-script previously
        See `pythonxbox/scripts/authenticate.py`
        """
        try:
            with open(tokens_file) as f:
                tokens = f.read()
            # Assign gathered tokens
            auth_mgr.oauth = OAuth2TokenResponse.model_validate_json(tokens)
        except FileNotFoundError as e:
            print(
                f"File {tokens_file} isn`t found or it doesn`t contain tokens! err={e}"
            )
            print("Authorizing via OAUTH")
            url = auth_mgr.generate_authorization_url()
            print(f"Auth via URL: {url}")
            authorization_code = input("Enter authorization code> ")
            tokens = await auth_mgr.request_oauth_token(authorization_code)
            auth_mgr.oauth = tokens

        """
        Refresh tokens, just in case
        You could also manually check the token lifetimes and just refresh them
        if they are close to expiry
        """
        try:
            await auth_mgr.refresh_tokens()
        except HTTPStatusError as e:
            print(
                f"""
                Could not refresh tokens from {tokens_file}, err={e}\n
                You might have to delete the tokens file and re-authenticate 
                if refresh token is expired
            """
            )
            sys.exit(-1)

        # Save the refreshed/updated tokens
        with open(tokens_file, mode="w") as f:
            f.write(auth_mgr.oauth.json())
        print(f"Refreshed tokens in {tokens_file}!")

        """
        Construct the Xbox API client from AuthenticationManager instance
        """
        xbl_client = XboxLiveClient(auth_mgr)

        """
        Some example API calls
        """
        # Get friendslist
        friendslist = await xbl_client.people.get_friends_own()
        print(f"Your friends: {friendslist}\n")

        # Get presence status (by list of XUID)
        presence = await xbl_client.presence.get_presence_batch(
            ["2533274794093122", "2533274807551369"]
        )
        print(f"Statuses of some random players by XUID: {presence}\n")

        # Get messages
        messages = await xbl_client.message.get_inbox()
        print(f"Your messages: {messages}\n")

        # Get profile by GT
        profile = await xbl_client.profile.get_profile_by_gamertag("SomeGamertag")
        print(f"Profile under SomeGamertag gamer tag: {profile}\n")


asyncio.run(async_main())
```

## Contribute

- Report bugs/suggest features
- Add/update docs
- Add additional xbox live endpoints

## Credits

This library is derived from [xbox-webapi](https://github.com/OpenXbox/xbox-webapi-python) library from the [OpenXbox](https://github.com/openxbox) project
The authentication code is based on [joealcorn/xbox](https://github.com/joealcorn/xbox)

Informations on endpoints gathered from:

- [XboxLive REST Reference](https://docs.microsoft.com/en-us/windows/uwp/xbox-live/xbox-live-rest/atoc-xboxlivews-reference)
- [XboxLiveTraceAnalyzer APIMap](https://github.com/Microsoft/xbox-live-trace-analyzer/blob/master/Source/XboxLiveTraceAnalyzer.APIMap.csv)
- [Xbox Live Service API](https://github.com/Microsoft/xbox-live-api)

## Disclaimer

Xbox, Xbox One, Smartglass and Xbox Live are trademarks of Microsoft Corporation. Team OpenXbox is in no way endorsed by or affiliated with Microsoft Corporation, or any associated subsidiaries, logos or trademarks.
