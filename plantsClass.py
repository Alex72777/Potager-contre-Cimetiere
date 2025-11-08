from dataclasses import dataclass

@dataclass
class Plant:
    name: str
    cooldown: float
    cost: int
    health: int

PEASHOOTER = Plant(name='Peashooter', cooldown=7.5, cost=100, health=100)

PLANTS = {
    'peashooter': PEASHOOTER
}