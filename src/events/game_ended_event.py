from typing import Literal

from src.events.eventClass import Event
from src.gameClass import Game

class GameEnded(Event):
    def __init__(self,
                 game: Game,
                 event_name: str,
                 text: str,
                 text_slide_speed: float,
                 direction: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled',) -> None:
        super().__init__(game, event_name, state)
        self.text = text
        self.text_slide_speed = text_slide_speed
        self.direction = direction

        self.x = 0

    def update(self, current_tick: float, last_tick: float) -> None:
        dt = current_tick - last_tick
