from typing import Literal

# from src.gameClass import Game
from ui.lane import Lane

class Event():
    STATE_TO_INT = {'disabled': -1, "paused": 0, "enabled": 1}
    STATE = Literal['disabled', 'paused', 'enabled']
    STATE_INT = Literal[-1, 0, 1]

    def __init__(self,
                 game: "Game",
                 event_name: str,
                 priority: int,
                #  is_ui: bool,
                 state: STATE | STATE_INT = 'disabled') -> None:
        self.game = game
        self.name = event_name
        self.priority = priority

        self.ui_conf: dict[tuple[int, int], dict[str, str]] = {}

        if not str(state).isdigit() and state in self.STATE_TO_INT.keys():
            new_state = str(state)
            self.state = self.STATE_TO_INT[new_state]

        if state in self.STATE_TO_INT.values():
            self.state = state

    def enable(self) -> None:
        if self.state != 1:
            self.state = 1
            self._on_enable()

    def _on_enable(self) -> None:
        print(self.name, "enabled.")

    def pause(self) -> None:
        if self.state != 0:
            self.state = 0
            self._on_pause()

    def _on_pause(self) -> None:
        print(self.name, "paused.")

    def disable(self) -> None:
        if self.state != -1:
            self.state = -1
            self._on_disable()

    def _on_disable(self) -> None:
        print(self.name, "disabled.")

    def update(self, current_tick: float, last_tick: float) -> None:
        if self.state == 1:
            self._ui_update(self.game.board, current_tick, last_tick)

    def _ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> None:
        self.ui_conf = {}