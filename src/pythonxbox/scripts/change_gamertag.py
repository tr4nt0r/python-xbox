"""
Example script that enables using your one-time-free gamertag change
"""

import argparse
import asyncio
import os
import sys

from httpx import HTTPStatusError

from pythonxbox.api.client import XboxLiveClient
from pythonxbox.api.provider.account.models import (
    ChangeGamertagResult,
    ClaimGamertagResult,
)
from pythonxbox.authentication.manager import AuthenticationManager
from pythonxbox.authentication.models import OAuth2TokenResponse
from pythonxbox.common.signed_session import SignedSession
from pythonxbox.scripts import CLIENT_ID, CLIENT_SECRET, TOKENS_FILE

GAMERTAG_MAX_LEN = 15


async def async_main() -> None:
    parser = argparse.ArgumentParser(description="Change your gamertag")
    parser.add_argument(
        "--tokens",
        "-t",
        default=TOKENS_FILE,
        help=f"Token filepath. Default: '{TOKENS_FILE}'",
    )
    parser.add_argument(
        "--client-id",
        "-cid",
        default=os.environ.get("CLIENT_ID", CLIENT_ID),
        help="OAuth2 Client ID",
    )
    parser.add_argument(
        "--client-secret",
        "-cs",
        default=os.environ.get("CLIENT_SECRET", CLIENT_SECRET),
        help="OAuth2 Client Secret",
    )
    parser.add_argument("gamertag", help="Desired Gamertag")

    args = parser.parse_args()

    if len(args.gamertag) > GAMERTAG_MAX_LEN:
        print(f"Desired gamertag exceedes limit of {GAMERTAG_MAX_LEN} chars")
        sys.exit(-1)

    if not os.path.exists(args.tokens):
        print("No token file found, run xbox-authenticate")
        sys.exit(-1)

    async with SignedSession() as session:
        auth_mgr = AuthenticationManager(
            session, args.client_id, args.client_secret, ""
        )

        with open(args.tokens) as f:
            tokens = f.read()
        auth_mgr.oauth = OAuth2TokenResponse.model_validate_json(tokens)
        try:
            await auth_mgr.refresh_tokens()
        except HTTPStatusError:
            print("Could not refresh tokens")
            sys.exit(-1)

        with open(args.tokens, mode="w") as f:
            f.write(auth_mgr.oauth.json())

        xbl_client = XboxLiveClient(auth_mgr)

        print(
            ":: Trying to change gamertag to '%s' for xuid '%i'..."
            % (args.gamertag, xbl_client.xuid)
        )

        print("Claiming gamertag...")
        try:
            resp = await xbl_client.account.claim_gamertag(
                xbl_client.xuid, args.gamertag
            )
            if resp == ClaimGamertagResult.NotAvailable:
                print("Claiming gamertag failed - Desired gamertag is unavailable")
                sys.exit(-1)
        except HTTPStatusError:
            print("Invalid HTTP response from claim")
            sys.exit(-1)

        print("Changing gamertag...")
        try:
            resp = await xbl_client.account.change_gamertag(
                xbl_client.xuid, args.gamertag
            )
            if resp == ChangeGamertagResult.NoFreeChangesAvailable:
                print("Changing gamertag failed - You are out of free changes")
                sys.exit(-1)
        except HTTPStatusError:
            print("Invalid HTTP response from change")
            sys.exit(-1)

        print("Gamertag successfully changed to %s" % args.gamertag)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
