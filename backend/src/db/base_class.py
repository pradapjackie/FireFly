import re
from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr

table_name_replace_pattern = re.compile("(?<=[a-z])([A-Z])")


@as_declarative()
class Base:
    id: Any
    __name__: str

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(table_name_replace_pattern, r"_\1", cls.__name__).lower()
