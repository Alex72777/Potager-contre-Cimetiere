from tkinter import Tk, Frame, Label, DoubleVar
from playerClass import Player, PlantSelector, Slot, Lane, HouseSlot
from plantsClass import Sunflower, Peashooter, Wallnut
from lawnmoyersClass import Lawnmoyer
from zombiesClass import Zombie, ZOMBIES
from livingentities.livingplants import livingPeashooter, livingplantClass, livingSunflower
from livingentities.livingzombies import livingzombieClass
from time import monotonic
from typing import cast
from math import floor

class Game(Tk):
    def __init__(self,
                 difficulty_rating: float = 1,
                 board_height: int = 5,
                 board_width: int = 9) -> None:
        super().__init__()
        self.player = Player(self)
        self.difficulty_rating = difficulty_rating
        self.board_height = board_height
        self.board_width = board_width
        self.plant_selectors: list[PlantSelector] = []
        self.waves: dict[int, list[Zombie]] = {}
        self.board: list[Lane] = []
        self.speed = 1

    def set_waves(self, waves: dict[int, list[Zombie]]) -> None:
        if waves:
            self.waves = waves
        else:
            self.waves = {}

    def end_game(self) -> None:
        #self.tick = None
        print("ded")
        pass

    def draw(self) -> None:
        game_frame = Frame(self, bg='gray64', padx=10, pady=10)

        board_frame = Frame(game_frame, bg='chartreuse4')
        house_frame = Frame(game_frame, bg='gray')

        for i in range(self.board_height):
            board_frame.rowconfigure(i, pad=10)
            house_frame.rowconfigure(i, pad=10)

        board: list[Lane] = []
        for y in range(self.board_height):
            new_lane = Lane(y, house_frame)
            board.append(new_lane)

            for x in range(self.board_width):
                slot = Slot(board_frame, x, new_lane)
                slot.configure(command = lambda game = self, lane = new_lane: lane.place_plant(game))
                slot.grid(column=x, row=y)
                new_lane.append_slot(slot)
        self.board = board
        self.board[2].enfiler_zombie(livingzombieClass.LivingZombie(ZOMBIES['classic_zombie'], 1, board[2], self))
        self.board[2].enfiler_zombie(livingzombieClass.LivingZombie(ZOMBIES['classic_zombie'], 7.5, board[2], self))
        deck_frame = Frame(game_frame, bg='grey', padx=5, pady=5)

        suns_label = Label(deck_frame, textvariable=self.player.suns)
        suns_label.pack(fill='x', side='bottom')

        suns_earn_cooldown_label = Label(deck_frame, textvariable=self.player.suns_earn_cooldown, bg='grey')
        suns_earn_cooldown_label.pack(fill='x', side='bottom')

        for plant in self.player.unlocked_plants:
            btn = PlantSelector(deck_frame, plant, self.player)
            btn.configure(command= lambda btn = btn: self.player.select_plant(btn))
            btn.pack()
            self.plant_selectors.append(btn)

        deck_frame.pack(side='left', fill='y')
        house_frame.pack(side='left')
        board_frame.pack(side='left')

        game_frame.pack(fill='both', expand=True)

        self.after(1, lambda: self.tick(monotonic()))
        self.mainloop()

    def tick(self, last_tick: float):
        current_tick = monotonic()
        # Plant selectors ticking

        for plant_selector in self.plant_selectors:
            plant_selector.update(current_tick, last_tick)

        # Player's passive suns income

        self.player.update(current_tick, last_tick)

        # Living entities ticking

        for lane in self.board:
            if lane.lawnmoyer != None:
                lane.lawnmoyer.update(current_tick, last_tick)

            for living_plant in lane.plantes:
                living_plant.update(current_tick, last_tick)

            for living_zombie in lane.zombies:
                living_zombie.update(current_tick, last_tick)

        # Slot update

        for lane in self.board:
            lane.house_slot.update(current_tick, last_tick)
            for slot in lane.slots:
                slot.update_text(current_tick, last_tick)

        self.after(1, lambda: self.tick(current_tick))
