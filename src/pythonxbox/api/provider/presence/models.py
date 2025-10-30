from enum import Enum
from pydantic import RootModel

from pythonxbox.common.models import CamelCaseModel


class PresenceLevel(str, Enum):
    USER = "user"
    DEVICE = "device"
    TITLE = "title"
    ALL = "all"


class PresenceState(str, Enum):
    ACTIVE = "Active"
    CLOAKED = "Cloaked"


class LastSeen(CamelCaseModel):
    device_type: str
    title_id: str | None = None
    title_name: str
    timestamp: str


class ActivityRecord(CamelCaseModel):
    richPresence: str | None = None
    media: str | None = None


class TitleRecord(CamelCaseModel):
    id: str | None = None
    name: str | None = None
    activity: list[ActivityRecord] | None = None
    lastModified: str | None = None
    placement: str | None = None
    state: str | None = None


class DeviceRecord(CamelCaseModel):
    titles: list[TitleRecord] | None = None
    type: str | None = None


class PresenceItem(CamelCaseModel):
    xuid: str
    state: str
    last_seen: LastSeen | None = None
    devices: list[DeviceRecord] | None = None


class PresenceBatchResponse(RootModel[list[PresenceItem]], CamelCaseModel):
    root: list[PresenceItem]
