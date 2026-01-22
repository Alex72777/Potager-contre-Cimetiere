from dataclasses import dataclass, field
from plantsClass import Plant, PLANTS, Sunflower, Peashooter
from entityClass import Lawnmoyer, LivingLawnmoyer, LivingPlant, LivingZombie, LivingSunflower, LivingPeashooter
from tkinter import Button, Frame, IntVar, Tk
from time import monotonic
from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameClass import Game

class PlantSelector(Button):
    def __init__(self,
                 master: Frame,
                 plant: Plant,
                 player: Player):
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
            text=self.plant.name,
        )
    
    def update(self, current_tick: int, last_tick: int) -> None:
        """
        Docstring
        """
        if monotonic() - self.last_used > self.plant.cooldown:
            plant_selector.configure(
                text=f"{self.plant.name} [{self.plant.cost}]",
                bg=self.default_color if self.player.selected_plant != plant_selector else plant_selector.hovered_color
            )
        else:
            self.configure(
                text=f"{self.plant.name} [{self.plant.cost}] {round(self.plant.cooldown - (current_tick - self.last_used), 1)}"
            )

        if self == self.player.selected_plant:
            if self.player.suns.get() >= self.plant.cost:
                self.configure(bg=self.hovered_color)
            else:
                self.configure(bg='red')

class Slot(Button):
    def __init__(self,
                 master: Frame,
                 x: int,
                 lane: "Lane",
                 taken_by: LivingPlant | None = None,):
        super().__init__(master)
        self.taken_by = taken_by
        self.x = x
        self.lane = lane
        self.default_color = ("green2" if self.x % 2 else 'chartreuse3')

        self.configure(bg=self.default_color,
                       width=20,
                       height=8,
                       borderwidth=0)

    def update_text(self) -> None:
        """Updates button text accordingly to plant and/or zombies on it."""
        slot_text = ""
        if self.taken_by != None:
            slot_text += self.taken_by.sous_texte()
        
        for zombie in self.lane.zombies:
            if self.x < zombie.x <= self.x + 1:
                slot_text += ", {}".format(zombie.sous_texte())

    def place_plant(self, game: "Game") -> None:
        if not game.player.selected_plant:
            return

        if self.lane.len_plantes >= self.lane.len_slots:
            return

        if game.player.suns.get() < game.player.selected_plant.plant.cost:
            return

        plant: Plant = game.player.selected_plant.plant
        new_living_plant = None
        if isinstance(plant, Sunflower):
            new_living_plant = LivingSunflower(plant, self, game)

        if isinstance(plant, Peashooter):
            new_living_plant = LivingPeashooter(plant, self, game)

        print("Nouvelle plante:", new_living_plant) # debug
        if new_living_plant == None:
            return

        game.player.add_suns(-(plant.cost))

        game.player.selected_plant.last_used = monotonic()
        game.player.selected_plant = None

class HouseSlot(Button):
    def __init__(self,
                 master: Frame,
                 lane: Lane,
                 taken_by: Lawnmoyer | None,
                 entities: list[LivingZombie] = []) -> None:
        super().__init__(master)
        self.taken_by = taken_by
        self.entities = entities
        self.lane = lane

        self.configure(bg='dimgray',
                       width=20,
                       height=8,
                       borderwidth=0,
                       text=(self.taken_by.name.upper() if self.taken_by else ""))

@dataclass
class Lane:
    """
    Classe contenant la pile des zombies et la pile des plantes.
    """
    house_slot: HouseSlot
    y: int
    slots: list[Slot] = field(default_factory= lambda: [])
    plantes: list[LivingPlant] = field(default_factory= lambda: [])
    zombies: list[LivingZombie] = field(default_factory= lambda: [])

    def release_lawnmoyer(self) -> None:
        """
        Docstring
        """
        pass

    def append_slot(self, slot: Slot) -> None:
        self.slots.append(slot)

    def empiler_zombie(self, zombie: LivingZombie) -> None:
        """
        Docstring
        """
        self.zombies.append(zombie)

    def empiler_plante(self, plante: LivingPlant) -> None:
        """
        Docstring
        """
        plante.slot.taken_by = plante
        self.plantes.append(plante)

    def depiler_zombie(self) -> LivingZombie | None:
        """
        Docstring
        """
        if self.len_zombie == 0:
            return None
        
        val: LivingZombie = self.zombies.pop()
        return val

    def depiler_plante(self) -> LivingPlant | None:
        """
        Docstring
        """
        if self.len_plantes == 0:
            return None
        
        val: LivingLawnmoyer | LivingPlant = self.plantes.pop()
        if isinstance(val, LivingLawnmoyer):
            return None
        
        return val

    def get_zombie(self) -> LivingZombie | None:
        if len(self.zombies) == 0:
            return None

        return self.zombies[-1]

    def get_plante(self) -> LivingPlant | None:
        if len(self.plantes) == 0:
            return None

        return self.plantes[-1]
    
    @property
    def len_zombie(self) -> int:
        return len(self.zombies)

    @property
    def len_plantes(self) -> int:
        return len(self.plantes)

    @property
    def len_slots(self) -> int:
        return len(self.slots)

    # def next_plant_from(self, zombie: LivingZombie) -> LivingPlant | None: # Nul! faire pile pour les plantes
    #     for i in range(floor(zombie.x), 0, -1):
    #         if self.slots[i].taken_by:
    #             living_plant = cast(LivingPlant, self.slots[i].taken_by)
    #             return living_plant


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
    unlocked_plants = field(default_factory=lambda: list(PLANTS.values()))
    selected_plant: PlantSelector | None = None
    SUNS_EARN_RATE = 25
    SUNS_COOLDOWN = 10 # seconds
    DEFAULT_SUNS = 100

    def __post_init__(self):
        self.suns = IntVar(self.master, self.DEFAULT_SUNS)
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
    
    def update(self, current_tick: int, last_tick: int) -> None:
        if monotonic() - self.lastly_earned_suns >= self.SUNS_COOLDOWN:
            self.add_suns(self.SUNS_EARN_RATE)
            self.lastly_earned_suns = current_tick
        else:
            ### Fix suns earn cooldown label ###
            self.suns_earn_cooldown.set(round(self.player.SUNS_COOLDOWN - (current_tick - self.player.lastly_earned_suns), 1))