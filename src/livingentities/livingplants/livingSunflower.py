from time import monotonic
from typing import cast
from math import floor

from livingentities.livingplants.livingplantClass import LivingPlant

from entities.plantsClass import Sunflower, Plant

from ui.slot import Slot

class LivingSunflower(LivingPlant):
    def __init__(self, plant: Plant, slot: Slot, master: "Game"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.sf_plant = cast(Sunflower, plant)
        self.lastly_produced: float = monotonic() - self.sf_plant.suns_cooldown + 5 # Timestamp of last production
        self.blinked_slot: float = 0 # used for the production notification (timestamp)

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingSunflower.
        """
        if current_tick - self.lastly_produced >= self.sf_plant.suns_cooldown:
            self.master.player.add_suns(self.sf_plant.suns_income)
            self.lastly_produced = current_tick
            self.blinked_slot = current_tick

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        text = f"{self.name.upper()} ({round(self.sf_plant.suns_cooldown - (monotonic() - self.lastly_produced), 1)})"

        if self.health < self.health_scale:
            text += f" [{round(self.health / self.health_scale * 100)}%]"

        return text

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Pour changer la couleur ici
        """
        if current_tick - self.blinked_slot < 1:
            return {"content": {self.slot.x: {"bg": "yellow"}}, "priority": 1}
        return {}