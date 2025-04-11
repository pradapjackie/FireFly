from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import Any, Dict, List

import bcrypt
import pendulum
from pydantic import BaseModel


class AnyEqualMixin:
    pass


class ApproximatelyEqual(float, AnyEqualMixin):
    def __new__(cls, value, diff_percentage):
        return super().__new__(cls, value)

    def __init__(self, value: float, diff_percentage: float):
        float.__init__(value)
        self.value = value
        self.margin = abs(value * (float(diff_percentage) / 100))

    def __eq__(self, other):
        try:
            other = float(other)
        except ValueError:
            return NotImplemented
        return self.value - self.margin <= other <= self.value + self.margin

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"~{self.value}(±{self.margin})"


class ApproximatelyAbsoluteEqual(float, AnyEqualMixin):
    def __new__(cls, value, diff: float):
        return super().__new__(cls, value)

    def __init__(self, value: float, diff: float):
        float.__init__(value)
        self.value = value
        self.diff = diff

    def __eq__(self, other):
        try:
            other = float(other)
        except ValueError:
            return NotImplemented
        return self.value - self.diff <= other <= self.value + self.diff

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"~{self.value}(±{self.diff})"


class ApproximatelyDateEqual(pendulum.DateTime, AnyEqualMixin):
    def __new__(cls, value: pendulum.DateTime, diff_minutes: int):
        return super().__new__(
            cls,
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second,
            microsecond=value.microsecond,
            tzinfo=value.tzinfo,
            fold=value.fold,
        )

    def __init__(self, value: pendulum.DateTime, diff_minutes: int):
        self.value = value
        self.diff_minutes = diff_minutes

    def __eq__(self, other):
        try:
            value = pendulum.instance(self.value)
            other = pendulum.instance(other)
        except ValueError:
            return NotImplemented
        return value.subtract(minutes=self.diff_minutes) <= other <= value.add(minutes=self.diff_minutes)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"~{self.value} (±{self.diff_minutes} minutes)"


