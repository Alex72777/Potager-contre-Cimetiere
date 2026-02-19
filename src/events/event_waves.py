from events.eventClass import Event

class Waves(Event):
    def __init__(self,
                 game: "Game",
                 event_name: str,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        