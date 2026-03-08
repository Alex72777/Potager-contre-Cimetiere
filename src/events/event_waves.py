from typing import Literal
from time import monotonic

from events.eventClass import Event
from ui.lane import Lane

class Waves(Event):
    def __init__(self,
                 game: "Game",
                 event_name: str,
                 wave_interval: float = 10,
                 zombie_spawn_interval: float = 5,
                 max_wave_duration: float = 60,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        self.wave_interval = wave_interval
        self.zombie_spawn_interval = zombie_spawn_interval
        self.max_wave_duration = max_wave_duration
        
        self.creation_time = monotonic()
        self.last_wave_timestamp = 0


    def update(self, current_tick: float, last_tick: float) -> None:
        # 1 plants <> 250 zombie hp
        # Min difficulty : 1000 zombie hp
        if self.state != 1:
            return
        
        pass

    def _on_pause(self) -> None:
        return super()._on_pause()