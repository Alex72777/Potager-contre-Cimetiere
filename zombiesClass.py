from dataclasses import dataclass

@dataclass
class Zombie:
    name: str
    dps: int
    speed: float
    health: int
    
    attack_range: float = .2

CLASSIC_ZOMBIE = Zombie(name="Zombie", health=190, dps=100, speed=1/4.7)

ZOMBIES = {
    'classic_zombie': CLASSIC_ZOMBIE,
}