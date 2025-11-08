from dataclasses import dataclass, field
from plantsClass import Plant, PEASHOOTER

@dataclass
class Player:
    unlocked_plants: list[Plant] = field(default_factory=lambda: [PEASHOOTER])
    suns: int = 0