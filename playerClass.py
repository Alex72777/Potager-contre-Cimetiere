from dataclasses import dataclass, field
from plantsClass import Plant, PEASHOOTER
from entityClass import Lawnmoyer, LivingPlant, LivingZombie
from tkinter import Button, Frame, IntVar, Tk
from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameClass import Game

class SelectablePlant(Button):
    def __init__(self,
                 master: Frame,
                 plant: Plant):
        super().__init__(master)
        self.plant = plant
        self.default_color = 'green'
        self.hovered_color = 'yellow'
        self.last_used: float = 0
        
        self.configure(
            bg=self.default_color,
            width=10,
            height=2,
            borderwidth=1,
            text=self.plant.name,
        )

class Slot(Button):
    def __init__(self,
                 master: Frame,
                 x: int,
                 y: int,
                 pos: tuple,
                 taken_by: LivingPlant | None = None,
                 entities: list[LivingPlant | LivingZombie | Lawnmoyer] = []):
        super().__init__(master)
        self.taken_by = taken_by
        self.entities = entities
        self.x, self.y = x, y
        self.pos = pos
        
        self.configure(bg="green2" if self.x % 2 else 'chartreuse3',
                       width=10,
                       height=3,
                       borderwidth=0)
    
    def place_plant(self, game: "Game"):
        if not game.player.selected_plant:
            return
        
        if self.taken_by:
            return
        
        plant = game.player.selected_plant.plant
        new_living_plant = LivingPlant(plant)
        
        game.player.suns.set(game.player.suns.get() - plant.cost)
        
        slot_text = str.upper(plant.name)
        for entity in self.entities:
            slot_text += " " + entity.name
        
        self.configure(text=slot_text)
        game.living_plants.append(new_living_plant)
        
        game.player.selected_plant.configure(
                bg='grey'
            )
        
        game.player.selected_plant.last_used = time()
        game.player.selected_plant = None

@dataclass
class Player:
    master: Tk
    unlocked_plants: list[Plant] = field(default_factory=lambda: [PEASHOOTER, PEASHOOTER, PEASHOOTER])
    selected_plant: SelectablePlant | None = None
    
    def __post_init__(self):
        self.suns = IntVar(self.master, 100)
    
    def select_plant(self, selectable_plant: SelectablePlant):
        time_elapsed = time() - selectable_plant.last_used
        if time_elapsed < selectable_plant.plant.cooldown:
            return
        
        if self.selected_plant:
            self.selected_plant.configure(
                bg=self.selected_plant.default_color
            )
            self.selected_plant = None
        
        can_place_plant = self.suns.get() >= selectable_plant.plant.cost and time() - selectable_plant.last_used >= selectable_plant.plant.cooldown
        
        self.selected_plant = selectable_plant
        selectable_plant.configure(
            bg=selectable_plant.hovered_color if can_place_plant else 'red'
        )
