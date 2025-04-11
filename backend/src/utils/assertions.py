from typing import Iterable, Optional, Pattern, Union

from src.modules.auto_test.step_manager import step


def assert_all_items_exist_in_string(item_list: Iterable[Union[Pattern, str]], string: str):
    check_list = []
    for item in item_list:
        if isinstance(item, Pattern):
            check_list.append(item.search(string))
        if isinstance(item, str):
            check_list.append(item if item in string else False)

    if not all(check_list):
        error_massage = f"""
            The following items:
            {[item for item, check in zip(item_list, check_list) if not check]}
            are not in given string: {string}
            """
        raise AssertionError(error_massage)


def assert_strings(name, real: str, expected: str):
    assert real == expected, f"We expect '{name}' will be equal to: {expected}, but the real value is: {real}"


async def assert_status_code(real: int, expected: int, error_details: Optional[str] = ""):
    async with step(f"Assert status code must be {expected}"):
        assert real == expected, f"Response status code {real} does not match the expected {expected}. {error_details}"


def assert_one_element(list_of_items: list, item_name: str):
    length = len(list_of_items)
    if length == 0:
        raise AssertionError(f"No matching '{item_name}' were found in the resulting list")
    if length > 1:
        raise AssertionError(f"More than one matching '{item_name}' were found in the resulting list")
