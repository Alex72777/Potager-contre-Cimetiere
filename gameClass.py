from tkinter import Tk, Frame, Label
from playerClass import Player, SelectablePlant, Slot
from zombiesClass import Zombie
from entityClass import LivingPlant, LivingZombie, Lawnmoyer
from time import time

class Game(Tk):
    def __init__(self, 
                 difficulty_rating: float = 1,
                 board_height: int = 5,
                 board_width: int = 10):
        super().__init__()
        self.difficulty_rating = difficulty_rating
        self.board_height = board_height
        self.board_width = board_width
        self.plant_selectors: list[SelectablePlant] = []
        self.waves: dict[int, list[Zombie]] = {}
        self.board = []
        self.speed = 1
        self.living_plants: list[LivingPlant | Lawnmoyer] = []
        self.living_zombies: list[LivingZombie] = []
        
        self.player = Player(self)
    
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
        placeholder_label = Label(deck_frame, textvariable=self.player.suns)
        placeholder_label.pack(fill='x', side='bottom')
        
        for plant in self.player.unlocked_plants:
            btn = SelectablePlant(deck_frame, plant)
            btn.configure(command= lambda btn = btn: self.player.select_plant(btn))
            btn.pack()
            self.plant_selectors.append(btn)
        
        deck_frame.pack(side='left', fill='y')
        board_frame.pack(side='left')
        
        game_frame.pack(fill='both', expand=True)
        
        self.after(1, lambda: self.tick(time()))
        self.mainloop()
    
    def tick(self, last_tick):
        dt = time() - last_tick
        
        for plant_selector in self.plant_selectors:
            if time() - plant_selector.last_used > plant_selector.plant.cooldown:
                plant_selector.configure(
                    text=plant_selector.plant.name,
                    bg=plant_selector.default_color
                )
            else:
                plant_selector.configure(
                    text=f"{plant_selector.plant.name} {round(plant_selector.plant.cooldown - (time() - plant_selector.last_used), 1)}"
                )
        
        self.after(1, lambda: self.tick(time()))