import base64
import json
from typing import Dict, NewType

FlutterElementId = NewType("FlutterElementId", str)


class FlutterElementIdGenerator:
    def by_ancestor(
        self,
        ancestor: FlutterElementId,
        matching: FlutterElementId,
        match_root: bool = False,
        first_match_only: bool = False,
    ) -> FlutterElementId:
        return self._by_ancestor_or_descendant(
            type_="Ancestor",
            serialized_finder=ancestor,
            matching=matching,
            match_root=match_root,
            first_match_only=first_match_only,
        )

    def by_descendant(
        self,
        descendant: FlutterElementId,
        matching: FlutterElementId,
        match_root: bool = False,
        first_match_only: bool = False,
    ) -> FlutterElementId:
        return self._by_ancestor_or_descendant(
            type_="Descendant",
            serialized_finder=descendant,
            matching=matching,
            match_root=match_root,
            first_match_only=first_match_only,
        )

    def by_semantics_label(self, label: str, is_regexp: bool = False) -> FlutterElementId:
        return self._serialize({"finderType": "BySemanticsLabel", "isRegExp": is_regexp, "label": label})

    def by_tooltip(self, text: str) -> FlutterElementId:
        return self._serialize({"finderType": "ByTooltipMessage", "text": text})

    def by_text(self, text: str) -> FlutterElementId:
        return self._serialize({"finderType": "ByText", "text": text})

    def by_type(self, type_name: str) -> FlutterElementId:
        return self._serialize({"finderType": "ByType", "type": type_name})

    def by_value_key(self, key: str) -> FlutterElementId:
        return self._serialize(
            {
                "finderType": "ByValueKey",
                "keyValueString": key,
                "keyValueType": "String" if isinstance(key, str) else "int",
            }
        )

    def page_back(self) -> FlutterElementId:
        return self._serialize({"finderType": "PageBack"})

    @staticmethod
    def _serialize(finder_dict: Dict) -> FlutterElementId:
        return FlutterElementId(
            base64.b64encode(bytes(json.dumps(finder_dict, separators=(",", ":")), "UTF-8")).decode("UTF-8")
        )

    def _by_ancestor_or_descendant(
        self,
        type_: str,
        serialized_finder: FlutterElementId,
        matching: FlutterElementId,
        match_root: bool = False,
        first_match_only: bool = False,
    ):
        param = {
            "finderType": type_,
            "matchRoot": str(match_root).lower(),
            "firstMatchOnly": str(first_match_only).lower(),
        }

        try:
            finder = json.loads(base64.b64decode(serialized_finder).decode("utf-8"))
        except Exception as e:
            print(e)
            finder = {}

        param.setdefault("of", {})
        for finder_key, finder_value in finder.items():
            param["of"].setdefault(finder_key, finder_value)
        param["of"] = json.dumps(param["of"], separators=(",", ":"))

        try:
            matching = json.loads(base64.b64decode(matching).decode("utf-8"))
        except Exception as e:
            print(e)
            matching = {}
        param.setdefault("matching", {})
        for matching_key, matching_value in matching.items():
            param["matching"].setdefault(matching_key, matching_value)
        param["matching"] = json.dumps(param["matching"], separators=(",", ":"))

        return self._serialize(param)
