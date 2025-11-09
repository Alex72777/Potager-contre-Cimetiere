from dataclasses import dataclass, field
from plantsClass import Plant, PLANTS, Sunflower, Peashooter
from entityClass import Lawnmoyer, RollingLawnmoyer, LivingPlant, LivingZombie, LivingSunflower, LivingPeashooter
from tkinter import Button, Frame, IntVar, Tk
from time import time
from math import floor
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from gameClass import Game

class PlantSelector(Button):
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
            width=15,
            height=3,
            borderwidth=1,
            text=self.plant.name,
        )

class Slot(Button):
    def __init__(self,
                 master: Frame,
                 x: int,
                 y: int,
                 pos: tuple,
                 lane: "Lane",
                 taken_by: LivingPlant | None = None,):
        super().__init__(master)
        self.taken_by = taken_by
        self.x, self.y = x, y
        self.pos = pos
        self.lane = lane
        self.default_color = "green2" if self.x % 2 else 'chartreuse3'
        
        self.configure(bg=self.default_color,
                       width=20,
                       height=8,
                       borderwidth=0)
    
    def place_plant(self, game: "Game"):
        if not game.player.selected_plant:
            return
        
        if self.taken_by:
            return
        
        if game.player.suns.get() < game.player.selected_plant.plant.cost:
            return
        
        plant = game.player.selected_plant.plant
        new_living_plant = None
        if isinstance(plant, Sunflower):
            sf_plant = cast(Sunflower, plant)
            new_living_plant = LivingSunflower(sf_plant, self)
            new_living_plant.lastly_produced = time() - plant.suns_cooldown + 5
        
        if isinstance(plant, Peashooter):
            ps_plant = cast(Peashooter, plant)
            new_living_plant = LivingPeashooter(ps_plant, self)
        
        print(new_living_plant)
        if not new_living_plant:
            return
        
        self.taken_by = new_living_plant
        
        game.player.suns.set(game.player.suns.get() - plant.cost)
        
        game.player.selected_plant.configure(
                bg='grey'
            )
        
        game.player.selected_plant.last_used = time()
        game.player.selected_plant = None

class HouseSlot(Button):
    def __init__(self,
                 master: Frame,
                 taken_by: Lawnmoyer | None,
                 lane: "Lane | None" = None,
                 entities: list[LivingZombie] = []):
        super().__init__(master)
        self.taken_by = taken_by
        self.entities = entities
        self.lane = lane
        
        self.configure(bg='dimgray',
                       width=20,
                       height=8,
                       borderwidth=0,
                       text=self.taken_by.name.upper() if self.taken_by else "")

@dataclass
class Lane:
    house_slot: HouseSlot
    y: int
    lawnmoyer: RollingLawnmoyer | None = None
    slots: list[Slot] = field(default_factory= lambda: [])
    entities: list[LivingZombie] = field(default_factory= lambda: [])
    
    def append(self, slot: Slot):
        self.slots.append(slot)
    
    def _distance_key(self, entity: LivingZombie) -> float:
        return entity.x
    
    def get_entities(self) -> list[LivingZombie]:
        """Returns a list of living zombies sorted by their closeness to the house"""
        return sorted(self.entities, key=self._distance_key)

    @property
    def furthest_plant(self) -> LivingPlant | None:
        for i in range(len(self.slots) - 1, 0, -1):
            if self.slots[i].taken_by:
                living_plant = cast(LivingPlant, self.slots[i].taken_by)
                return living_plant

@dataclass
class Player:
    master: Tk
    unlocked_plants: list[Plant] = field(default_factory=lambda: list(PLANTS.values()))
    selected_plant: PlantSelector | None = None
    SUNS_EARN_RATE = 25 
    SUNS_COOLDOWN = 10 # seconds
    
    def __post_init__(self):
        self.suns = IntVar(self.master, 5000)
        self.lastly_earned_suns = time()
    
    def select_plant(self, selectable_plant: PlantSelector):
        time_elapsed = time() - selectable_plant.last_used
        if time_elapsed < selectable_plant.plant.cooldown:
            return
        
        if self.selected_plant and self.selected_plant == selectable_plant:
            self.selected_plant = None
        else:
            self.selected_plant = selectable_plant

    def add_suns(self, suns: int):
        self.suns.set(max(0, self.suns.get() + suns))