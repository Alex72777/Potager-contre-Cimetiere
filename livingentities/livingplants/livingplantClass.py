from dataclasses import dataclass
from typing import TYPE_CHECKING

from entities.plantsClass import Plant

from ui.slot import Slot

@dataclass
class LivingPlant:
    master: "Game"
    plant: Plant
    slot: Slot

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
        ui_update
        """
        return {"priority": 0}