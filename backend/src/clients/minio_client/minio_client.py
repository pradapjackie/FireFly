import asyncio
import json
from datetime import datetime
from typing import AsyncIterator, List, Optional, Tuple, cast
from xml.etree import ElementTree

import aiohttp
from async_lru import alru_cache
from minio.credentials import Credentials
from minio.helpers import md5sum_hash
from minio.signer import sign_v4_s3
from minio.time import to_amz_date, utcnow
from minio.xml import Element, SubElement, getbytes
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from yarl import URL

from src.clients.http_client.client import HttpClient
from src.core.config import settings


class MinioURL(BaseModel):
    path: str
    query: str


class Part(BaseModel):
    id: int
    e_tag: str


def get_read_only_policy(bucket_name: str) -> str:
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                }
            ],
        }
    )


class MinioClient(HttpClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, connector=aiohttp.TCPConnector(ssl=False))
        self.base_url = URL(settings.MINIO_HOST)
        self.base_public_url = URL(settings.MINIO_PUBLIC_HOST) if settings.MINIO_PUBLIC_HOST else self.base_url
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.region = "us-east-1"
        self.credentials = Credentials(access_key=settings.MINIO_ACCESS_KEY, secret_key=settings.MINIO_SECRET_KEY)
        self.min_chunk_size = 1024 * 1024 * 5

    @staticmethod
    def _get_unique_file_name(extension_with_dot: str, file_name: str = "") -> str:
        current_ts = int(datetime.now().timestamp())
        return f"{file_name.replace(' ', '_').lower()}_{current_ts}{extension_with_dot}"

    def _get_headers(self, method: str, url: URL, query_string: str = "", content_type: Optional[str] = None) -> dict:
        now = utcnow()
        sha256 = "UNSIGNED-PAYLOAD"
        headers = {"Host": url.host, "x-amz-content-sha256": sha256, "x-amz-date": to_amz_date(now)}
        if content_type:
            headers["Content-Type"] = content_type
        return sign_v4_s3(
            method=method,
            url=MinioURL(path=url.path, query=query_string),
            region=self.region,
            headers=headers,
            credentials=self.credentials,
            content_sha256=sha256,
            date=now,
        )

    @alru_cache()
    async def _check_bucket_exist(self) -> bool:
        url = self.base_url / self.bucket_name
        async with self.http_session.head(url=url, headers=self._get_headers("HEAD", url)) as resp:
            return resp.status == 200

    async def _create_bucket(self):
        url = self.base_url / self.bucket_name
        async with self.http_session.put(url=url, data=None, headers=self._get_headers("PUT", url)) as resp:
            assert resp.status == 200

    async def _make_bucket_public(self):
        url = self.base_url / self.bucket_name
        policy = get_read_only_policy(self.bucket_name)
        headers = self._get_headers("PUT", url, "policy=") | {"Content-MD5": cast(str, md5sum_hash(policy))}
        async with self.http_session.put(
            url=url,
            params={"policy": ""},
            data=policy.encode(),
            headers=headers,
        ) as resp:
            assert resp.status == 204

    async def ensure_bucket(self):
        if not await self._check_bucket_exist():
            await self._create_bucket()
            await self._make_bucket_public()

    @retry(
        retry=retry_if_exception_type((asyncio.TimeoutError, RuntimeError)),
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        before_sleep=lambda retry_state: print(f"Retry Save to Minio: {retry_state.outcome.exception()}", flush=True),
        reraise=True,
    )
    async def upload_file(self, file_to_upload: bytes, extension: str, file_name: str = "") -> str:
        await self.ensure_bucket()
        filename = self._get_unique_file_name(extension, file_name)
        url = self.base_url / self.bucket_name / filename
        headers = self._get_headers("PUT", url)
        async with self.http_session.put(url=url, data=file_to_upload, headers=headers) as resp:
            if resp.status != 200:
                response = await resp.read()
                raise RuntimeError(f"Minio returns unsuccessful status code: {resp.status}. Response: {response}")
            return str(self.base_public_url / self.bucket_name / filename)

    async def _start_file_part_upload(self, url: URL) -> str:
        url = url.with_query({"uploads": ""})
        headers = self._get_headers("POST", url, content_type="application/octet-stream")
        async with self.http_session.post(url=url, headers=headers) as resp:
            response = await resp.read()
            element = ElementTree.fromstring(response.decode())
            return [item.text for item in element if "UploadId" in item.tag][0]

    async def _complete_multipart_upload(self, url: URL, upload_id: str, parts: List[Part]):
        element = Element("CompleteMultipartUpload")
        for part in parts:
            tag = SubElement(element, "Part")
            SubElement(tag, "PartNumber", str(part.id))
            SubElement(tag, "ETag", '"' + part.e_tag + '"')
        data = getbytes(element)
        url = url.with_query({"uploadId": upload_id})
        headers = self._get_headers("POST", url, content_type="application/xml")
        await self.http_session.post(url=url, data=data, headers=headers)

    async def _upload_part(self, url: URL, upload_id: str, part_id: int, data: bytes) -> Part:
        url = url.with_query({"partNumber": part_id, "uploadId": upload_id})
        headers = self._get_headers("PUT", url, content_type="application/octet-stream")
        async with self.http_session.put(url=url, data=data, headers=headers) as resp:
            return Part(id=part_id, e_tag=resp.headers.get("Etag"))

    async def upload_parts(self, stream: AsyncIterator[Tuple[bytes, bool]], extension: str) -> str:
        await self.ensure_bucket()
        url = self.base_url / self.bucket_name / self._get_unique_file_name(extension)
        upload_id = await self._start_file_part_upload(url)
        part_id, buffer, parts = 1, b"", []
        async for data, end in stream:
            buffer += data
            if len(buffer) > self.min_chunk_size or end:
                parts.append(await self._upload_part(url, upload_id, part_id, buffer))
                part_id += 1
                buffer = b""
        await self._complete_multipart_upload(url, upload_id, parts)
        return str(url)
