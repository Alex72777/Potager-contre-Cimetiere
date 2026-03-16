from typing import Literal

from events.eventClass import Event

class LaunchGame(Event):
    def __init__(self, game, event_name: str, priority: int, state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game, event_name, priority, state)
    
    def _on_enable(self) -> None:
        super()._on_enable()
        self.game.events['event_waves'].enable()
        print("game started")
        self.disable()