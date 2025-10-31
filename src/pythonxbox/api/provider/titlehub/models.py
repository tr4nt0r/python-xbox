from datetime import datetime
from enum import StrEnum
from typing import Any

from pythonxbox.common.models import CamelCaseModel, PascalCaseModel


class TitleFields(StrEnum):
    SERVICE_CONFIG_ID = "scid"
    ACHIEVEMENT = "achievement"
    STATS = "stats"
    GAME_PASS = "gamepass"  # noqa: S105
    IMAGE = "image"
    DETAIL = "detail"
    FRIENDS_WHO_PLAYED = "friendswhoplayed"
    ALTERNATE_TITLE_ID = "alternateTitleId"
    PRODUCT_ID = "productId"
    CONTENT_BOARD = "contentBoard"


class Achievement(CamelCaseModel):
    current_achievements: int
    total_achievements: int
    current_gamerscore: int
    total_gamerscore: int
    progress_percentage: float
    source_version: int


class Stats(CamelCaseModel):
    source_version: int


class GamePass(CamelCaseModel):
    is_game_pass: bool


class Image(CamelCaseModel):
    url: str
    type: str


class TitleHistory(CamelCaseModel):
    last_time_played: datetime
    visible: bool
    can_hide: bool


class Attribute(CamelCaseModel):
    applicable_platforms: list[str] | None = None
    maximum: int | None = None
    minimum: int | None = None
    name: str


class Availability(PascalCaseModel):
    actions: list[str]
    availability_id: str
    platforms: list[str]
    sku_id: str


class Detail(CamelCaseModel):
    attributes: list[Attribute]
    availabilities: list[Availability]
    capabilities: list[str]
    description: str
    developer_name: str | None = None
    genres: list[str] | None = None
    publisher_name: str
    min_age: int | None = None
    release_date: datetime | None = None
    short_description: str | None = None
    vui_display_name: str | None = None
    xbox_live_gold_required: bool


class Title(CamelCaseModel):
    title_id: str
    pfn: str | None = None
    bing_id: str | None = None
    service_config_id: str | None = None
    windows_phone_product_id: str | None = None
    name: str
    type: str
    devices: list[str]
    display_image: str
    media_item_type: str
    modern_title_id: str | None = None
    is_bundle: bool
    achievement: Achievement | None = None
    stats: Stats | None = None
    game_pass: GamePass | None = None
    images: list[Image] | None = None
    title_history: TitleHistory | None = None
    detail: Detail | None = None
    friends_who_played: Any = None
    alternate_title_ids: Any = None
    content_boards: Any = None
    xbox_live_tier: str | None = None
    is_streamable: bool | None = None


class TitleHubResponse(CamelCaseModel):
    xuid: str | None = None
    titles: list[Title]
