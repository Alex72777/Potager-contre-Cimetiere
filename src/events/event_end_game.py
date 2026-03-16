from typing import Literal

from events.eventClass import Event

class TerminateGame(Event):
    def __init__(self, game, event_name: str, priority: int, state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game, event_name, priority, state)
        self.has_ended = False
    
    def _on_enable(self) -> None:
        super()._on_enable()
        if not self.has_ended:
            print('game stopped')
            self.has_ended = True
            # self.events['event_seizure'].enable()
            # self.events['event_invoke_zombie'].disable()
            self.game.events['event_waves'].disable()

            
            for lane in self.game.board:
                lane.release_lawnmoyer(True)
        self.disable()