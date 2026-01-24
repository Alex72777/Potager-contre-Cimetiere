from dataclasses import dataclass

@dataclass
class Plant:
    name: str
    cooldown: float
    cost: int
    health: int

class Peashooter(Plant):
    def __init__(self,
                 name,
                 cost,
                 pea_launch_cooldown = 2,
                 pea_damage = 20,
                 frozen_projectile = False,
                 amount_of_peas = 1):
        super().__init__(name=name, cooldown=7.5, cost=cost, health=300)
        self.pea_launch_cooldown = pea_launch_cooldown
        self.pea_damage = pea_damage
        self.frozen_projectile = frozen_projectile
        self.amount_of_peas = amount_of_peas


class Sunflower(Plant):
    def __init__(self,
                 name,
                 cost,
                 suns_cooldown,
                 suns_income):
        super().__init__(name=name, cost=cost, cooldown=7.5, health=300)
        self.suns_cooldown = suns_cooldown
        self.suns_income = suns_income

class Wallnut(Plant):
    def __init__(self,
                 name,
                 cost,
                 health,
                 cooldown = 30,):
        super().__init__(name=name, cost=cost, cooldown=cooldown, health=health)

PEASHOOTER = Peashooter(name='Peashooter', cost=100)
SNOW_PEA = Peashooter(name='Snow Pea', cost=175, frozen_projectile=True)
REPEATER = Peashooter(name="Repeater", cost=200, amount_of_peas=2)
SUNFLOWER = Sunflower(name="Sunflower", cost=50, suns_cooldown=24.25, suns_income=25)
WALLNUT = Wallnut(name="Wall-nut", cost=50, health=4000)

PLANTS = {
    'peashooter': PEASHOOTER ,
    'snow_pea': SNOW_PEA,
    'repeater': REPEATER,
    'sunflower': SUNFLOWER,
    'wallnut': WALLNUT,
}