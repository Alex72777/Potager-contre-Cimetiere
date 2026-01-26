from typing import Literal
from time import monotonic
from random import randint, choice

from events.eventClass import Event

from ui.lane import Lane

from entities.zombiesClass import Zombie

from livingentities.livingzombies.livingzombieClass import LivingZombie

class InvokeZombie(Event):
    def __init__(self,
                 game: "Game",
                 event_name: str,
                 zombie: Zombie,
                 interval: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game, event_name, priority=1, state=state)
        self.zombie = zombie
        self.interval = interval
        self.timestamp = monotonic()

    def update(self, current_tick: float, last_tick: float) -> None:
        if self.state == 1:
            lanes: list[Lane] = self.game.board
            board_len = lanes[0].len_slots

            if self.game.has_ended:
                self.state = -1

            if current_tick - self.timestamp > self.interval:
                spawning_lane = choice(lanes)
                new_living_zombie = LivingZombie(self.zombie, board_len, spawning_lane, self.game)
                spawning_lane.enfiler_zombie(new_living_zombie)
                self.timestamp = current_tick