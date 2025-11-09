from pythonxbox.common.models import FlatCaseModel, PascalCaseModel


class GeneralStatsField:
    MINUTES_PLAYED = "MinutesPlayed"


class GroupProperties(PascalCaseModel):
    ordinal: str | None = None
    sort_order: str | None = None
    display_name: str | None = None
    display_format: str | None = None
    display_semantic: str | None = None


class Properties(PascalCaseModel):
    display_name: str | None = None


class Stat(FlatCaseModel):
    group_properties: GroupProperties | None = None
    xuid: str
    scid: str
    name: str
    type: str
    value: str
    properties: Properties


class StatListsCollectionItem(FlatCaseModel):
    arrange_by_field: str
    arrange_by_field_id: str
    stats: list[Stat]


class Group(FlatCaseModel):
    name: str
    title_id: str | None = None
    statlistscollection: list[StatListsCollectionItem]


class UserStatsResponse(FlatCaseModel):
    groups: list[Group] | None = None
    statlistscollection: list[StatListsCollectionItem]
