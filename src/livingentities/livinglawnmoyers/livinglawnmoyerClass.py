from dataclasses import dataclass
from time import monotonic
from random import choice
from math import floor

from entities.lawnmoyersClass import Lawnmoyer

@dataclass
class LivingLawnmoyer:
    lawnmoyer: Lawnmoyer
    lane: "Lane"
    destroys_everything: bool = False

    def __post_init__(self):
        self.name = self.lawnmoyer.name
        self.speed = self.lawnmoyer.speed
        self.x = 0
        self.key_time = 0
        self.bg = ""
        self.direction = 1

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingLawnmoyer.
        """
        dt = current_tick - last_tick
        self.x = max(0, min(self.lane.len_slots, self.x + self.speed * dt * self.direction))

        zombie = self.lane.get_zombie()
        while zombie != None and zombie.x <= self.x and self.direction > 0:
            zombie.kill()
            zombie = self.lane.get_zombie()

        if self.destroys_everything and self.direction < 0:
            plante = self.lane.get_plante()
            if plante != None and self.x <= plante.x:
                plante.kill()

        if self.x == self.lane.len_slots and self.destroys_everything == True:
            self.direction = -1

        if ((self.x == self.lane.len_slots and self.destroys_everything == False)
            or (self.x == 0 and self.direction < 0 and self.destroys_everything == True)):
            self.lane.lawnmoyer = None
            del self

    def sous_texte(self) -> str:
        """
        Docstring
        """
        return self.name.upper() + " "

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Docstring
        """
        if current_tick - self.key_time >= .05:
            self.bg = choice(['blue', 'red', 'pink', 'yellow', 'green', 'purple'])
            self.key_time = current_tick
        return {"content": {floor(self.x): {"bg": self.bg}}, "priority": 3}