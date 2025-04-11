from itertools import product
from typing import List, Optional, Type

from src.modules.auto_test.test_abs import TestAbs


def register(tags: Optional[List[str]] = None):
    def inner(cls: Type[TestAbs]) -> Type[TestAbs]:
        cls.tags = tags
        return cls

    return inner


class Parametrized:
    def __init__(self, iterations):
        self.iterations = list(iterations)

    def __call__(self, func):
        func.iterations = self.iterations
        return func


def params(iterations):
    return Parametrized(iterations)


def params_product(**iteration_template):
    return Parametrized(create_params_product(**iteration_template))


def run_in_separate_thread(func):
    """
    Schedule autotest to run in a separate thread.
    Useful for time sensitive tests (checking timers, animations, etc.)
    It's not possible (due to GIL) to guarantee continuous execution of test in separate thread,
    but so far there are few such tests - this allows us to reduce the number and time of interruptions.
    In tests run in a separate thread, you can NOT use futures created in group setup
    (like open database or network connection)
    """
    func.run_in_separate_thread = True
    return func


def create_params_product(**iteration_template):
    iteration_name: str = iteration_template.pop("iteration_name")
    result = []
    for iteration in product(*iteration_template.values()):
        iteration = dict(zip(iteration_template.keys(), iteration))
        result.append(dict(iteration_name=iteration_name.format_map(iteration), **iteration))
    return result
