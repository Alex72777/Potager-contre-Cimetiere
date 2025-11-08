from dataclasses import dataclass
from plantsClass import Plant
from zombiesClass import Zombie

@dataclass
class LivingPlant:
    plant: Plant
    
    def __post_init__(self):
        self.name = self.plant.name
        self.health_scale = self.plant.health
        self.health = self.health_scale

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