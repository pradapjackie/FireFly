from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import DATETIME

from src.db.base_class import Base
from src.schemas.auto_test.test_run import TestRunStatus


class TestRunHistory(Base):
    id = Column(String(36), primary_key=True, index=True, unique=True, comment="Test run UUIDv4")
    status = Column(Enum(TestRunStatus), nullable=False, comment="Test run status")
    user_id = Column(Integer, ForeignKey("user.id"))
    version = Column(String(10), nullable=False, comment="Code version to which this test run belongs to")
    root_folder = Column(String(100), nullable=False, comment="The root folder to which the test run belongs")
    environment = Column(String(50), nullable=False, comment="Environment on which the test run was executed")
    run_config = Column(JSON, nullable=False, comment="The configuration set of test run")
    result_by_status = Column(JSON, nullable=False, comment="Test statuses by groups")
    error = Column(JSON, comment="Test run error. Can be null")
    start_time = Column(DATETIME, nullable=False)
    group_ids = Column(JSON, nullable=False, comment="Test run groups")
