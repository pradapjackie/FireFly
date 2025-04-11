from datetime import date
from enum import StrEnum
from io import BytesIO
from typing import Any, List, Type

import pendulum
from pydantic import BaseModel, ConfigDict, field_serializer


class MobilePlatformEnum(StrEnum):
    ios = "ios"
    android = "android"


class FieldTypeEnum(StrEnum):
    string = "string"
    number = "number"
    checkbox = "checkbox"
    autocomplete = "autocomplete"
    multi_autocomplete = "multi_autocomplete"
    string_list = "string_list"
    switch = "switch"
    file = "file"
    date = "date"


class Field(BaseModel):
    type: FieldTypeEnum
    label: str
    placeholder: str = ""
    value: Any = None
    default_value: Any = None
    optional: bool = False
    python_type: Type | None = None

    @field_serializer("python_type")
    def serialize_type(self, python_type: Type):
        return str(python_type)

    model_config = ConfigDict(validate_assignment=True)


class StringField(Field):
    type: FieldTypeEnum = FieldTypeEnum.string
    python_type: Type = str
    default_value: str | None = None
    value: str | None = None


class NumberField(Field):
    type: FieldTypeEnum = FieldTypeEnum.number
    default_value: int | float | None = None
    value: int | float | None = None


class CheckboxFiled(Field):
    type: FieldTypeEnum = FieldTypeEnum.checkbox
    python_type: Type = bool
    default_value: bool = False
    value: bool | None = None


class AutocompleteFiled(Field):
    type: FieldTypeEnum = FieldTypeEnum.autocomplete
    options: List[str]
    default_value: str | None = None
    value: str | None = None


class AutocompleteMultiFiled(Field):
    type: FieldTypeEnum = FieldTypeEnum.multi_autocomplete
    options: List[str]
    default_value: str | None = None
    value: str | None = None


class StringListFiled(Field):
    type: FieldTypeEnum = FieldTypeEnum.string_list
    default_value: List[str] | None = None
    value: List[str] | None = None


class SwitchFiled(Field):
    type: FieldTypeEnum = FieldTypeEnum.switch
    python_type: Type = bool
    default_value: bool = False
    value: bool | None = None


class AppiumCapabilitiesValue(BaseModel):
    os: MobilePlatformEnum
    app: str
    device: str
    version: str


class FileField(Field):
    type: FieldTypeEnum = FieldTypeEnum.file
    python_type: Type = BytesIO
    value: bytes | None = None


class DateField(Field):
    type: FieldTypeEnum = FieldTypeEnum.date
    python_type: Type = pendulum.Date
    value: date | pendulum.Date | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
