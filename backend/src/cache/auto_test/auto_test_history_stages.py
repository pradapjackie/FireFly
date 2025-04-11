from src.cache.base import CacheBase
from src.schemas.auto_test.auto_test_history import AutoTestStages, StageResult


class AutoTestHistoryStagesCache(CacheBase[StageResult, StageResult]):
    def __init__(self, run_id: str):
        self.run_id = run_id
        super().__init__(StageResult)

    async def create_multi(self, test_id: str, data: AutoTestStages):
        data = {k: self.converter.encode_to_str(data) for k, v in data.model_dump().items()}
        await self._save_dict(f"{self.run_id}:autotest:{test_id}:stages", data)

    async def update(self, test_id: str, stage_name: str, data: StageResult):
        data = self.converter.encode_to_str(data)
        await self._update_key_value_in_dict(f"{self.run_id}:autotest:{test_id}:stages", stage_name, data)

    async def get(self, test_id: str, stage_name: str) -> StageResult:
        return await self._get_key_value_from_dict(f"{self.run_id}:autotest:{test_id}:stages", stage_name)

    async def get_all(self, test_id: str) -> AutoTestStages:
        result = await self._get_dict(f"{self.run_id}:autotest:{test_id}:stages")
        data = {k.decode("UTF-8"): self.converter.decode_from_bytes(v) for k, v in result.items()}
        return AutoTestStages(**data)
