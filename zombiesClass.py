from dataclasses import dataclass

@dataclass
class Zombie:
    name: str
    attack_damage: int
    speed: float
    health: int

    attack_range = .2
    attack_cooldown = 1.

CLASSIC_ZOMBIE = Zombie(name="Zombie", health=190, attack_damage=100, speed=round(1/4.7, 4))

ZOMBIES: dict[str, Zombie] = {
    'classic_zombie': CLASSIC_ZOMBIE,
}