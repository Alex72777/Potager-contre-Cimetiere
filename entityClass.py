from dataclasses import dataclass
from plantsClass import Plant, Sunflower, Peashooter
from zombiesClass import Zombie
from typing import TYPE_CHECKING
from time import time

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
    
    def damage(self, damages: int):
        self.health = max(0, self.health - damages)
        if not self.health:
            self.slot.taken_by = None
            del self

class LivingSunflower(LivingPlant):
    def __init__(self, plant: Sunflower, slot: "Slot"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")
        super().__init__(plant=plant, slot=slot)
        self.lastly_produced: float = 0
        self.blinked_slot: float = 0

class LivingPeashooter(LivingPlant):
    def __init__(self, plant: Peashooter, slot: "Slot"):
        if not isinstance(plant, Peashooter):
            raise TypeError("LivingPeashooter requires a Peashooter class instance")
        super().__init__(plant=plant, slot=slot)
        self.pea_launch_cooldown = plant.pea_launch_cooldown
        self.pea_damage = plant.pea_damage
        self.frozen_projectile = plant.frozen_projectile
        self.lastly_shot = time() - self.pea_launch_cooldown + 1

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
        if not self.health:
            slot: Slot = self.lane.slots[round(self.x)]
            self.lane.entities.pop(self.lane.entities.index(self))
            if not slot.taken_by:
                slot.configure(text='')
            del self

@dataclass
class Lawnmoyer:
    name: str = "Lawnmoyer"
    speed: float = 2

@dataclass
class RollingLawnmoyer:
    lawnmoyer: Lawnmoyer
    lane: "Lane"
    
    def __post_init__(self):
        self.name = self.lawnmoyer.name
        self.speed = self.lawnmoyer.speed