from dataclasses import dataclass, field

from livingentities.livingzombies.livingzombieClass import LivingZombie
from entities.plantsClass import Plant

@dataclass
class PlantEater(LivingZombie):
    consumes_plants: list[Plant] = field(default_factory= lambda: [])
    eating_cooldown: float = 60 # seconds

    def __post_init__(self):
        super().__post_init__()
        self.last_meal = 0 # timestamp

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe PlantEater.
        """
        dt = current_tick - last_tick

        if self.health == 0:
            self.lane.defiler_zombie()
            return

        next_plant = self.lane.get_plante()
        if (next_plant
            and next_plant.x <= self.x < next_plant.x + self.attack_range
            and (current_tick - self.last_attacked >= self.attack_cooldown or current_tick - self.last_meal > self.eating_cooldown)
            ): # Attack range

            if current_tick - self.last_meal > self.eating_cooldown:
                print('%s miam miam with %s' % (self.name, next_plant.name))
                next_plant.kill()
                self.last_meal = current_tick
            else:
                next_plant.damage(self.attack_damage)
                self.last_attacked = current_tick
                # print(self.health, next_plant.health)

        if next_plant:
            self.x = max(next_plant.x, self.x - self.speed * dt)
        else:
            self.x = max(0, self.x - self.speed * dt)

        if self.x == 0:
            # lawnmoyers be cooking
            if self.lane.house_slot.taken_by != None:
                self.lane.release_lawnmoyer()
            else:
                self.master.events['event_end_game'].enable()
                self.kill()