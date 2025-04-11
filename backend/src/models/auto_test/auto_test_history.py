from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String

from src.db.base_class import Base
from src.schemas.auto_test.auto_test_history import StatusEnum


class AutoTestHistory(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    test_id = Column(String(132), ForeignKey("auto_test.id"))
    test_run_id = Column(String(36), ForeignKey("test_run_history.id"))
    run_config = Column(JSON, nullable=False, comment="The configuration set on autotest run")
    groups = Column(JSON, nullable=False, comment="Auto test history groups")
    status = Column(Enum(StatusEnum), nullable=False, comment="Autotest final status")
    stages = Column(JSON, nullable=False, comment="Json with autotest stages and steps data")
    env_used = Column(JSON, nullable=False, comment="Environment variables used during test")
    warnings = Column(JSON, comment="Warnings that occurred during the test")
    assets_path = Column(JSON, nullable=False, comment="Path to autotest assets directory")
    generated_params = Column(JSON, nullable=False, comment="Variables generated during test")
    errors = Column(JSON, nullable=True, comment="Autotest errors")
