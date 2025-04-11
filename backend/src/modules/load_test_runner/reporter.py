from typing import Dict, Type

from pendulum import now

from src.cache.load_test.current import LoadTestCurrentCache
from src.cache.load_test.report import LoadTestReportCache
from src.cache.load_test.tasks import LoadTestTaskCache
from src.cache.load_test.workers import LoadTestWorkerCache
from src.models import User
from src.modules.load_test_runner.charts.base import BaseChart
from src.modules.load_test_runner.charts.boxplot import BoxPlot
from src.schemas.load_test.load_test import StartLoadTestRequest
from src.schemas.load_test.load_test_history import LoadTestHistory, LoadTestHistoryFull

chart_classes: Dict[str, Type[BaseChart]] = {"BoxPlot": BoxPlot}


class LoadTestReporter:
    def __init__(self, load_test_id: str):
        self.load_test_id = load_test_id
        self.report_cache = LoadTestReportCache(load_test_id)
        self.current_execution_cache = LoadTestCurrentCache()

    async def start_report(self, execution_id: str, user: User, start_request: StartLoadTestRequest):
        new_script_history = LoadTestHistory(
            execution_id=execution_id,
            load_test_id=self.load_test_id,
            params=start_request.params,
            config_values=start_request.config_values,
            chart_config=start_request.chart_config,
            number_of_tasks=start_request.number_of_tasks,
            user_id=user.id,
            root_folder=start_request.root_folder,
            env_name=start_request.env_name,
            setting_overwrite=start_request.setting_overwrite,
            start_time=now(tz="UTC"),
        )
        await self.report_cache.create(execution_id, new_script_history)
        await self.current_execution_cache.save(self.load_test_id, execution_id)

    async def get_history(self, execution_id: str) -> LoadTestHistoryFull:
        load_test_history = await self.report_cache.get(execution_id)
        workers = await LoadTestWorkerCache(self.load_test_id, execution_id).get_all()
        task_status_history = await LoadTestTaskCache(self.load_test_id, execution_id).get_status_history()
        charts_data = {}
        for chart_name, chart_type in load_test_history.chart_config.items():
            if chart_class := chart_classes.get(chart_type, None):
                charts_data[chart_name] = await chart_class().get_chart_data(
                    load_test_id=load_test_history.load_test_id, execution_id=execution_id, chart_name=chart_name
                )
        return LoadTestHistoryFull(
            **load_test_history.model_dump(),
            workers=workers,
            task_status_history=task_status_history,
            charts=charts_data,
        )

    async def get_last_history(self) -> LoadTestHistoryFull | None:
        if last_execution_id := await self.current_execution_cache.get(self.load_test_id):
            return await self.get_history(last_execution_id)
