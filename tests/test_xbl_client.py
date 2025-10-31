from pythonxbox.api.client import XboxLiveClient
from pythonxbox.authentication.manager import AuthenticationManager


def test_authorization_header(auth_mgr: AuthenticationManager) -> None:
    client = XboxLiveClient(auth_mgr)

    assert (
        client._auth_mgr.xsts_token.authorization_header_value
        == "XBL3.0 x=abcdefg;123456789"
    )
