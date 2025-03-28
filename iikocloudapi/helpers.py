from copy import deepcopy
from typing import Any

from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo


class ExternalData(BaseModel):
    key: str
    value: str


class BaseResponseModel(BaseModel):
    correlation_id: str = Field(alias="correlationId")


def partial_model(model: type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = field.annotation | None  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{field_name: make_field_optional(field_info) for field_name, field_info in model.model_fields.items()},  # type: ignore
    )  # type: ignore
