from typing import Literal

from src.events.eventClass import Event
from src.gameClass import Game
from src.ui.lane import Lane

class GameEnded(Event):
    # 5 (height) : {"char": [list of tuple slot cords starting from upper left]}
    LETTERS = {
        5: {
            "a": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2) ,(2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (4, 0), (4, 2)]
        }
    }
    def __init__(self,
                 game: Game,
                 event_name: str,
                 text: str,
                 text_slide_speed: float,
                 direction: float,
                 starting_x: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled',) -> None:
        super().__init__(game, event_name, state)
        self.text = text
        self.text_slide_speed = text_slide_speed
        self.direction = direction
        self.width = len(self.text) * 3
        self.starting_x = starting_x

        self.x = 0
        self.ui_conf = {}

    def update(self, current_tick: float, last_tick: float) -> None:
        dt = current_tick - last_tick
        if self.x > self.width:
            self.disable()

        self.x += self.text_slide_speed * self.direction * dt

    def _ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> None:
        # returns {(0, 0): {"bg": "red"}}

        # {(0, 0): {"bg": "red"}}
        display_slots: dict[tuple, dict] = {}
        display_slots[(0, 0)] = {"bg": "pink"}

        self.ui_conf = display_slots
