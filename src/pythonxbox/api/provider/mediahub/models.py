from typing import Optional

from pythonxbox.common.models import CamelCaseModel


class ContentSegment(CamelCaseModel):
    segment_id: int
    creation_type: str
    creator_channel_id: Optional[str] = None
    creator_xuid: int
    record_date: str
    duration_in_seconds: int
    offset: int
    secondary_title_id: Optional[int] = None
    title_id: int


class ContentLocator(CamelCaseModel):
    expiration: Optional[str] = None
    file_size: Optional[int] = None
    locator_type: str
    uri: str


class GameclipContent(CamelCaseModel):
    content_id: str
    content_locators: list[ContentLocator]
    content_segments: list[ContentSegment]
    creation_type: str
    duration_in_seconds: int
    local_id: str
    owner_xuid: int
    sandbox_id: str
    shared_to: list[int]
    title_id: int
    title_name: str
    upload_date: str
    upload_language: str
    upload_region: str
    upload_title_id: int
    upload_device_type: str
    comment_count: int
    like_count: int
    share_count: int
    view_count: int
    content_state: str
    enforcement_state: str
    sessions: list[str]
    tournaments: list[str]


class MediahubGameclips(CamelCaseModel):
    values: list[GameclipContent]


class ScreenshotContent(CamelCaseModel):
    content_id: str
    capture_date: str
    content_locators: list[ContentLocator]
    local_id: str
    owner_xuid: int
    resolution_height: int
    resolution_width: int
    date_uploaded: str
    sandbox_id: str
    shared_to: list[int]
    title_id: int
    title_name: str
    upload_language: str
    upload_region: str
    upload_title_id: int
    upload_device_type: str
    comment_count: int
    like_count: int
    share_count: int
    view_count: int
    content_state: str
    enforcement_state: str
    sessions: list[str]
    tournaments: list[str]


class MediahubScreenshots(CamelCaseModel):
    values: list[ScreenshotContent]
