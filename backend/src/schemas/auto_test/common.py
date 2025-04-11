from enum import IntEnum

from pydantic import BaseModel


class ResultByStatus(BaseModel):
    success: int = 0
    fail: int = 0
    pending: int = 0

    def increment(self, name):
        self.__dict__[name] += 1

    def increment_by(self, name, value):
        self.__dict__[name] += value


class TestError(BaseModel):
    name: str
    message: str
    traceback: str


class StepLevel(IntEnum):
    info = 0
    important = 1
    critical = 2
