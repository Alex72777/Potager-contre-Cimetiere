from typing import Literal

from src.gameClass import Game
from src.ui.lane import Lane

class Event():
    STATE_TO_INT = {'disabled': -1, "paused": 0, "enabled": 1}
    STATE = Literal['disabled', 'paused', 'enabled']
    STATE_INT = Literal[-1, 0, 1]

    def __init__(self,
                 game: Game,
                 event_name: str,
                 state: STATE | STATE_INT = 'disabled') -> None:
        self.master = game
        self.event_name = event_name

        if not str(state).isdigit() and state in self.STATE_TO_INT.keys():
            new_state = str(state)
            self.state = self.STATE_TO_INT[new_state]

        if state in self.STATE_TO_INT.values():
            self.state = state

    def enable(self) -> None:
        self.state = 1

    def pause(self) -> None:
        self.state = 0

    def disable(self) -> None:
        self.state = -1

    def update(self, current_tick: float, last_tick: float) -> None:
        if self.state == 1:
            print(f"Empty update logic for: {self.event_name}")

    def ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> dict:
        return {}