from __future__ import annotations

from tkinter import Button, Frame
from time import monotonic

from entities.plantsClass import Plant

class PlantSelector(Button):
    def __init__(self,
                 master: Frame,
                 plant: Plant | None,
                 player: "Player"):
        super().__init__(master)
        self.player = player
        self.plant = plant
        self.default_color = 'green'
        self.hovered_color = 'yellow'
        self.last_used: float = 0

        self.configure(
            bg=self.default_color,
            width=15,
            height=3,
            borderwidth=1,
        )

        if self.plant is None:
            self['text'] = "Unstack"
        else:
            self['text'] = self.plant.name

    def update_selector(self, current_tick: float, last_tick: float) -> None:
        """
        Docstring
        """
        if self.player.selected_plant == self:
            self['bg'] = self.hovered_color
        else:
            self['bg'] = self.default_color

        if self.plant is None:
            return

        if monotonic() - self.last_used > self.plant.cooldown:
            self.configure(
                text=f"{self.plant.name} [{self.plant.cost}]",
            )
        else:
            self.configure(
                text=f"{self.plant.name} [{self.plant.cost}] {round(self.plant.cooldown - (current_tick - self.last_used), 1)}",
                bg='gray'
            )

        if self == self.player.selected_plant:
            if self.player.suns.get() >= self.plant.cost:
                self.configure(bg=self.hovered_color)
            else:
                self.configure(bg='red')