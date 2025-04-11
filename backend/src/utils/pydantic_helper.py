import json
from copy import deepcopy
from typing import Any, Optional, Tuple, Type

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer
from google.protobuf.message import Message
from pydantic import BaseModel, ConfigDict, ValidationError, create_model, model_validator
from pydantic.fields import FieldInfo

from src.utils.format import snake_to_camel, snake_to_pascal


def all_optional(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]
        return new.annotation, new

    return create_model(
        model.__name__,
        __base__=model,
        __module__=model.__module__,
        **{field_name: make_field_optional(field_info) for field_name, field_info in model.model_fields.items()},
    )


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=snake_to_camel, populate_by_name=True)

    def model_dump(self, *args, **kwargs) -> dict:
        if "by_alias" not in kwargs:
            kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)


class PascalCaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=snake_to_pascal, populate_by_name=True)


class FromProtobufModel(BaseModel):
    @model_validator(mode="before")
    def get(cls, data: Any):
        if not isinstance(data, Message):
            raise ValueError(
                f"{cls.__name__} сan only be used for values returned by a gRPC client. Not for {type(data)}"
            )
        result = {}
        for schema_key, schema_field in cls.model_fields.items():
            value = getattr(data, schema_key, schema_field.default)
            if isinstance(value, (RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer)):
                value = list(value)
            result[schema_key] = value
        return result

    model_config = ConfigDict(from_attributes=True)


class FromProtobufResponseModel(FromProtobufModel):
    @classmethod
    def model_validate(cls, *args, **kwargs):
        try:
            return super().model_validate(*args, **kwargs)
        except ValidationError as e:
            additional_message = "\r\nReal:\r\n"
            additional_message += str(args)
            error = CustomValidationError(e, additional_message=additional_message)
            raise error from e


class CustomValidationError(ValueError):
    def __init__(self, e: ValidationError, additional_message: str):
        self.e = e
        self.additional_message = additional_message
        super().__init__()

    def __str__(self) -> str:
        return str(self.e) + self.additional_message


class PydanticEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)


class BaseResponse(BaseModel):
    def __init__(self, **kwargs):
        error = None
        try:
            super().__init__(**kwargs)
        except ValidationError as e:
            additional_message = "\r\nReal:\r\n"
            additional_message += json.dumps(kwargs, indent=4, cls=PydanticEncoder, default=str)
            error = CustomValidationError(e, additional_message=additional_message)
        if error:
            raise error


class CamelCaseResponse(BaseResponse, CamelCaseModel):
    pass


class PascalCaseResponse(BaseResponse, PascalCaseModel):
    pass


class UpdatableModel(BaseModel):
    def update(self, data: BaseModel):
        self.__dict__.update(data.model_dump(exclude_unset=True, exclude_none=True))
        self.model_validate(self.model_dump())
        return self
