from typing import Literal
from time import monotonic

from events.eventClass import Event
from ui.lane import Lane

class Waves(Event):
    def __init__(self,
                 game,
                 event_name: str,
                 wave_interval: float = 10,
                 zombie_spawn_interval: float = 5,
                 max_wave_duration: float = 60,
                 min_zombie_hp: int = 1000,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        self.wave_interval = wave_interval
        self.zombie_spawn_interval = zombie_spawn_interval
        self.max_wave_duration = max_wave_duration
        
        self.creation_time = monotonic()
        self.wave_began_timestamp = 0
        self.wave_ended_timestamp = 0
        self.has_last_wave_ended = False

        self.min_zombie_hp = min_zombie_hp
        self.total_zombie_hp = 0
        self.last_zombie_spawn_timestamp = 0
        self.zombie_stack = []


    def update(self, current_tick: float, last_tick: float) -> None:
        # 1 plants <> 250 zombie hp
        # Min difficulty : 1000 zombie hp
        if self.state != 1:
            return
        
        if current_tick - self.wave_began_timestamp <= self.max_wave_duration and not self.has_last_wave_ended: # ongoing wave
            if len(self.zombie_stack) > 0: # more zombies to come
                pass
            else: # no more :>
                self.wave_ended_timestamp = current_tick
                print("a zombie wave has ended. (before max duration)")
                print("a zombie wave will begin in {} seconds".format(
                    (self.wave_interval + (self.wave_began_timestamp + self.max_wave_duration  - current_tick))
                ))

        elif current_tick - self.wave_began_timestamp > self.max_wave_duration and not self.has_last_wave_ended: # wave duration expired
            print("a zombie wave has ended. (exceeded max duration)")