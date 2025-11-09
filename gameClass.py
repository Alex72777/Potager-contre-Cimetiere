from tkinter import Tk, Frame, Label, DoubleVar
from playerClass import Player, SelectablePlant, Slot
from zombiesClass import Zombie
from entityClass import LivingPlant, LivingZombie, LivingSunflower ,Lawnmoyer
from plantsClass import Sunflower
from time import time
from typing import cast

class Game(Tk):
    def __init__(self, 
                 difficulty_rating: float = 1,
                 board_height: int = 5,
                 board_width: int = 10):
        super().__init__()
        self.player = Player(self)
        self.difficulty_rating = difficulty_rating
        self.board_height = board_height
        self.board_width = board_width
        self.plant_selectors: list[SelectablePlant] = []
        self.suns_earn_cooldown = DoubleVar(self, value=self.player.SUNS_COOLDOWN)
        self.waves: dict[int, list[Zombie]] = {}
        self.board = []
        self.speed = 1
        self.living_plants: list[LivingPlant] = []
        self.living_zombies: list[LivingZombie] = []
        self.lawnmoyers: list[Lawnmoyer] = []
    
    def set_waves(self, waves: dict[int, list[Zombie]]):
        if waves:
            self.waves = waves
        else:
            self.waves = {}
    
    def draw(self):
        game_frame = Frame(self, bg='gray64', padx=10, pady=10)
        
        board_frame = Frame(game_frame, bg='chartreuse4')
        
        for i in range(self.board_height):
            board_frame.rowconfigure(i, pad=10)
        
        board: list[list[Slot]] = []
        for y in range(self.board_height):
            board.append([])
            for x in range(self.board_width):
                slot = Slot(board_frame, x, y, (x, y))
                slot.configure(command = lambda game = self, slot = slot: slot.place_plant(game))
                slot.grid(column=x, row=y)
                board[y].append(slot)
        self.board = board
        
        deck_frame = Frame(game_frame, bg='grey', padx=5, pady=5)
        
        suns_label = Label(deck_frame, textvariable=self.player.suns)
        suns_label.pack(fill='x', side='bottom')
        
        suns_earn_cooldown_label = Label(deck_frame, textvariable=self.suns_earn_cooldown, bg='grey')
        suns_earn_cooldown_label.pack(fill='x', side='bottom')
        
        for plant in self.player.unlocked_plants:
            btn = SelectablePlant(deck_frame, plant)
            btn.configure(command= lambda btn = btn: self.player.select_plant(btn))
            btn.pack()
            self.plant_selectors.append(btn)
        
        deck_frame.pack(side='left', fill='y')
        board_frame.pack(side='left')
        
        game_frame.pack(fill='both', expand=True)
        
        self.after(0, lambda: self.tick(time()))
        self.mainloop()
    
    def tick(self, last_tick: float):
        dt = time() - last_tick
        
        for plant_selector in self.plant_selectors:
            if time() - plant_selector.last_used > plant_selector.plant.cooldown:
                plant_selector.configure(
                    text=f"{plant_selector.plant.name} [{plant_selector.plant.cost}]",
                    bg=plant_selector.default_color if self.player.selected_plant != plant_selector else plant_selector.hovered_color
                )
            else:
                plant_selector.configure(
                    text=f"{plant_selector.plant.name} [{plant_selector.plant.cost}] {round(plant_selector.plant.cooldown - (time() - plant_selector.last_used), 1)}"
                )
            
            if plant_selector == self.player.selected_plant:
                if self.player.suns.get() >= plant_selector.plant.cost:
                    plant_selector.configure(bg=plant_selector.hovered_color)
                else:
                    plant_selector.configure(bg='red')
        
        if time() - self.player.lastly_earned_suns >= self.player.SUNS_COOLDOWN:
            self.player.add_suns(self.player.SUNS_EARN_RATE)
            self.player.lastly_earned_suns = time()
        else:
            self.suns_earn_cooldown.set(round(self.player.SUNS_COOLDOWN - (time() - self.player.lastly_earned_suns), 1))
        
        for living_plant in self.living_plants:
            if isinstance(living_plant, LivingSunflower): # Sunflowers
                plant: Sunflower = cast(Sunflower, living_plant.plant)
                if time() - living_plant.lastly_produced >= plant.suns_cooldown:
                    self.player.add_suns(plant.suns_income)
                    living_plant.lastly_produced = time()
                    living_plant.blinked_slot = time()
                
                if time() - living_plant.blinked_slot >= 1:
                    living_plant.slot.configure(bg=living_plant.slot.default_color)
                else:
                    living_plant.slot.configure(bg='yellow')
        
        self.after(1, lambda: self.tick(time()))