from collections.abc import MutableMapping


def _flatten_dict_gen(d: MutableMapping, sep: str, parent_key: str = ""):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from _flatten_dict_gen(v, sep, new_key)
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, sep: str = "."):
    return dict(_flatten_dict_gen(d, sep))
