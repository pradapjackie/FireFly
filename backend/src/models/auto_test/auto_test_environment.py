from sqlalchemy import Boolean, Column, Integer, String, Text, UniqueConstraint

from src.db.base_class import Base


class AutoTestEnvironment(Base):
    id = Column(Integer, primary_key=True, index=True)
    param = Column(String(100), nullable=False)
    env = Column(String(50), nullable=False)
    value = Column(Text)
    secure = Column(Boolean, default=False, comment="Values of secure params are not saved to the database.")
    __table_args__ = (UniqueConstraint("param", "env", name="parameter_for_particular_env"),)
