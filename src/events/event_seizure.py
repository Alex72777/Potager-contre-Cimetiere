from typing import Literal
from random import randint

from events.eventClass import Event
from ui.lane import Lane

class Seizure(Event):
    def __init__(self,
                 game: "Game",
                 event_name: str,
                 elapse_time: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game, event_name, priority=5, state=state)
        self.game = game
        self.timestamp = 0
        self.elapse_time = elapse_time
        self.priority = 5
        self.ui_conf = {}

    def _ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> None:
        if current_tick - self.timestamp > self.elapse_time:
            rand_slot = (randint(0, len(board)), randint(0, board[0].len_slots))
            display_slots: dict[tuple, dict] = {}
            display_slots[rand_slot] = {"bg": "blue"}

            self.ui_conf = display_slots
            self.timestamp = current_tick