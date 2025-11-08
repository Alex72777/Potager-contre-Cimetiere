from tkinter import Tk, Button, Frame
from dataclasses import dataclass
from playerClass import Player
from plantsClass import Plant
from entityClass import Entity, Lawnmoyer, LivingPlant
from time import time

class Game(Tk):
    def __init__(self, 
                 player: Player,
                 difficulty_rating: float = 1,
                 board_height: int = 5,
                 board_width: int = 10):
        super().__init__()
        self.player = player
        self.difficulty_rating = difficulty_rating
        self.board_height = board_height
        self.board_width = board_width
        self.waves = []
        self.board = []
        self.speed = 1
    
    def set_waves(self, waves: dict[int, list[Plant]] | None):
        if waves:
            self.waves = waves
        else:
            self.waves = []
    
    def draw(self):
        board_frame = Frame(self, bg='grey')
        board_frame.grid(row=0, column=1)
        self.rowconfigure(list(range(0, self.board_height, 2)), pad=10)
        
        board: list[list[Slot]] = []
        for y in range(self.board_height):
            board.append([])
            for x in range(self.board_width):
                slot = Slot(board_frame, x, y, (x, y))
                slot.grid(column=x, row=y)
                board[y].append(slot)
        self.board = board
        
        deck_frame = Frame(self, bg='grey')
        deck_frame.grid()
        
        self.after(1, lambda: self.tick(time()))
        self.mainloop()
    
    def tick(self, last_tick):
        self.after(1, lambda: self.tick(time()))
        

class Slot(Button):
    def __init__(self,
                 master: Frame,
                 x: int,
                 y: int,
                 pos: tuple,
                 taken_by: LivingPlant | None = None,
                 entities: list[Entity | Lawnmoyer | None] = []):
        super().__init__()
        self.master = master
        self.taken_by = taken_by
        self.entities = entities
        self.x, self.y = x, y
        self.pos = pos
        
        self.configure(bg="green", width=10, height=3)