from httpx import Response
import pytest
from respx import MockRouter

from pythonxbox.api.client import XboxLiveClient
from tests.common import get_response_json


@pytest.mark.asyncio
async def test_titlehub_titlehistory(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.get("https://titlehub.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("titlehub_titlehistory"))
    )
    ret = await xbl_client.titlehub.get_title_history(987654321)

    assert len(ret.titles) == 5

    assert route.called


@pytest.mark.asyncio
async def test_titlehub_titleinfo(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.get("https://titlehub.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("titlehub_titleinfo"))
    )
    ret = await xbl_client.titlehub.get_title_info(1717113201)

    assert len(ret.titles) == 1
    assert ret.titles[0].detail.genres == ["Action & adventure"]

    assert route.called


@pytest.mark.asyncio
async def test_titlehub_titleinfo_by_xuid(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.get("https://titlehub.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("titlehub_titleinfo"))
    )
    ret = await xbl_client.titlehub.get_title_info_by_xuid(987654321, 1717113201)

    assert len(ret.titles) == 1
    assert "xuid(987654321)" in str(respx_mock.calls[0].request.url)

    assert route.called


@pytest.mark.asyncio
async def test_titlehub_titleinfo_by_pfn(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.get("https://titlehub.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("titlehub_titleinfo"))
    )
    ret = await xbl_client.titlehub.get_title_info_by_pfn(
        "Microsoft.SeaofThieves_8wekyb3d8bbwe"
    )

    assert len(ret.titles) == 1
    assert "pfn(Microsoft.SeaofThieves_8wekyb3d8bbwe)" in str(
        respx_mock.calls[0].request.url
    )

    assert route.called


@pytest.mark.asyncio
async def test_titlehub_batch(
    respx_mock: MockRouter, xbl_client: XboxLiveClient
) -> None:
    route = respx_mock.post("https://titlehub.xboxlive.com").mock(
        return_value=Response(200, json=get_response_json("titlehub_batch"))
    )
    ret = await xbl_client.titlehub.get_titles_batch(
        ["Microsoft.SeaofThieves_8wekyb3d8bbwe", "Microsoft.XboxApp_8wekyb3d8bbwe"]
    )

    assert len(ret.titles) == 2

    assert ret.titles[0].detail.genres == []
    assert ret.titles[1].detail.genres == ["Action & adventure"]

    assert route.called
