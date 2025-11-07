from dataclasses import dataclass
from common import Lane
from plantsClass import Plant

@dataclass
class Entity:
    lane: Lane
    health_scale: int
    
@dataclass
class LivingPlant(Entity):
    plant: Plant

@dataclass
class Lawnmoyer:
    name: str = "Lawnmoyer"
    speed: float = 2