from sqlalchemy import Boolean, Column, Integer, String

from src.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True, unique=True, nullable=False)
    full_name = Column(String(50), index=True, unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    disabled = Column(Boolean(), default=False)
