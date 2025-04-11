from itertools import groupby
from typing import Hashable, List, Union


def remove_duplicates(list_of_items: List[Hashable]) -> List[Union[Hashable, str]]:
    return list(dict.fromkeys(list_of_items))


def all_items_in_list_equal(iterable: List) -> bool:
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
