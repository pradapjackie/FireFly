import re

class_name_replace_pattern = re.compile(r"(?<![A-Z]\s)(?<!^)([A-Z])")
method_name_replace_pattern = re.compile(r"(test_|_test)")


def format_method_name(test_name: str) -> str:
    test_name = method_name_replace_pattern.sub("", test_name)
    return test_name.replace("_", " ").title()


def format_class_name(class_name: str) -> str:
    return class_name_replace_pattern.sub(r" \1", class_name)


def format_class_or_method_name(name: str) -> str:
    name = name.replace("_", " ")
    return class_name_replace_pattern.sub(r" \1", name).title()


def snake_to_camel(s: str) -> str:
    return "".join(word[0].upper() + word[1:] if i != 0 else word for i, word in enumerate(s.split("_")))


def snake_to_pascal(s: str) -> str:
    return "".join(word[0].upper() + word[1:] for i, word in enumerate(s.split("_")))


def camel_to_snake(s: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")
