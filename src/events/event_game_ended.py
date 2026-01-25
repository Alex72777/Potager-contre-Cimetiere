from typing import Literal
from random import randint

from events.eventClass import Event
# from src.gameClass import Game
from ui.lane import Lane

class GameEnded(Event):
    # 5 (height) : {"char": [list of tuple slot cords starting from upper left]}
    LETTERS = {
        5: {
            "a": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2) ,(2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (4, 0), (4, 2)]
        }
    }
    def __init__(self,
                 game: "Game",
                 event_name: str,
                 text: str,
                 text_slide_speed: float,
                 direction: float,
                 starting_x: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled',) -> None:
        super().__init__(game, event_name, True, state)
        self.text = text
        self.text_slide_speed = text_slide_speed
        self.direction = direction
        self.starting_x = starting_x
        self.width = len(self.text) * 3
        self.priority = 5

        self.x = 0
        self.ui_conf = {}

    def update(self, current_tick: float, last_tick: float) -> None:
        dt = current_tick - last_tick
        if self.x > self.width:
            pass
            # self.disable()

        self.x += self.text_slide_speed * self.direction * dt
        self._ui_update(self.game.board, current_tick, last_tick)

    def _ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> None:
        # returns {(0, 0): {"bg": "red"}}

        # {(0, 0): {"bg": "red"}}
        rand_slot = (randint(0, len(board)), randint(0, board[0].len_slots))
        display_slots: dict[tuple, dict] = {}
        display_slots[rand_slot] = {"bg": "blue"}

        self.ui_conf = display_slots
