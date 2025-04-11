from sqlalchemy import JSON, Column, DateTime, String, Text
from sqlalchemy.sql import text

from src.db.base_class import Base


class Script(Base):
    id = Column(
        String(132),
        primary_key=True,
        index=True,
        unique=True,
        comment="script_name plus md5(script params)",
    )
    name = Column(String(100), nullable=False, comment="Script real code name")
    display_name = Column(String(100), nullable=False, comment="Script display name")
    description = Column(Text, comment="Script description")
    root_folder = Column(String(100), nullable=False, comment="The root folder to which the script belongs")
    filepath = Column(String(500), nullable=False, comment="Script full path in code base")
    params = Column(JSON, nullable=False, comment="Script launch parameters")
    supported_from = Column(
        String(10), nullable=False, comment="Code version from which (inclusive) this script is supported."
    )
    supported_to = Column(
        String(10), nullable=False, comment="Code version to which (inclusive) this script is supported."
    )
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
