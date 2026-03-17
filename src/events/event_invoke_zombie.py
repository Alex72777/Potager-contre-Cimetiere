from typing import Literal
from time import monotonic
from random import choice

from events.eventClass import Event

from ui.lane import Lane

from entities.zombiesClass import Zombie

from livingentities.livingzombies.livingzombieClass import LivingZombie
from livingentities.livingzombies.zombie_plant_eater import PlantEater

class InvokeZombie(Event):
    def __init__(self,
                 game,
                 event_name: str,
                 zombie: Zombie | list[Zombie],
                 interval: float,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game, event_name, priority=5, state=state)
        self.zombie = zombie
        self.interval = interval
        self.timestamp = monotonic()
        self.keytime = 0
        self.ui_conf = {}

    def _on_enable(self) -> None:
        super()._on_enable()
        lanes: list[Lane] = self.game.board
        self.next_lane = choice(lanes)

    def update(self, current_tick: float, last_tick: float) -> None:
        if self.state == 1:
            self._ui_update(self.game.board, current_tick, last_tick)
            lanes: list[Lane] = self.game.board
            board_len = lanes[0].width

            if current_tick - self.timestamp > self.interval:
                killed_zombies = self.game.player.killed_zombies
                spawning_lane = self.next_lane
            
                if isinstance(self.zombie, list):
                    zombie = choice(self.zombie)
                    if zombie.eats_plant:
                        new_living_zombie = PlantEater(zombie, board_len, spawning_lane, self.game, zombie.is_boss, zombie.consumes_plants, zombie.eating_cooldown)
                    else:
                        new_living_zombie = LivingZombie(choice(self.zombie), board_len, spawning_lane, self.game)
                else:
                    if self.zombie.eats_plant:
                        new_living_zombie = PlantEater(self.zombie, board_len, spawning_lane, self.game, self.zombie.is_boss, self.zombie.consumes_plants, self.zombie.eating_cooldown)
                    else:
                        new_living_zombie = LivingZombie(self.zombie, board_len, spawning_lane, self.game)
                
                self.next_lane.enfiler_zombie(new_living_zombie)
                self.timestamp = current_tick
                self.next_lane = choice(lanes)

    def _ui_update(self, board: list[Lane], current_tick: float, last_tick: float) -> None:
        self.ui_conf = {}
        if current_tick - self.timestamp <= self.interval and current_tick - self.timestamp > self.interval - 3:
            slot_pos = self.next_lane.slots[self.next_lane.width - 1].pos
            if current_tick - self.keytime > 1:
                self.ui_conf = {}
                self.keytime = current_tick

            if current_tick - self.keytime > .5:
                self.ui_conf = {slot_pos: {"bg": "red"}}