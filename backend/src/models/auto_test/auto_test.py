from sqlalchemy import JSON, Boolean, Column, DateTime, String, Text
from sqlalchemy.sql import text

from src.db.base_class import Base


class AutoTest(Base):
    id = Column(
        String(132),
        primary_key=True,
        index=True,
        unique=True,
        comment="md5 hash from class_name, method_name, iteration_name, filepath columns",
    )
    class_name = Column(String(100), nullable=False, comment="Autotest class name")
    method_name = Column(String(100), nullable=False, comment="Autotest method name")
    iteration_name = Column(String(100), nullable=False, comment="Autotest iteration name")
    root_folder = Column(String(100), nullable=False, comment="The root folder to which the test belongs")
    filepath = Column(String(500), nullable=False, comment="Autotest full path in code base")
    params = Column(JSON, nullable=False, comment="Autotest params")
    supported_from = Column(
        String(10), nullable=False, comment="Code version from which (inclusive) this test is supported"
    )
    supported_to = Column(
        String(10), nullable=False, comment="Code version to which (inclusive) this test is supported"
    )
    is_active = Column(Boolean, default=True, comment="Is this test supported now?")
    description = Column(Text, comment="Autotest description")
    required_run_config = Column(
        JSON, nullable=True, comment="Autotest configuration that must be filled before launch this test"
    )
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
