from dataclasses import dataclass
from plantsClass import PLANTS, Plant, Sunflower, Peashooter, Lawnmoyer
from zombiesClass import Zombie
from typing import TYPE_CHECKING
from time import monotonic
from random import choice

if TYPE_CHECKING:
    from gameClass import Slot, Game
    from playerClass import Lane

@dataclass
class LivingPlant:
    master: "Game"
    plant: "Plant"
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
            self.slot.taken_by = None
            self.lane.depiler_plante()
            del self

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking.
        """
        pass

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        """
        Représentation textuelle utilsée pour les emplacements dans le jardin
        """
        return self.name.upper()

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Docstring
        """
        return {"priority": 0}

class LivingSunflower(LivingPlant):
    def __init__(self, plant: "Sunflower", slot: "Slot", master: "Game"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.lastly_produced: float = monotonic() - self.plant.suns_cooldown + 5 # Timestamp of last production
        self.blinked_slot: float = 0 # used for the production notification (timestamp)

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingSunflower.
        """
        sf_plant: Sunflower = self.plant
        if current_tick - self.lastly_produced >= sf_plant.suns_cooldown:
            self.master.player.add_suns(sf_plant.suns_income)
            self.lastly_produced = current_tick
            self.blinked_slot = current_tick

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        sf_plant: Sunflower = self.plant
        text = f"{self.name.upper()} ({round(sf_plant.suns_cooldown - (monotonic() - self.lastly_produced), 1)})"

        if self.health < self.health_scale:
            text += f" [{round(self.health / self.health_scale * 100)}%]"

        return text

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Pour changer la couleur ici
        """
        if current_tick - self.blinked_slot >= 1:
            return {"bg": self.slot.default_color, "priority": 1} # ???? Nécessaire?
        else:
            return {"bg": "yellow", "priority": 1}

class LivingPeashooter(LivingPlant):
    """
    La représentation vivante de l'entité.
    """
    def __init__(self, plant: "Peashooter", slot: "Slot", master: "Game"):
        if not isinstance(plant, Peashooter):
            raise TypeError("LivingPeashooter requires a Peashooter class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.pea_launch_cooldown = plant.pea_launch_cooldown
        self.pea_damage = plant.pea_damage
        self.frozen_projectile = plant.frozen_projectile
        self.lastly_shot = monotonic() - self.pea_launch_cooldown + 1 # Timestamp (-1 second cooldown first time)

    """
    Faire les méthodes de ticking et tout ici et pas dans la boucle principale (fausse POO)
    """

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingPeashooter.
        """
        ps_plant: Peashooter = self.plant
        if current_tick - self.lastly_shot >= ps_plant.pea_launch_cooldown:
            for shot in range(ps_plant.amount_of_peas):
                zombie = self.lane.get_zombie()
                if zombie and zombie.x >= self.x:
                    zombie.damage(ps_plant.pea_damage)
            self.lastly_shot = current_tick

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        ps_plant: Peashooter = self.plant

        text = ""
        if self.lane.get_zombie() != None:
            text = f"{ps_plant.name.upper()} ({round(ps_plant.pea_launch_cooldown - (monotonic() - self.lastly_shot), 1)})"
        else:
            text = f"{ps_plant.name.upper()}"

        if self.health < self.health_scale:
            text += f" [{round(self.health / self.health_scale * 100)}%]"

        return text

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
            del self
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
{self.name.upper()} [{round(self.health / self.health_scale * 100)}%] ({round(self.attack_cooldown - (monotonic() - self.last_attacked), 1)})
"""
        else:
            return f"{self.name.upper()} [{round(self.health / self.health_scale * 100)}%]"

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Docstring
        """
        return {"priority": 1}

@dataclass
class LivingLawnmoyer:
    lawnmoyer: "Lawnmoyer"
    lane: "Lane"

    def __post_init__(self):
        self.name = self.lawnmoyer.name
        self.speed = self.lawnmoyer.speed
        self.x = 0
        self.key_time = 0
        self.bg = ""

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingLawnmoyer.
        """
        dt = current_tick - last_tick
        self.x = min(self.lane.len_slots, self.x + self.speed * dt)

        zombie = self.lane.get_zombie()
        if zombie != None and zombie.x <= self.x:
            zombie.kill()

        if self.x == self.lane.len_slots:
            self.lane.lawnmoyer = None
            del self

    def sous_texte(self) -> str:
        """
        Docstring
        """
        return self.name.upper()

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Docstring
        """
        if monotonic() - self.key_time >= .05:
            self.bg = choice(['blue', 'red', 'pink', 'yellow', 'green', 'purple'])
            self.key_time = monotonic()
        return {"bg": self.bg, "priority": 3}