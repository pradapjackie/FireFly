import ast
import asyncio
import base64
import inspect
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import date
from enum import StrEnum
from importlib import util
from io import BytesIO
from pathlib import Path
from types import UnionType
from typing import Any, Callable, Dict, List, Literal, Type, TypeVar, Union, get_args, get_origin

import aiofiles
import pendulum

from src.schemas.common import CollectedObject, CollectedPath, CollectObjectTypes
from src.utils.dynamic_form import (
    AutocompleteFiled,
    AutocompleteMultiFiled,
    CheckboxFiled,
    DateField,
    Field,
    FieldTypeEnum,
    FileField,
    NumberField,
    StringField,
    StringListFiled,
)

CollectedObjectType = TypeVar("CollectedObjectType", bound=CollectedObject)

type_to_ast_map = {CollectObjectTypes.class_: ast.ClassDef, CollectObjectTypes.async_function: ast.AsyncFunctionDef}


class BaseCollector:
    @staticmethod
    async def collect_from_file(
        file_path: Path,
        acceptable_types_of_objects: List[CollectObjectTypes],
        base_class: Type | None = None,
        decorator: Callable[..., Any] | None = None,
    ) -> List[CollectedPath]:
        acceptable_ast_types = tuple([type_to_ast_map[object_type] for object_type in acceptable_types_of_objects])
        collected: List[CollectedPath] = []
        async with aiofiles.open(file_path, "r") as file:
            try:
                tree = ast.parse(await file.read(), filename=file_path)
                for node in ast.walk(tree):
                    if not isinstance(node, acceptable_ast_types):
                        continue
                    if base_class:
                        if not isinstance(node, ast.ClassDef):
                            continue
                        if not any(
                            isinstance(base, ast.Name) and base.id == base_class.__name__ for base in node.bases
                        ):
                            continue
                    if decorator:
                        if not isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef)):
                            continue
                        if not (
                            any(
                                isinstance(node, ast.Name) and node.id == decorator.__name__
                                for node in node.decorator_list
                            )
                            or any(
                                isinstance(node, ast.Call)
                                and isinstance(node.func, ast.Name)
                                and node.func.id == decorator.__name__
                                for node in node.decorator_list
                            )
                        ):
                            continue
                    collected.append(CollectedPath(name=node.name, path=file_path))
            except SyntaxError:
                print(f"The file by path {file_path} contains syntactic errors - skipped")
        return collected

    @staticmethod
    def import_from_file(
        root_path: Path, file_path: Path, object_name: str, collected_type: Type[CollectedObjectType]
    ) -> CollectedObjectType | None:
        spec = util.spec_from_file_location(file_path.name, file_path)
        module = util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"The {object_name} class from {file_path} causes an error upon import - skipped. Error: {e}")
        else:
            root_folder = file_path.relative_to(root_path).parts[0]
            return collected_type(
                name=object_name, path=file_path, root_folder=root_folder, callable=getattr(module, object_name)
            )

    @staticmethod
    def collect_root_folders(root_path: Path) -> List[str]:
        return [item.name for item in root_path.iterdir() if item.is_dir() and not item.name.startswith("__")]

    async def collect(
        self,
        root_path: Path,
        acceptable_types_of_objects: List[CollectObjectTypes],
        collected_type: Type[CollectedObjectType],
        base_class: Type | None = None,
        decorator: Callable[..., Any] | None = None,
        root_folder: str | None = None,
    ) -> List[CollectedObjectType]:
        path_iterator = root_path.glob(f"{root_folder or '*'}/**/*.py")
        result = await asyncio.gather(
            *[
                self.collect_from_file(file_path, acceptable_types_of_objects, base_class, decorator)
                for file_path in path_iterator
            ]
        )
        collected_info: List[CollectedPath] = list(itertools.chain(*result))

        with ThreadPoolExecutor(5) as executor:
            futures = [
                executor.submit(self.import_from_file, root_path, info.path, info.name, collected_type)
                for info in collected_info
            ]
            results = [future.result() for future in as_completed(futures)]

        return [result for result in results if result is not None]

    def _get_annotation_without_optional(self, callable_name: str, param: inspect.Parameter) -> Type:
        annotation = param.annotation
        if get_origin(annotation) is Union or isinstance(annotation, UnionType):
            annotation_args = [arg for arg in get_args(annotation) if arg is not type(None)]
            if len(annotation_args) == 1:
                return annotation_args[0]
            else:
                raise NotImplementedError(
                    f"Unsupported Union annotation {annotation} for param {param.name} "
                    f"of {callable_name}. Only union with None supported"
                )
        else:
            return annotation

    def signature_to_params(
        self, callable_name: str, signature_parameters: List[inspect.Parameter]
    ) -> Dict[str, Field]:
        result = {}
        for param in signature_parameters:
            label = param.name.replace("_", " ").title()
            annotation = self._get_annotation_without_optional(callable_name, param)
            default = param.default if param.default is not inspect.Signature.empty else None
            annotation_origin_type = get_origin(annotation)
            annotation_args = get_args(annotation)
            if annotation_origin_type == list and len(annotation_args) == 1:
                inner_annotation = annotation_args[0]
                if inner_annotation == str:
                    field = StringListFiled(label=label, default_value=default)
                elif inspect.isclass(inner_annotation) and issubclass(inner_annotation, StrEnum):
                    field = AutocompleteMultiFiled(
                        label=label, options=inner_annotation, default_value=default, python_type=inner_annotation
                    )
                elif get_origin(inner_annotation) == Literal:
                    field = AutocompleteMultiFiled(
                        label=label, options=get_args(inner_annotation), default_value=default, python_type=str
                    )
                else:
                    raise NotImplementedError(
                        f"Unsupported List parameter annotation {annotation} for param {param.name} "
                        f"of {callable_name}. Supported types List[str], List[StrEnum], List[Literal]"
                    )
            else:
                if annotation_origin_type == Literal:
                    field = AutocompleteFiled(
                        label=label, options=annotation_args, default_value=default, python_type=str
                    )
                elif inspect.isclass(annotation) and issubclass(annotation, StrEnum):
                    field = AutocompleteFiled(
                        label=label, options=annotation, default_value=default, python_type=annotation
                    )
                elif inspect.isclass(annotation) and issubclass(annotation, bool):
                    field = CheckboxFiled(label=label, default_value=default or False)
                elif inspect.isclass(annotation) and issubclass(annotation, str):
                    field = StringField(label=label, default_value=default)
                elif inspect.isclass(annotation) and issubclass(annotation, int):
                    field = NumberField(label=label, default_value=default, python_type=int)
                elif inspect.isclass(annotation) and issubclass(annotation, float):
                    field = NumberField(label=label, default_value=default, python_type=float)
                elif inspect.isclass(annotation) and issubclass(annotation, BytesIO):
                    field = FileField(label=label)
                elif inspect.isclass(annotation) and issubclass(annotation, date):
                    field = DateField(label=label, default_value=default)
                else:
                    raise NotImplementedError(
                        f"Unsupported script parameter type {annotation} for param {param.name} "
                        f"of {callable_name}. "
                        f"Supported types are: str, int, float, bool, StrEnum, Literal, List[], BytesIO (file), date"
                    )
            field.optional = param.default is None
            result[param.name] = field
        return result

    def process_input_params(self, config: Dict[str, Field], params: Dict) -> Dict:
        result = {}
        for field_name, field_value in config.items():
            if not field_name in params:
                if field_value.default_value is not None:
                    result[field_name] = field_value.default_value
                if field_value.optional:
                    result[field_name] = None
            else:
                user_input = params[field_name]
                if field_value.python_type:
                    if field_value.type in (FieldTypeEnum.multi_autocomplete, FieldTypeEnum.string_list):
                        user_input = [field_value.python_type(item) for item in user_input] if user_input else []
                    elif field_value.type == FieldTypeEnum.file:
                        user_input = self._convert_base64file_to_bytes(user_input["data"])
                    elif field_value.type == FieldTypeEnum.date:
                        user_input = pendulum.parse(user_input).date()
                    else:
                        user_input = field_value.python_type(user_input)
                result[field_name] = user_input
        return result

    @staticmethod
    def process_input_params_for_save(config: Dict[str, Field], original_params: Dict, processed_params: Dict) -> Dict:
        result = deepcopy(processed_params)
        for field_name, field_value in config.items():
            if user_input := original_params.get(field_name):
                if field_value.type == FieldTypeEnum.file:
                    result[field_name] = user_input["fileName"]
        return result

    @staticmethod
    def _convert_base64file_to_bytes(base64_data: str) -> BytesIO:
        if "," in base64_data:
            base64_data = base64_data.split(",", 1)[1]
        return BytesIO(base64.b64decode(base64_data))
