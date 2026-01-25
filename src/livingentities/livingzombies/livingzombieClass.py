from dataclasses import dataclass
from math import floor

from entities.zombiesClass import Zombie

@dataclass
class LivingZombie:
    zombie: Zombie
    x: float
    lane: "Lane"
    master: "Game"

    def __post_init__(self):
        self.name = self.zombie.name
        self.health_scale = self.zombie.health
        self.health = self.health_scale
        self.attack_damage = self.zombie.attack_damage
        self.attack_range = self.zombie.attack_range
        self.attack_cooldown = self.zombie.attack_cooldown
        self.speed = self.zombie.speed
        self.last_attacked = 0.

    def damage(self, damage: int):
        self.health = max(0, self.health - damage)

    def kill(self) -> None:
        self.health = 0

    def update(self, current_tick: float, last_tick: float) -> None:
        dt = current_tick - last_tick
        """
        Méthode de ticking pour la classe LivingZombie.
        """

        if self.health == 0:
            self.lane.defiler_zombie()
            return

        next_plant = self.lane.get_plante()
        if (next_plant
            and next_plant.x <= self.x < next_plant.x + self.attack_range
            and current_tick - self.last_attacked >= self.attack_cooldown
            ): # Attack range

            next_plant.damage(self.attack_damage)
            self.last_attacked = current_tick
            # print(sep=.health, next_plant.health)

        if next_plant:
            self.x = max(next_plant.x, self.x - self.speed * dt)
        else:
            self.x = max(0, self.x - self.speed * dt)

        if self.x == 0:
            # lawnmoyers be cooking (if any)
            if self.lane.house_slot.taken_by != None:
                self.lane.release_lawnmoyer()
            else:
                self.master.end_game()

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        if not (current_tick - self.last_attacked >= self.attack_cooldown):
            return f"""
{self.name.upper()} [{round(self.health / self.health_scale * 100)}%] ({round(self.attack_cooldown - (current_tick - self.last_attacked), 1)})
"""
        else:
            return f"{self.name.upper()} [{round(self.health / self.health_scale * 100)}%]"

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Docstring
        """
        return {"content": {min(self.lane.len_slots - 1, floor(self.x)): {"bg": "red"}}, "priority": 1}

    @property
    def is_alive(self) -> bool:
        if self.health == 0:
            return True
        return False