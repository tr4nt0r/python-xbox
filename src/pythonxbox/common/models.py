"""Base Models."""

from pydantic import BaseModel, ConfigDict


def to_pascal(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def to_lower(string: str) -> str:
    return string.replace("_", "")


class PascalCaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_pascal
    )


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_camel
    )


class LowerCaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True, alias_generator=to_lower
    )
