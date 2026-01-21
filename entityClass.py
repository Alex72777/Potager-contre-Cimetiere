from dataclasses import dataclass
from plantsClass import PLANTS
from zombiesClass import Zombie
from typing import TYPE_CHECKING
from time import monotonic

if TYPE_CHECKING:
    from gameClass import Slot, Game
    from playerClass import Lane
    from plantsClass import Plant, Sunflower, Peashooter

@dataclass
class LivingPlant:
    master: Game
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

    def update(self, current_tick: int, last_tick: int) -> None:
        """
        Méthode de ticking.
        """
        pass

    def sous_texte(self, current_tick: int, last_tick: int) -> str:
        """
        Représentation textuelle utilsée pour les emplacements dans le jardin
        """
        return self.name.upper()

    def ui_update(self, current_tick: int, last_tick: int) -> dict:
        """

        """
        return {}

class LivingSunflower(LivingPlant):
    def __init__(self, plant: Sunflower, slot: "Slot", master: Game):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.lastly_produced: float = 0 # Timestamp of last production
        self.blinked_slot: float = 0 # used for the production notification (timestamp)

    def update(self, current_tick: int, last_tick: int) -> None:
        """
        Méthode de ticking pour la classe LivingSunflower.
        """
        if current_tick - self.lastly_produced >= PLANTS['sunflower'].suns_cooldown:
            self.master.player.add_suns(PLANTS['sunflower'].suns_income)
            self.lastly_produced = current_tick
            self.blinked_slot = current_tick

    def sous_texte(self, current_tick: int, last_tick: int) -> str:
        return f"{self.name.upper()} ({round(PLANTS['sunflower'].suns_cooldown - (monotonic() - self.lastly_produced), 1)})"

    def ui_update(self, current_tick: int, last_tick: int) -> dict:
        """
        Pour changer la couleur ici
        """
        if current_tick - self.blinked_slot >= 1:
            return {"bg": self.slot.default_color} # ???? Nécessaire?
        else:
            return {"bg": "yellow"}

class LivingPeashooter(LivingPlant):
    """
    La représentation vivante de l'entité.
    """
    def __init__(self, plant: Peashooter, slot: "Slot", master: Game):
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

    def update(self, current_tick: int, last_tick: int) -> None:
        """
        Méthode de ticking pour la classe LivingPeashooter.
        """
        ps_plant = PLANTS['peashooter']
        if current_tick - self.lastly_shot >= ps_plant.pea_launch_cooldown:
            for shot in range(ps_plant.amount_of_peas):
                zombie = self.lane.get_zombie()
                if zombie and zombie.x >= self.x:
                    zombie.damage(ps_plant.pea_damage)
            self.lastly_shot = current_tick

    def sous_texte(self, current_tick: int, last_tick: int) -> str:
        ps_plant = PLANTS['peashooter']

        if self.lane.get_zombie() != None:
            return f"{ps_plant.name.upper()} ({round(ps_plant.pea_launch_cooldown - (monotonic() - self.lastly_shot), 1)})"
        else:
            return f"{ps_plant.name.upper()}"
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

    def update(self) -> None:
        """
        Méthode de ticking pour la classe LivingZombie.
        """
        if self.health == 0:
            self.lane.depiler_zombie()
            print(f"{self.name} tué.")
            del self

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

    def update(self) -> None:
        """
        Méthode de ticking pour la classe LivingLawnmoyer.
        """
        pass