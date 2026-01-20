from dataclasses import dataclass
from plantsClass import Plant, Sunflower, Peashooter
from zombiesClass import Zombie
from typing import TYPE_CHECKING
from time import monotonic

if TYPE_CHECKING:
    from gameClass import Slot
    from playerClass import Lane

@dataclass
class LivingPlant:
    plant: Plant
    slot: "Slot"

    def __post_init__(self):
        self.name = self.plant.name
        self.health_scale = self.plant.health
        self.health = self.health_scale
        self.lane = self.slot.lane
        self.x = self.slot.x + .5
        self.slot.taken_by = self

    def damage(self, damages: int):
        """
        damage(amount: int) -> None : inflige 'amount' dégats à self
        """
        self.health = max(0, self.health - damages)
        if self.health == 0:
            self.slot.configure(bg=self.slot.default_color)
            self.slot.taken_by = None
            del self

class LivingSunflower(LivingPlant):
    def __init__(self, plant: Sunflower, slot: "Slot"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")
        super().__init__(plant=plant, slot=slot)
        self.lastly_produced: float = 0 # Timestamp of last production
        self.blinked_slot: float = 0 # used for the production notification (timestamp)

    """
    Faire les méthodes de ticking et tout ici et pas dans la boucle principale (fausse POO)
    """

class LivingPeashooter(LivingPlant):
    """
    The peashooter you see on the board
    """
    def __init__(self, plant: Peashooter, slot: "Slot"):
        if not isinstance(plant, Peashooter):
            raise TypeError("LivingPeashooter requires a Peashooter class instance")
        super().__init__(plant=plant, slot=slot)
        self.pea_launch_cooldown = plant.pea_launch_cooldown
        self.pea_damage = plant.pea_damage
        self.frozen_projectile = plant.frozen_projectile
        self.lastly_shot = monotonic() - self.pea_launch_cooldown + 1 # Timestamp (-1 second cooldown first time)

    """
    Faire les méthodes de ticking et tout ici et pas dans la boucle principale (fausse POO)
    """

@dataclass
class LivingZombie:
    zombie: Zombie
    x: float
    lane: "Lane"

    def __post_init__(self):
        self.name = self.zombie.name
        self.health_scale = self.zombie.health
        self.health = self.health_scale
        self.attack_damage = self.zombie.attack_damage
        self.attack_range = self.zombie.attack_range
        self.attack_cooldown = self.zombie.attack_cooldown
        self.speed = self.zombie.speed
        self.last_attacked = 0.

    def damage(self, damages: int):
        self.health = max(0, self.health - damages)
        # if self.health == 0:
        #     new_kill = self.lane.depiler_zombie()
        #     print(f"{new_kill.name} tué.")
        #     del self

@dataclass
class Lawnmoyer:
    name: str = "Lawnmoyer"
    speed: float = 2

@dataclass
class LivingLawnmoyer:
    lawnmoyer: Lawnmoyer
    lane: "Lane"

    def __post_init__(self):
        self.name = self.lawnmoyer.name
        self.speed = self.lawnmoyer.speed