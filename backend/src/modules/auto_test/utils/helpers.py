from typing import List

from src import models
from src.models.auto_test.auto_test import AutoTest
from src.schemas.auto_test.auto_test import (
    AutoTestDB,
    CollectedAutoTestsResponse,
    CollectedGroup,
    CollectedGroupsResponse,
    CollectedTest,
)
from src.schemas.auto_test.common import ResultByStatus


def generate_group_response(auto_tests: List[models.AutoTest], calc_result=False) -> CollectedGroupsResponse:
    result = CollectedGroupsResponse()
    group_names = set(
        (
            tuple(auto_test.filepath.split(".")) + (auto_test.class_name, auto_test.method_name)
            for auto_test in auto_tests
        )
    )
    for group_name in group_names:
        for i in range(len(group_name)):
            prev_group_id = ".".join(group_name[0:i])
            group_id = ".".join(group_name[0 : i + 1])
            result.ids.add(group_id)
            if i == 0:
                result.first_level.add(group_id)
            if group_id not in result.groups_map:
                result.groups_map[group_id] = CollectedGroup(name=group_name[i])
            if prev_group_id:
                result.groups_map[prev_group_id].groups.add(group_id)
    for auto_test in auto_tests:
        test_id = auto_test.id if type(auto_test) == AutoTest else auto_test.test_id
        auto_test_group_name = f"{auto_test.filepath}.{auto_test.class_name}.{auto_test.method_name}"
        result.groups_map[auto_test_group_name].auto_tests.add(test_id)
        if calc_result:
            for group in auto_test.groups:
                if not result.groups_map[group].result_by_status:
                    result.groups_map[group].result_by_status = ResultByStatus()
                result.groups_map[group].result_by_status.increment(auto_test.status)

    return result


def generate_collected_test_result(auto_tests: List[AutoTestDB]) -> CollectedAutoTestsResponse:
    result = CollectedAutoTestsResponse()
    for auto_test in auto_tests:
        result.ids.add(auto_test.id)
        result.auto_test_map[auto_test.id] = CollectedTest(
            id=auto_test.id, name=auto_test.iteration_name, required_run_config=auto_test.required_run_config
        )
    return result
