from dataclasses import dataclass
from plantsClass import Plant, Sunflower
from zombiesClass import Zombie
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameClass import Slot

@dataclass
class LivingPlant:
    plant: Plant
    slot: "Slot"
    
    def __post_init__(self):
        self.name = self.plant.name
        self.health_scale = self.plant.health
        self.health = self.health_scale

class LivingSunflower(LivingPlant):
    def __init__(self, plant: Sunflower, slot: "Slot"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower Plant")
        super().__init__(plant=plant, slot=slot)
        self.lastly_produced: float = 0
        self.blinked_slot: float = 0

@dataclass
class LivingZombie:
    zombie: Zombie
    
    def __post_init__(self):
        self.name = self.zombie.name
        self.health_scale = self.zombie.health
        self.health = self.health_scale

@dataclass
class Lawnmoyer:
    name: str = "Lawnmoyer"
    speed: float = 2