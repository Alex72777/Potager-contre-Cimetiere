from dataclasses import dataclass
from time import monotonic
from random import choice

from lawnmoyersClass import Lawnmoyer

@dataclass
class LivingLawnmoyer:
    lawnmoyer: Lawnmoyer
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