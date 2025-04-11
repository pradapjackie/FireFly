from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from src.db.base_class import Base


class ScriptHistory(Base):
    id = Column(
        String(132),
        primary_key=True,
        index=True,
        unique=True,
        comment="UUID of script execution",
    )
    script_id = Column(String(132), ForeignKey("script.id"))
    params = Column(JSON, nullable=False, comment="Script launch parameter values")
    status = Column(String(50), nullable=False, comment="Script execution final status")
    root_folder = Column(String(100), nullable=False, comment="The root folder to which the script belongs")
    environment = Column(String(50), nullable=False, comment="Environment on which the script was executed")
    env_used = Column(JSON, nullable=False, comment="Environment variables used during script execution")
    result_type = Column(String(50), nullable=True, comment="Type of result of a successfully executed script")
    result = Column(JSON, nullable=True, comment="Result of a successfully executed script")
    errors = Column(JSON, nullable=True, comment="Script execution errors")
    user_id = Column(Integer, ForeignKey("user.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
