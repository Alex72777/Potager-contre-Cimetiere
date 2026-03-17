from dataclasses import dataclass, field

from entities.plantsClass import PLANTS

@dataclass
class Zombie:
    name: str
    attack_damage: int
    health: int
    is_boss: bool = False

    # Plant eaters

    eats_plant: bool = False
    consumes_plants: list = field(default_factory= lambda: list(PLANTS.values()))
    eating_cooldown: float = 15

    SPEED = round(1/4.7, 4)
    attack_range = .2
    attack_cooldown = 1.

    def to_string(self) -> str:
        return self.name.upper()

ZOMBIES: dict[str, Zombie] = {
    # Zombies de base (faciles)
    'classic_zombie': Zombie(name="Zombie", health=175, attack_damage=100),
    'heavy_zombie': Zombie(name="Heavy Zombie", health=300, attack_damage=100),
    'armored_zombie': Zombie(name="Armored Zombie", health=450, attack_damage=100),
    'patrol_zombie': Zombie(name="Patrol Zombie", health=180, attack_damage=250),
    
    # Zombies intermédiaires (moyens)
    'speedy_zombie': Zombie(name="Speedy Zombie", health=130, attack_damage=80),
    'tank_zombie': Zombie(name="Tank Zombie", health=600, attack_damage=120),
    'assassin_zombie': Zombie(name="Assassin Zombie", health=100, attack_damage=200),
    'giant_zombie': Zombie(name="Giant Zombie", health=800, attack_damage=150),
    'berserker_zombie': Zombie(name="Berserker", health=250, attack_damage=180),
    'slow_zombie': Zombie(name="Slow Zombie", health=500, attack_damage=90),
    'elite_zombie': Zombie(name="Elite Zombie", health=700, attack_damage=160),
    'ninja_zombie': Zombie(name="Ninja Zombie", health=120, attack_damage=220),
    'hungry_zombie': Zombie(name="Hungry Zombie", health=200, attack_damage=100, eats_plant=True),
    
    # Zombies avancés (difficiles)
    'behemoth_zombie': Zombie(name="Behemoth Zombie", health=900, attack_damage=200),
    'phantom_zombie': Zombie(name="Phantom Zombie", health=80, attack_damage=250),
    'colossus_zombie': Zombie(name="Colossus Zombie", health=1200, attack_damage=180),
    'shadow_zombie': Zombie(name="Shadow Zombie", health=150, attack_damage=300),
    
    # Bosses
    'boss_hulk': Zombie(name="Hulk", health=2000, attack_damage=250, is_boss=True),
    'boss_ogre': Zombie(name="Ogre", health=3000, attack_damage=300, is_boss=True, eats_plant=True),
    'boss_titan': Zombie(name="Titan", health=4000, attack_damage=350, is_boss=True),
    'boss_reaper': Zombie(name="Reaper", health=1500, attack_damage=400, is_boss=True),
}