class ApproximatelyTimestampEqual(float, AnyEqualMixin):
    def __new__(cls, value, diff_minutes: int = 0, diff_seconds: int = 0):
        return super().__new__(cls, value)

    def __init__(
        self,
        value: float | ApproximatelyTimestampEqual,
        diff_minutes: int = 0,
        diff_seconds: int = 0,
    ):
        int.__init__(value)
        self.value = pendulum.from_timestamp(value)
        self.diff_minutes = diff_minutes
        self.diff_seconds = diff_seconds

    def __eq__(self, other):
        try:
            other = pendulum.from_timestamp(other)
        except ValueError:
            return NotImplemented
        return (
            self.value.subtract(minutes=self.diff_minutes, seconds=self.diff_seconds)
            <= other
            <= self.value.add(minutes=self.diff_minutes, seconds=self.diff_seconds)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"~{self.value} (±{self.diff_minutes} minutes ±{self.diff_seconds} seconds)"


class BCryptPasswordEqual(str, AnyEqualMixin):
    def __eq__(self, other: str):
        password = self.encode("UTF-8")
        previous_hash = other.encode("UTF-8")
        return bcrypt.checkpw(password, previous_hash)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"bcrypt({self})"


class AnyStringEqual(str, AnyEqualMixin):
    def __eq__(self, other):
        return isinstance(other, str)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "AnyString"


class RegexEqual(str, AnyEqualMixin):
    def __init__(self, regex: str):
        self.regex = regex

    def __eq__(self, other):
        return bool(re.fullmatch(self.regex, other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Equal regex: {self.regex}"


class AnyIntegerEqual(int, AnyEqualMixin):
    def __eq__(self, other):
        return isinstance(other, int)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "AnyInteger"


class AnyFloatEqual(float, AnyEqualMixin):
    def __eq__(self, other):
        return isinstance(other, float)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "AnyFloat"


class IntegerGreaterThan(int, AnyEqualMixin):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, int) and other > self

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Integer greater than {self.value}"


class IntegerLessThan(int, AnyEqualMixin):
    def __init__(self, value: int):
        int.__init__(value)
        self.value = value

    def __eq__(self, other):
        return isinstance(other, int) and other < self

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Integer less than {self.value}"


class OneOfStringsEqual(str, AnyEqualMixin):
    def __init__(self, possible_values: List[str]):
        self.possible_values = possible_values

    def __eq__(self, other):
        return other in self.possible_values

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"One of {self.possible_values}"


class CompareDiff(BaseModel):
    field_name: str
    real: Any
    expected: Any
    message: str


class Comparator:
    def __init__(self):
        self.errors: Dict[str, List[CompareDiff]] = defaultdict(list)

    def _compare_unknown(self, real: Any, expected: Any, field_name: str, parent):
        if not self.compare_types(real, expected, field_name, parent):
            return

        if isinstance(expected, BaseModel):
            self.compare_pydantic_models(
                real, expected, field_name, parent=f"{parent}.{expected.model_json_schema()['title']}"
            )
        elif isinstance(expected, list):
            self.compare_lists(real, expected, field_name, parent)
        elif isinstance(expected, float) and not isinstance(expected, AnyEqualMixin):
            self.compare_float(real, expected, field_name, parent)
        else:
            self.compare_other(real, expected, field_name, parent)

    def compare_other(self, real: Any, expected: Any, field_name: str, parent: str):
        if real != expected:
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=real,
                    expected=expected,
                    message=f"{field_name}: Objects doesn't match. Real: {real}. Expected: {expected}",
                )
            )

    def compare_float(self, real: float, expected: float, field_name: str, parent: str):
        if not math.isclose(real, expected):
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=real,
                    expected=expected,
                    message=f"{field_name}: Float value doesn't close enough. Real: {real}. Expected: {expected}",
                )
            )

    def compare_types(self, real: Any, expected: Any, field_name: str, parent) -> bool:
        if isinstance(expected, AnyEqualMixin) or isinstance(real, AnyEqualMixin):
            return True
        real_type, expected_type = type(real), type(expected)
        if real_type != expected_type:
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=real,
                    expected=expected,
                    message=f"{field_name}: Types doesn't match. Real: {real_type}. Expected: {expected_type}",
                )
            )
        return real_type == expected_type

    def compare_lists(self, real: list, expected: list, field_name: str, parent="root"):
        real_len, expected_len = len(real), len(expected)
        if real_len != expected_len:
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=real,
                    expected=expected,
                    message=f"{field_name}: Len of arrays don't match: Real: {real_len}. Expected: {expected_len}",
                )
            )
        try:
            real, expected = sorted(real), sorted(expected)
        except TypeError:
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=None,
                    expected=None,
                    message=f"{field_name}: List doesn't support sorting. Compare hole objects",
                )
            )
            self.compare_other(real, expected, field_name, parent)
            return

        for i, (real_item, expected_item) in enumerate(zip(real, expected)):
            self._compare_unknown(real_item, expected_item, f"{field_name}[{i}]", f"{parent}.{field_name}[{i}]")

    def compare_pydantic_models(self, real, expected, field_name="root", parent="root"):
        if not type(real) is type(expected):
            self.errors[parent].append(
                CompareDiff(
                    field_name=field_name,
                    real=None,
                    expected=None,
                    message=f"{field_name}: Models to be compared must be instances of the same class.",
                )
            )

        for field_name, field_params in expected.schema(by_alias=False)["properties"].items():
            real_field_value = getattr(real, field_name)
            expected_field_value = getattr(expected, field_name)

            self._compare_unknown(real_field_value, expected_field_value, field_name, parent)

    def create_error_message(self):
        result = ""
        if not self.errors:
            return None
        current_parent = None
        for parent, errors in self.errors.items():
            for error in errors:
                if parent != current_parent:
                    result += "    " * (len(parent.split(".")) - 1) + parent + "\r\n"
                result += "    " * len(parent.split(".")) + error.message + "\r\n"
                current_parent = parent
        return result


def compare_pydantic_models(real: BaseModel, expected: BaseModel):
    comparator = Comparator()
    comparator.compare_pydantic_models(real, expected)
    error_message = comparator.create_error_message()
    if error_message:
        error_message += f"""
        Real:
            {real.model_dump_json()}
        Expected:
            {expected.model_dump_json()}
        """
        raise AssertionError(error_message)


def compare_pydantic_models_without_raise(real: BaseModel, expected: BaseModel):
    comparator = Comparator()
    comparator.compare_pydantic_models(real, expected)
    return comparator.create_error_message()


def compare_lists(real: list, expected: list):
    comparator = Comparator()
    comparator.compare_lists(real, expected, "root")
    error_message = comparator.create_error_message()
    if error_message:
        error_message += f"""
        Real:
            {real}
        Expected:
            {expected}
        """
        raise AssertionError(error_message)


def compare_lists_of_models(real: List[BaseModel], expected: List[BaseModel]):
    comparator = Comparator()
    comparator.compare_lists(real, expected, "root")
    error_message = comparator.create_error_message()
    if error_message:
        error_message += f"""
        Real:
            {[item.model_dump_json() for item in real]}
        Expected:
            {[item.model_dump_json() for item in expected]}
        """
        raise AssertionError(error_message)
