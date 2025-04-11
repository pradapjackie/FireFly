import json
from typing import Dict, List, NamedTuple

import pendulum

from src.modules.load_test_runner.charts.base import BaseChart

ChartBox = NamedTuple("ChartBox", [("min", int), ("q1", int), ("median", int), ("q3", int), ("max", int)])


class BoxPlot(BaseChart):
    @staticmethod
    def median(nums: List[int | float]) -> int | float:
        n = len(nums)
        if n % 2 == 0:
            return (nums[n // 2 - 1] + nums[n // 2]) / 2
        else:
            return nums[n // 2]

    def calculate_quartiles(self, data: List[int | float]) -> ChartBox:
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 1:
            return ChartBox(data[0], data[0], data[0], data[0], data[0])
        return ChartBox(
            min=min(sorted_data),
            q1=self.median(sorted_data[: n // 2]),
            median=self.median(sorted_data),
            q3=self.median(sorted_data[(n + 1) // 2 :]),
            max=max(sorted_data),
        )

    async def update_box(self, value: int | float):
        prefix = f"load_test:{self._get_load_test_id()}:{self._get_execution_id()}:charts:{self.name}"
        now_time = pendulum.now("UTC").format("YYYY-MM-DD HH:mm")
        await self._add_to_list(f"{prefix}:data:{now_time}", value)
        current_data = await self._get_list(f"{prefix}:data:{now_time}") or []
        box_data = self.calculate_quartiles([float(x) for x in current_data])
        await self._update_key_value_in_dict(f"{prefix}:current", now_time, json.dumps(box_data))
        await self.send_update([now_time, *box_data])

    async def get_chart_data(self, load_test_id: str, execution_id: str, chart_name: str) -> Dict[str, List[int]]:
        data = await self._get_decoded_dict(f"load_test:{load_test_id}:{execution_id}:charts:{chart_name}:current")
        return {key: json.loads(value) for key, value in data.items()}
