from dataclasses import dataclass, field
from tkinter import Button, Frame, IntVar, Tk, DoubleVar
from time import monotonic
from math import floor
from typing import TYPE_CHECKING

from plantsClass import Plant, PLANTS, Sunflower, Peashooter
from lawnmoyersClass import Lawnmoyer

from livingentities.livingplants import livingplantClass, livingPeashooter, livingSunflower
from livingentities.livingzombies import livingzombieClass
from livingentities.livinglawnmoyers import livinglawnmoyerClass

from ui.plantselector import PlantSelector

if TYPE_CHECKING:
    from gameClass import Game

@dataclass
class Player:
    """
    class Player
     master: app Tkinter
     unlocked_plants: list[Plant] Liste des plantes disponibles à l'usage dès le début de la partie
     selected_plants: PlantSelector | None Pointe vers le bouton sélecteur de la plante, None le cas échéant
     SUNS_EARN_RATE: int La quantité de soleis reçus par le joueur toutes les SUNS_COOLDOWN secondes
     SUNS_COOlDOWN: int Le temps qui s'écoule avant que le joueur reçoive des soleils automatiquement
     DEFAULT_SUNS: int La quantité de départ de soleils du joueur

     select_plant() -> None : appelée lorsque le joueur sélectionne un PlantSelector dans son deck
     add_suns(suns: int) -> None : ajoute 'suns' soleils au joueur.
    """

    master: Tk
    unlocked_plants: list[Plant] = field(default_factory=lambda: list(PLANTS.values()))
    selected_plant: PlantSelector | None = None
    SUNS_EARN_RATE = 25
    SUNS_COOLDOWN = 10 # seconds
    DEFAULT_SUNS = 1000

    def __post_init__(self):
        self.suns = IntVar(self.master, self.DEFAULT_SUNS)
        self.suns_earn_cooldown = DoubleVar(self.master, self.SUNS_COOLDOWN)
        self.lastly_earned_suns = monotonic()

    def select_plant(self, selectable_plant: PlantSelector) -> None:
        time_elapsed: float = monotonic() - selectable_plant.last_used
        if time_elapsed < selectable_plant.plant.cooldown:
            return

        if self.selected_plant and self.selected_plant == selectable_plant:
            self.selected_plant = None
        else:
            self.selected_plant = selectable_plant

    def add_suns(self, suns: int) -> None:
        self.suns.set(max(0, self.suns.get() + suns))

    def update(self, current_tick: float, last_tick: float) -> None:
        if monotonic() - self.lastly_earned_suns >= self.SUNS_COOLDOWN:
            self.add_suns(self.SUNS_EARN_RATE)
            self.lastly_earned_suns = current_tick
        else:
            self.suns_earn_cooldown.set(round(self.SUNS_COOLDOWN - (current_tick - self.lastly_earned_suns), 1))