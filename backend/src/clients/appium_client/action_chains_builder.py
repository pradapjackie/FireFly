from __future__ import annotations

from src.clients.appium_client.schemas import ActionsChain


class ActionsBuilder:
    def __init__(self):
        self.actions = list()
        self._result = dict()

    def init_mouse_actions(self) -> ActionsBuilder:
        self._result = {"type": "pointer", "parameters": {"pointerType": "mouse"}, "id": "mouse"}
        return self

    def init_touch_actions(self) -> ActionsBuilder:
        self._result = {"type": "pointer", "parameters": {"pointerType": "touch"}, "id": "touch"}
        return self

    def mouse_move(self, x: int, y: int, duration=2000) -> ActionsBuilder:
        self.actions.append({"type": "pointerMove", "duration": duration, "x": x, "y": y, "origin": "viewport"})
        return self

    def pointer_down(self, duration: int = 0) -> ActionsBuilder:
        self.actions.append({"type": "pointerDown", "duration": duration, "button": 0})
        return self

    def pointer_up(self, duration: int = 0) -> ActionsBuilder:
        self.actions.append({"type": "pointerUp", "duration": duration, "button": 0})
        return self

    def pause(self, duration: int = 200) -> ActionsBuilder:
        self.actions.append({"type": "pause", "duration": duration})
        return self

    def build(self) -> ActionsChain:
        self._result["actions"] = self.actions
        return ActionsChain(actions=[self._result])

    def _send_key(self, key: str):
        pass

    def init_send_keys(self) -> ActionsBuilder:
        self._result = {
            "type": "key",
            "id": "key",
        }
        return self

    def send_keys(self, text: str) -> ActionsBuilder:
        for symbol in text:
            self.actions.append({"type": "keyDown", "value": symbol})
            self.actions.append({"type": "keyUp", "value": symbol})
        return self
