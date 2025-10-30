from datetime import datetime

from pythonxbox.common.models import CamelCaseModel


class Thumbnail(CamelCaseModel):
    uri: str
    file_size: int
    thumbnail_type: int


class GameClipUri(CamelCaseModel):
    uri: str
    file_size: int
    uri_type: int
    expiration: str


class GameClip(CamelCaseModel):
    game_clip_id: str
    state: int
    date_published: datetime
    date_recorded: datetime
    last_modified: datetime
    user_caption: str
    type: int
    duration_in_seconds: int
    scid: str
    title_id: int
    rating: float
    rating_count: int
    views: int
    title_data: str
    system_properties: str
    saved_by_user: bool
    achievement_id: str
    greatest_moment_id: str
    thumbnails: list[Thumbnail]
    game_clip_uris: list[GameClipUri]
    xuid: str
    clip_name: str
    title_name: str
    game_clip_locale: str
    clip_content_attributes: int
    device_type: str
    comment_count: int
    like_count: int
    share_count: int
    partial_views: int


class PagingInfo(CamelCaseModel):
    continuation_token: str | None = None


class GameclipsResponse(CamelCaseModel):
    game_clips: list[GameClip]
    paging_info: PagingInfo
