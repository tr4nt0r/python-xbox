"""Base Models."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_pascal


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
