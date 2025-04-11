from sqlalchemy import JSON, Column, DateTime, String, Text
from sqlalchemy.sql import text

from src.db.base_class import Base


class LoadTest(Base):
    id = Column(
        String(132),
        primary_key=True,
        index=True,
        unique=True,
        comment="load test name plus md5(load test params)",
    )
    name = Column(String(100), nullable=False, comment="Load Test real code name")
    display_name = Column(String(100), nullable=False, comment="Load Test display name")
    description = Column(Text, comment="Load Test description")
    root_folder = Column(String(100), nullable=False, comment="The root folder to which the load test belongs")
    filepath = Column(String(500), nullable=False, comment="Load Test full path in code base")
    params = Column(JSON, nullable=False, comment="Load Test launch parameters")
    charts = Column(JSON, nullable=False, comment="Charts config that load test produces")
    config = Column(JSON, nullable=False, comment="Load test execution config")
    supported_from = Column(
        String(10), nullable=False, comment="Code version from which (inclusive) this load test is supported."
    )
    supported_to = Column(
        String(10), nullable=False, comment="Code version to which (inclusive) this load test is supported."
    )
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
