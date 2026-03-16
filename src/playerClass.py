from dataclasses import dataclass, field
from tkinter import IntVar, DoubleVar
from time import monotonic

from entities.plantsClass import Plant, PLANTS

from ui.plantselector import PlantSelector

@dataclass
class Player:
    """
    class Player
     master: app Tkinter
     unlocked_plants: list[Plant] Liste des plantes disponibles à l'usage dès le début de la partie
     selected_plants: PlantSelector | None Pointe vers le bouton sélecteur de la plante, None le cas échéant
     amount_living_plants : int Nombre de plantes vivantes, permet une difficulté croissante des vagues
     SUNS_EARN_RATE: int La quantité de soleis reçus par le joueur toutes les SUNS_COOLDOWN secondes
     SUNS_COOlDOWN: int Le temps qui s'écoule avant que le joueur reçoive des soleils automatiquement
     DEFAULT_SUNS: int La quantité de départ de soleils du joueur

     select_plant() -> None : appelée lorsque le joueur sélectionne un PlantSelector dans son deck
     add_suns(suns: int) -> None : ajoute 'suns' soleils au joueur.
    """

    master: "Game"
    unlocked_plants: list[Plant] = field(default_factory=lambda: list(PLANTS.values()))
    selected_plant: PlantSelector | None = None
    suns_earn_rate: int = 25
    suns_cooldown: int = 10 # seconds
    default_suns: int = 1000

    def __post_init__(self):
        self.suns = IntVar(self.master, self.default_suns)
        self.suns_earn_cooldown = DoubleVar(self.master, self.suns_cooldown)
        self.lastly_earned_suns = monotonic()

        self.amount_living_plants: int = 0 
        self.sum_livingplant_hp: int = 0
        self.killed_zombies: int = 0
        self.killed_bosses: int = 0

    def select_plant(self, selectable_plant: PlantSelector) -> None:
        time_elapsed: float = monotonic() - selectable_plant.last_used
        if selectable_plant.plant and time_elapsed < selectable_plant.plant.cooldown:
            return

        if self.selected_plant and self.selected_plant == selectable_plant:
            self.selected_plant = None
        else:
            self.selected_plant = selectable_plant

    def add_suns(self, suns: int) -> None:
        self.suns.set(max(0, self.suns.get() + suns))

    def update(self, current_tick: float, last_tick: float) -> None:
        if current_tick - self.lastly_earned_suns >= self.suns_cooldown:
            self.add_suns(self.suns_earn_rate)
            self.lastly_earned_suns = current_tick
        else:
            self.suns_earn_cooldown.set(round(self.suns_cooldown - (current_tick - self.lastly_earned_suns), 1))