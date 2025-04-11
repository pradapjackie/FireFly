import asyncio
from typing import AsyncIterator, Optional, Tuple

from src.clients.minio_client.minio_client import MinioClient
from src.modules.auto_test.contexts import auto_test_context
from src.modules.auto_test.reporter import Reporter
from src.schemas.auto_test.auto_test import Asset, AssetTypeEnum
from src.schemas.auto_test.auto_test_history import AutoTestHistoryUpdate


class AssetsHelper:
    def __init__(self, run_id: Optional[str] = None, auto_test_id: Optional[str] = None):
        self.minio_client = MinioClient()
        self.run_id = run_id
        self.auto_test_id = auto_test_id
        self.lock = asyncio.Lock()

    async def _add_asset_path(self, asset: Asset):
        if auto_test_context and auto_test_context.get(None):
            auto_test_context.get().assets_path[asset.title] = asset
        else:
            if None in (self.run_id, self.auto_test_id):
                raise RuntimeError(
                    "The autotest has already been completed. Specify run and test IDs to update after finish."
                )
            reporter = Reporter(self.run_id)
            async with self.lock:
                history = await reporter.auto_test_history_cache.get(self.auto_test_id)
                history_assets = history.assets_path
                history_assets[asset.title] = asset
                await reporter.update_test_report_after_finish(
                    self.run_id, self.auto_test_id, AutoTestHistoryUpdate(assets_path=history_assets)
                )

    async def add_video(self, title: str, video_stream: AsyncIterator[Tuple[bytes, bool]]):
        video_url = await self.minio_client.upload_parts(video_stream, extension=".mp4")
        await self._add_asset_path(Asset(type=AssetTypeEnum.video, title=title, url=video_url))

    async def add_image(self, title: str, image_bytes: Optional[bytes]):
        image_url = await self.minio_client.upload_file(image_bytes, extension=".png")
        await self._add_asset_path(Asset(type=AssetTypeEnum.image, title=title, url=image_url))

    async def add_text(self, title: str, text_bytes: Optional[bytes]):
        text_url = await self.minio_client.upload_file(text_bytes, extension=".txt")
        await self._add_asset_path(Asset(type=AssetTypeEnum.text, title=title, url=text_url))

    async def close_connection(self):
        await self.minio_client.close()
