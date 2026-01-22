from httpx import Response
import pytest
from respx import MockRouter

from pythonxbox.api.client import XboxLiveClient
from pythonxbox.api.provider.presence.models import PresenceState
from tests.common import get_response_json


@pytest.mark.asyncio
async def test_presence(respx_mock: MockRouter, xbl_client: XboxLiveClient) -> None:
    route = respx_mock.get("https://userpresence.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("presence"))
    )
    await xbl_client.presence.get_presence("2669321029139235")

    assert route.called


@pytest.mark.asyncio
async def test_presence_batch(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.post("https://userpresence.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("presence_batch"))
    )
    ret = await xbl_client.presence.get_presence_batch(
        ["2669321029139235", "2584878536129841"]
    )

    assert len(ret) == 2
    assert route.called


@pytest.mark.asyncio
async def test_presence_too_many_people(xbl_client: XboxLiveClient) -> None:
    xuids = range(0, 2000)
    with pytest.raises(Exception) as err:
        await xbl_client.presence.get_presence_batch(xuids)

    assert "length is > 1100" in str(err)


@pytest.mark.asyncio
async def test_presence_own(respx_mock: MockRouter, xbl_client: XboxLiveClient) -> None:
    route = respx_mock.get("https://userpresence.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("presence_own"))
    )
    await xbl_client.presence.get_presence_own()

    assert route.called


@pytest.mark.asyncio
async def test_presence_own_set(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.put(
        "https://userpresence.xboxlive.com/users/xuid(2669321029139235)/state"
    ).mock(return_value=Response(200))

    ret = await xbl_client.presence.set_presence_own(PresenceState.ACTIVE)

    assert route.called
    assert ret


@pytest.mark.asyncio
async def test_presence_own_set_fail(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.put(
        "https://userpresence.xboxlive.com/users/xuid(2669321029139235)/state"
    ).mock(return_value=Response(500))

    ret = await xbl_client.presence.set_presence_own(PresenceState.CLOAKED)

    assert route.called
    assert not ret

@pytest.mark.asyncio
async def test_presence_with_activity(respx_mock: MockRouter, xbl_client: XboxLiveClient) -> None:
    custom_data = {
        "xuid": "0123456789",
        "state": "online",
        "devices": [
            {
                "type": "D",
                "titles": [
                    {
                        "id": "12341234",
                        "name": "Contoso 5",
                        "state": "active",
                        "placement": "fill",
                        "timestamp": "2012-09-17T07:15:23.4930000",
                        "activity": {"richPresence": "Team Deathmatch on Nirvana"}
                    }
                ]
            }
        ]
    }

    route = respx_mock.get("https://userpresence.xboxlive.com").mock(
        return_value=Response(200, json=custom_data)
    )

    response = await xbl_client.presence.get_presence("0123456789")

    assert route.called
    assert response.xuid == "0123456789"
    assert response.devices[0].titles[0].activity.richPresence == "Team Deathmatch on Nirvana"

