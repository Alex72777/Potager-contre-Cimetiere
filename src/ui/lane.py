from dataclasses import dataclass, field
from tkinter import Frame
from time import monotonic

from entities.plantsClass import PLANTS_CLASSES, Plant
from entities.lawnmoyersClass import Lawnmoyer

from livingentities.livingplants.livingplantClass import LivingPlant
from livingentities.livingplants.livingPeashooter import LivingPeashooter
from livingentities.livingplants.livingSunflower import LivingSunflower
from livingentities.livingplants.livingWallnut import LivingWallnut
from livingentities.livingplants.livinglandmine import LivingLandmine

from livingentities.livingzombies.livingzombieClass import LivingZombie
from livingentities.livinglawnmoyers.livinglawnmoyerClass import LivingLawnmoyer

from ui.slot import Slot
from ui.houseslot import HouseSlot

from playerClass import Player

@dataclass
class Lane:
    """
    Classe contenant la pile des zombies et la pile des plantes.
    """
    y: int
    player: Player
    house_frame: Frame
    slots: list[Slot] = field(default_factory= lambda: [])
    plantes: list[LivingPlant] = field(default_factory= lambda: [])
    zombies: list[LivingZombie] = field(default_factory= lambda: [])
    lawnmoyer: LivingLawnmoyer | None = None

    def __post_init__(self) -> None:

        self.house_slot = HouseSlot(self.house_frame, self, taken_by=Lawnmoyer())
        self.house_slot.grid(row=self.y, column=0)

    def release_lawnmoyer(self, destroy_everything: bool = False) -> None:
        """
        Libère la tondeuse de som emplacement pour la rendre vivante.
        """
        if self.house_slot.taken_by != None:
            lawnmoyer = LivingLawnmoyer(self.house_slot.taken_by, self, destroys_everything=destroy_everything)
            self.house_slot.taken_by = None
            self.lawnmoyer = lawnmoyer
            # self.player.master.

    def dig_up_plant(self) -> None:
        plante = self.get_plante()
        if plante == None:
            return

        self.player.add_suns(round(plante.plant.cost / 2))
        self.depiler_plante()

    def append_slot(self, slot: Slot) -> None:
        self.slots.append(slot)

    def enfiler_zombie(self, zombie: LivingZombie) -> None:
        """
        Ajoute un zombie dans la file.
        """
        self.zombies.append(zombie)
        print("Apparition de", zombie.name)

    def empiler_plante(self, plante: LivingPlant) -> None:
        """
        Empile une plante dans la file.
        """
        plante.slot.taken_by = plante
        self.plantes.append(plante)

    def defiler_zombie(self) -> None:
        """
        Défile un zombie de la file.
        """
        if self.len_zombie == 0:
            return None

        val: LivingZombie = self.zombies.pop(0)
        print(val.name, "tué.")
        del val

    def depiler_plante(self) -> None:
        """
        Dépile une plante de la pile.
        """
        if self.len_plantes == 0:
            return

        val: LivingPlant = self.plantes.pop()
        print(val.name, "tuée.")
        val.slot.taken_by = None
        del val

    def get_zombie(self) -> LivingZombie | None:
        """
        Renvoie le premier zombie de la file.
        """
        if len(self.zombies) == 0:
            return None

        for i in range(self.len_zombie):
            if self.zombies[i].health > 0:
                return self.zombies[i]

    def get_plante(self) -> LivingPlant | None:
        """
        Renvoie la première plante de la file
        """
        if len(self.plantes) == 0:
            return None

        return self.plantes[-1]

    def place_plant(self) -> None:
        """
        Logique ajout plante
        """
        game = self.player.master
        if not game.player.selected_plant or game.has_ended:
            return

        if self.len_plantes >= self.len_slots:
            return
        slot = self.slots[self.len_plantes]

        if game.player.suns.get() < game.player.selected_plant.plant.cost:
            return

        plant: Plant = game.player.selected_plant.plant
        new_living_plant: LivingPlant | None = None
        if isinstance(plant, PLANTS_CLASSES['sunflower']):
            new_living_plant = LivingSunflower(plant, slot, game)

        if isinstance(plant, PLANTS_CLASSES['peashooter']):
            new_living_plant = LivingPeashooter(plant, slot, game)

        if isinstance(plant, PLANTS_CLASSES['wallnut']):
            new_living_plant = LivingWallnut(plant, slot, game)

        if isinstance(plant, PLANTS_CLASSES['landmine']):
            new_living_plant = LivingLandmine(plant, slot, game)

        if new_living_plant == None:
            return
        print("Nouvelle plante:", new_living_plant.name) # debug

        game.player.add_suns(-(plant.cost))
        self.empiler_plante(new_living_plant)

        game.player.selected_plant.last_used = monotonic()
        game.player.selected_plant = None

    @property
    def len_zombie(self) -> int:
        return len(self.zombies)

    @property
    def len_plantes(self) -> int:
        return len(self.plantes)

    @property
    def len_slots(self) -> int:
        return len(self.slots)