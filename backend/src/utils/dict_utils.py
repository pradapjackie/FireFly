from collections import defaultdict
from typing import Any, Dict, List, Tuple, TypeVar

Key = TypeVar("Key")
Value = TypeVar("Value")


def reverse(value: Dict[Key, Value]) -> Dict[Value, List[Key]]:
    result = defaultdict(list)
    for k, v in sorted(value.items()):
        result[v].append(k)
    return dict(result)


def dict_from_list(values: List[Value], key_name: str) -> Dict[Any, List[Value]]:
    result = defaultdict(list)
    for item in sorted(values):
        result[getattr(item, key_name)].append(item)
    return result


def merge_dicts(list_of_dicts: List[Dict[Key, Value]] | Tuple[Dict[Key, Value]]) -> Dict[Key, Value]:
    return {k: v for d in list_of_dicts for k, v in d.items()}
