from datetime import datetime
from typing import Any

from pythonxbox.common.models import CamelCaseModel


class Part(CamelCaseModel):
    content_type: str
    version: int
    text: str | None = None
    unsuitable_for: list | None = None
    locator: str | None = None


class Content(CamelCaseModel):
    parts: list[Part]


class ContentPayload(CamelCaseModel):
    content: Content


class Message(CamelCaseModel):
    content_payload: ContentPayload | None = None
    timestamp: datetime
    last_update_timestamp: datetime
    type: str
    network_id: str
    conversation_type: str
    conversation_id: str
    owner: int | None = None
    sender: str
    message_id: str
    is_deleted: bool
    is_server_updated: bool


class Conversation(CamelCaseModel):
    timestamp: datetime
    network_id: str
    type: str
    conversation_id: str
    voice_id: str
    participants: list[str]
    read_horizon: str
    delete_horizon: str
    is_read: bool
    muted: bool
    folder: str
    last_message: Message


class Primary(CamelCaseModel):
    folder: str
    total_count: int
    unread_count: int
    conversations: list[Conversation]


class SafetySettings(CamelCaseModel):
    version: int
    primary_inbox_media: str
    primary_inbox_text: str
    primary_inbox_url: str
    secondary_inbox_media: str
    secondary_inbox_text: str
    secondary_inbox_url: str
    can_unobscure: bool


class InboxResponse(CamelCaseModel):
    primary: Primary
    folders: list[Any]
    safety_settings: SafetySettings


class ConversationResponse(CamelCaseModel):
    timestamp: datetime
    network_id: str
    type: str
    conversation_id: str
    participants: list[str] | None = None
    read_horizon: str
    delete_horizon: str
    is_read: bool
    muted: bool
    folder: str
    messages: list[Message] | None = None
    continuation_token: str | None = None
    voice_id: str
    voice_roster: list[Any] | None = None


class SendMessageResponse(CamelCaseModel):
    message_id: str
    conversation_id: str
