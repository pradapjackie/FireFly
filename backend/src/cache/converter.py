import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Type, Union

import pendulum
from pydantic import BaseModel
from yarl import URL


class PydanticRedisConverter:
    def __init__(self, model_class: Type[BaseModel]):
        self.model_class = model_class
        self.to_str_types = (str, int, float, URL, Path, datetime)
        self.to_json_types = (dict, list, tuple, bool)
        self.from_str_types = {item.__name__: item for item in (str, int, float, URL, Path)}
        self.from_json_types = {item.__name__: item for item in (dict, list, bool)}

    def encode_value(self, value: Any) -> Union[str, int, float]:
        if isinstance(value, Enum):
            encoded_value, value_type = str(value.value), type(value.value)
        elif isinstance(value, set):
            encoded_value, value_type = json.dumps(list(value)), type(value)
        elif isinstance(value, self.to_json_types):
            encoded_value, value_type = json.dumps(value, default=str), type(value)
        elif isinstance(value, self.to_str_types):
            encoded_value, value_type = str(value), type(value)
        else:
            raise NotImplementedError(f"No encoder for type: {type(value)}")
        return json.dumps((encoded_value, str(value_type.__name__)))

    def decode_value(self, value: str) -> Any:
        value, value_type = json.loads(value)
        if value_type in self.from_json_types:
            return json.loads(value)
        elif value_type in self.from_str_types:
            return self.from_str_types.get(value_type)(value)
        elif value_type == datetime.__name__:
            return pendulum.parse(value).to_datetime_string()
        elif value_type == pendulum.DateTime.__name__:
            return pendulum.parse(value)
        elif value_type == tuple.__name__:
            return tuple(json.loads(value))
        elif value_type == set.__name__:
            return set(json.loads(value))
        else:
            raise NotImplementedError(f"No decoder for type: {value_type}")

    def encode_to_dict(self, model: BaseModel, exclude_unset=False) -> Dict[str, Union[str, int, float]]:
        return {
            k: self.encode_value(v) for k, v in model.model_dump(exclude_none=True, exclude_unset=exclude_unset).items()
        }

    def encode_to_str(self, model: BaseModel) -> str:
        return json.dumps({k: self.encode_value(v) for k, v in model.model_dump(exclude_none=True).items()})

    def decode_from_dict(self, value: dict):
        return self.model_class(**{k.decode("utf-8"): self.decode_value(v.decode("UTF-8")) for k, v in value.items()})

    def decode_from_bytes(self, value: bytes):
        data = json.loads(value.decode("UTF-8"))
        return self.model_class(**{k: self.decode_value(v) for k, v in data.items()})

    @staticmethod
    def decode_dict(dictionary: Dict[bytes, bytes]) -> Dict[str, str]:
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in dictionary.items()}
