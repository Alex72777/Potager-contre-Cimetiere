from time import monotonic
from typing import cast

from livingentities.livingplants.livingplantClass import LivingPlant

from entities.plantsClass import Peashooter, Plant

from ui.slot import Slot


class LivingPeashooter(LivingPlant):
    """
    La représentation vivante de l'entité.
    """
    def __init__(self, plant: Plant, slot: Slot, master: "Game"):
        if not isinstance(plant, Peashooter):
            raise TypeError("LivingPeashooter requires a Peashooter class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.pea_launch_cooldown = plant.pea_launch_cooldown
        self.pea_damage = plant.pea_damage
        self.frozen_projectile = plant.frozen_projectile
        self.lastly_shot = monotonic() - self.pea_launch_cooldown + 1 # Timestamp (-1 second cooldown first time)
        self.ps_plant = cast(Peashooter, self.plant)

    """
    Faire les méthodes de ticking et tout ici et pas dans la boucle principale (fausse POO)
    """

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingPeashooter.
        """
        if current_tick - self.lastly_shot >= self.ps_plant.pea_launch_cooldown:
            for shot in range(self.ps_plant.amount_of_peas):
                zombie = self.lane.get_zombie()
                if zombie and zombie.x >= self.x:
                    zombie.damage(self.ps_plant.pea_damage)
            self.lastly_shot = current_tick

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        text = ""
        if self.lane.get_zombie() != None:
            text = f"{self.ps_plant.name.upper()} ({round(self.ps_plant.pea_launch_cooldown - (monotonic() - self.lastly_shot), 1)})"
        else:
            text = f"{self.ps_plant.name.upper()}"

        if self.health < self.health_scale:
            text += f" [{round(self.health / self.health_scale * 100)}%]"

        return text