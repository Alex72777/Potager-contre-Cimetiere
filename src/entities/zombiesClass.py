from dataclasses import dataclass

@dataclass
class Zombie:
    name: str
    attack_damage: int
    health: int
    is_boss: bool = False

    speed = round(1/4.7, 4)
    attack_range = .2
    attack_cooldown = 1.

    def to_string(self) -> str:
        return self.name.upper()

ZOMBIES: dict[str, Zombie] = {
    'classic_zombie': Zombie(name="Zombie", health=200, attack_damage=100),
    'heavy_zombie': Zombie(name="Heavy Zombie", health=300, attack_damage=100),
    'armored_zombie': Zombie(name="Armored Zombie", health=450, attack_damage=100),
    'patrol_zombie': Zombie(name="Patrol Zombie", health=200, attack_damage=250),
    'boss_hulk': Zombie(name="Hulk", health=2000, attack_damage=250, is_boss=True),
}
