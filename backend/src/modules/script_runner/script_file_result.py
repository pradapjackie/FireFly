import csv
from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict, List

from pydantic import BaseModel

from src.clients.minio_client.minio_client import MinioClient
from src.schemas.script_runner.script_history import (
    ScriptFileExtension,
    ScriptFileResult,
    ScriptResult,
    ScriptResultTypeEnum,
)


class FileResult(ABC):
    def __init__(self, file_name: str, extension: ScriptFileExtension):
        self.file_name = file_name
        self.extension = extension
        self.file_url: str | None = None

    @abstractmethod
    def _get_file_as_bytes(self) -> bytes:
        pass

    async def _upload_file(self, file_bytes: bytes) -> str:
        async with MinioClient() as minio_client:
            return await minio_client.upload_file(file_bytes, extension=f".{self.extension}", file_name=self.file_name)

    async def get_script_result(self) -> ScriptResult:
        if not self.file_url:
            file_bytes = self._get_file_as_bytes()
            self.file_url = await self._upload_file(file_bytes)
        return ScriptResult(
            type=ScriptResultTypeEnum.file,
            object=ScriptFileResult(title=self.file_name, type=self.extension, url=self.file_url),
        )


class CsvResult(FileResult):
    def __init__(self, models: List[BaseModel | Dict], file_name: str):
        super().__init__(file_name, ScriptFileExtension.csv)
        self.models = models

    def _get_file_as_bytes(self) -> bytes:
        if not self.models:
            return b""

        if isinstance(self.models[0], BaseModel):
            fields = self.models[0].model_dump(by_alias=True).keys()
        elif isinstance(self.models[0], dict):
            fields = set().union(*[set(i.keys()) for i in self.models])
        else:
            raise ValueError(f"CsvResult accept only List[BaseModel | Dict], not: {type(self.models)}")

        csv_buffer = StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=fields)
        writer.writeheader()

        if isinstance(self.models[0], BaseModel):
            for model in self.models:
                writer.writerow(model.model_dump(by_alias=True))
        elif isinstance(self.models[0], dict):
            for model in self.models:
                writer.writerow(model)
        else:
            raise ValueError(f"CsvResult accept only List[BaseModel | Dict], not: {type(self.models)}")

        csv_content = csv_buffer.getvalue()
        csv_buffer.close()
        return csv_content.encode("utf-8")
