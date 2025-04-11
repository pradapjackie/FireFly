import datetime
from typing import Annotated, List

import pendulum
from pydantic import WithJsonSchema

PendulumDateTime = Annotated[pendulum.DateTime, WithJsonSchema({"type": "datetime"})]


def datetime_from_date(date: pendulum.Date) -> pendulum.DateTime:
    return pendulum.DateTime(year=date.year, month=date.month, day=date.day)


def datetime_from_raw_date(date: datetime.date) -> pendulum.DateTime:
    return pendulum.DateTime(year=date.year, month=date.month, day=date.day)


def date_from_raw_date(date: datetime.date) -> pendulum.Date:
    return pendulum.Date(year=date.year, month=date.month, day=date.day)


def date_from_formats(date_str: str, formats: List[str]) -> pendulum.DateTime:
    for fmt in formats:
        try:
            return pendulum.from_format(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"The string '{date_str}' does not match any of the provided date formats: {formats}")
