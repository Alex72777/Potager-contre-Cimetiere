from tkinter import Tk, Frame, Label
from time import monotonic

from playerClass import Player

from ui.plantselector import PlantSelector
from ui.lane import Lane
from ui.slot import Slot

from entities.zombiesClass import ZOMBIES

from events.eventClass import Event

from events.event_start_game import LaunchGame
from events.event_end_game import TerminateGame
from events.event_seizure import Seizure
from events.event_invoke_zombie import InvokeZombie
from events.event_waves import Waves

class Game(Tk):
    def __init__(self,
                 board_height: int = 5,
                 board_width: int = 8) -> None:
        super().__init__()
        self.player = Player(self,default_suns=500)
        self.board_height = board_height
        self.board_width = board_width
        self.plant_selectors: list[PlantSelector] = []
        self.board: list[Lane] = []
        self.events: dict[str, Event] = {
            "event_seizure": Seizure(event_name="seizure", game=self, elapse_time=.05),
            "event_invoke_zombie": InvokeZombie(
                event_name="invoke_zombie",
                game=self,
                zombie=ZOMBIES['boss_ogre'],
                interval=10
                ),
            "event_waves": Waves(event_name="zombie_waves", game=self),
            'event_start_game': LaunchGame(event_name="launch_game", game=self, priority=1),
            'event_end_game': TerminateGame(event_name="terminate_game", game=self, priority=1)
        }

    def draw(self) -> None:
        game_frame = Frame(self, bg='gray64', padx=10, pady=10)

        board_frame = Frame(game_frame, bg='chartreuse4')
        house_frame = Frame(game_frame, bg='gray')

        for i in range(self.board_height):
            board_frame.rowconfigure(i, pad=10)
            house_frame.rowconfigure(i, pad=10)

        board: list[Lane] = []
        for y in range(self.board_height):
            new_lane = Lane(y, self.player, house_frame)
            board.append(new_lane)

            for x in range(self.board_width):
                slot = Slot(board_frame, x, new_lane)
                slot.configure(command = lambda lane = new_lane: lane.interact_with())
                new_lane.house_slot.configure(command = lambda lane = new_lane: lane.interact_with())
                slot.grid(column=x, row=y)
                new_lane.append_slot(slot)
        self.board = board
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

        unstack_btn = PlantSelector(deck_frame, None, self.player)
        unstack_btn.pack(side='bottom')
        unstack_btn.configure(command= lambda btn = unstack_btn: self.player.select_plant(btn))
        self.plant_selectors.append(unstack_btn)

        deck_frame.pack(side='left', fill='y')
        house_frame.pack(side='left')
        board_frame.pack(side='left')

        game_frame.pack(fill='both', expand=True)
        
        # Debugging frame
        
        debug_frame = Frame(self)
        _ = 0
        row = 0
        col_max = 15
        for stat, var in self.events['event_waves'].debug_stats.items():
            Label(debug_frame, text=stat).grid(row=row, column=_)
            Label(debug_frame, textvariable=var).grid(row=row + 1, column=_)
            if _ >= col_max:
                _ = 0
                row += 2
            else:
                _ += 1
        
        debug_frame.pack(fill='x')

        self.events['event_start_game'].enable()
        self.after(1, lambda: self.tick(monotonic()))
        self.mainloop()

    def tick(self, last_tick: float):
        current_tick = monotonic()
        # Plant selectors ticking

        for plant_selector in self.plant_selectors:
            plant_selector.update_selector(current_tick, last_tick)

        # Slot update

        for lane in self.board:
            lane.house_slot.update_slot(current_tick, last_tick)
            for slot in lane.slots:
                slot.update_text(current_tick, last_tick)

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

        # Event handling

        for event in self.events.values():
            event.update(current_tick, last_tick)

        self.after(1, lambda: self.tick(current_tick))
