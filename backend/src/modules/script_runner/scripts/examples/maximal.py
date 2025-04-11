import asyncio
from datetime import date
from enum import StrEnum
from io import BytesIO
from typing import Dict, List

import pendulum
from pydantic import BaseModel

from src.modules.environment.env import env
from src.modules.script_runner.register import register
from src.modules.script_runner.script_file_result import CsvResult
from src.modules.script_runner.script_logger import log


class MyEnum(StrEnum):
    a = "a"
    b = "b"


@register
async def maximal_script(
    some_float: float,
    some_str_enum: MyEnum,
    some_date_one: date,
    some_file: BytesIO,
    some_date_two: pendulum.Date = pendulum.Date(year=2023, month=11, day=11),
    some_string: str = "test",
    some_int: int = 10,
    some_bool: bool = True,
) -> List[Dict]:
    """
    My Script description
    """

    # The values entered by the user are simply available in the script
    await log(some_string, some_int, some_float, some_bool, some_str_enum, some_date_one, some_date_two)

    # Certain values may differ from environment to environment: application and database URLs, passwords, ...
    # Such variables need to be stored in the environment. They can be easily changed through the UI
    await log(env.test_env_variable)

    for i in range(10):
        # To add a log line to the UI, use the log() method
        await log(i)
        await asyncio.sleep(0.2)

    # The script can return any result that can be cast to a string.
    # The framework will try to display it as user-friendly as possible.
    return [
        {"result": "I am result", "additional": "More info", "some data": 1},
        {"result": "I am second result", "additional": "More second info", "some data": 2},
    ]


async def test_func(some_id: int):
    if some_id == 2 or some_id == 3 or some_id == 55:
        raise ValueError(f"I don't like id: {some_id}")
    else:
        return {"Test3": f"{some_id}", "Test4": f"{some_id}{some_id}"}


@register
async def async_generator_script():
    # The script can be an asynchronous generator and return multiple results!
    yield await asyncio.gather(*[test_func(i) for i in [11, 22, 55]], return_exceptions=True)

    await asyncio.sleep(2)

    # Any script can return an array of results interspersed with exceptions
    # This will be beautifully displayed on the frontend!
    yield await asyncio.gather(*[test_func(i) for i in range(5)], return_exceptions=True)

    await asyncio.sleep(2)

    # You can also automatically create csv files from lists and return them from script!
    class Test(BaseModel):
        first: str
        second: str

    test_data = [Test(first="one", second="two"), Test(first="three", second="four")]
    test_data2 = [Test(first="one2", second="two2"), Test(first="three2", second="four2")]
    yield [CsvResult(test_data, file_name="Combined result"), CsvResult(test_data2, file_name="Combined result 2")]
