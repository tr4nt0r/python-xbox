from pythonxbox.common.models import PascalCaseModel


class Item(PascalCaseModel):
    item_id: str
    content_type: str
    title: str | None = None
    device_type: str
    provider: str | None = None
    provider_id: str | None = None


class ListItem(PascalCaseModel):
    date_added: str
    date_modified: str
    index: int
    k_value: int
    item: Item


class ListMetadata(PascalCaseModel):
    list_title: str
    list_version: int
    list_count: int
    allow_duplicates: bool
    max_list_size: int
    access_setting: str


class ListsResponse(PascalCaseModel):
    impression_id: str
    list_items: list[ListItem]
    list_metadata: ListMetadata
