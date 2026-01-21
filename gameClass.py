from tkinter import Tk, Frame, Label, DoubleVar
from playerClass import Player, PlantSelector, Slot, Lane, HouseSlot
from zombiesClass import Zombie, ZOMBIES
from entityClass import LivingPlant, LivingZombie, LivingSunflower, LivingPeashooter, Lawnmoyer
from plantsClass import Sunflower, Peashooter, Wallnut
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
        self.suns_earn_cooldown = DoubleVar(self, value=self.player.SUNS_COOLDOWN)
        self.waves: dict[int, list[Zombie]] = {}
        self.board: list[Lane] = []
        self.speed = 1
        self.lawnmoyers: list[Lawnmoyer] = []

    def set_waves(self, waves: dict[int, list[Zombie]]) -> None:
        if waves:
            self.waves = waves
        else:
            self.waves = {}

    def draw(self) -> None:
        game_frame = Frame(self, bg='gray64', padx=10, pady=10)

        house_frame = Frame(game_frame, bg='gray')
        board_frame = Frame(game_frame, bg='chartreuse4')

        for i in range(self.board_height):
            board_frame.rowconfigure(i, pad=10)
            house_frame.rowconfigure(i, pad=10)

        board: list[Lane] = []
        for y in range(self.board_height):
            house_slot = HouseSlot(house_frame, Lawnmoyer())
            house_slot.grid(row=y, column=0)
            new_lane = Lane(house_slot, y)
            new_lane.house_slot = house_slot
            board.append(new_lane)

            for x in range(self.board_width):
                slot = Slot(board_frame, x, new_lane)
                slot.configure(command = lambda game = self, slot = slot: slot.place_plant(game))
                slot.grid(column=x, row=y)
                new_lane.append_slot(slot)
        self.board = board
        # self.board[2].entities.append(LivingZombie(ZOMBIES['classic_zombie'], 7.5, board[2]))
        # self.board[2].entities.append(LivingZombie(ZOMBIES['classic_zombie'], 8, board[2]))
        deck_frame = Frame(game_frame, bg='grey', padx=5, pady=5)

        suns_label = Label(deck_frame, textvariable=self.player.suns)
        suns_label.pack(fill='x', side='bottom')

        suns_earn_cooldown_label = Label(deck_frame, textvariable=self.suns_earn_cooldown, bg='grey')
        suns_earn_cooldown_label.pack(fill='x', side='bottom')

        for plant in self.player.unlocked_plants:
            btn = PlantSelector(deck_frame, plant)
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
        current_tick = (monotonic())
        dt = current_tick - last_tick
        # Plant selectors ticking

        for plant_selector in self.plant_selectors:
            if monotonic() - plant_selector.last_used > plant_selector.plant.cooldown:
                plant_selector.configure(
                    text=f"{plant_selector.plant.name} [{plant_selector.plant.cost}]",
                    bg=plant_selector.default_color if self.player.selected_plant != plant_selector else plant_selector.hovered_color
                )
            else:
                plant_selector.configure(
                    text=f"{plant_selector.plant.name} [{plant_selector.plant.cost}] {round(plant_selector.plant.cooldown - (current_tick - plant_selector.last_used), 1)}"
                )

            if plant_selector == self.player.selected_plant:
                if self.player.suns.get() >= plant_selector.plant.cost:
                    plant_selector.configure(bg=plant_selector.hovered_color)
                else:
                    plant_selector.configure(bg='red')

        # Player's passive suns income

        if monotonic() - self.player.lastly_earned_suns >= self.player.SUNS_COOLDOWN:
            self.player.add_suns(self.player.SUNS_EARN_RATE)
            self.player.lastly_earned_suns = current_tick
        else:
            self.suns_earn_cooldown.set(round(self.player.SUNS_COOLDOWN - (current_tick - self.player.lastly_earned_suns), 1))

        # Living plants ticking

        for living_plant in self.living_plants:
            if isinstance(living_plant, LivingSunflower): # Sunflowers
                sf_plant: Sunflower = cast(Sunflower, living_plant.plant)
                if current_tick - living_plant.lastly_produced >= sf_plant.suns_cooldown:
                    self.player.add_suns(sf_plant.suns_income)
                    living_plant.lastly_produced = current_tick
                    living_plant.blinked_slot = current_tick

                living_plant.slot.configure(text=f"{living_plant.name.upper()} ({round(sf_plant.suns_cooldown - (monotonic() - living_plant.lastly_produced), 1)})")
                if current_tick - living_plant.blinked_slot >= 1:
                    living_plant.slot.configure(bg=living_plant.slot.default_color)
                else:
                    living_plant.slot.configure(bg='yellow')

            if isinstance(living_plant, LivingPeashooter): # Peashooters
                ps_plant: Peashooter = cast(Peashooter, living_plant.plant)
                if current_tick - living_plant.lastly_shot >= ps_plant.pea_launch_cooldown:
                    for shot in range(ps_plant.amount_of_peas):
                        lane_entities = living_plant.lane.get_entities()
                        if lane_entities and lane_entities[0].x >= living_plant.x:
                            lane_entities[0].damage(ps_plant.pea_damage)
                    living_plant.lastly_shot = current_tick

                if living_plant.lane.get_entities():
                    living_plant.slot.configure(text=f"{ps_plant.name.upper()} ({round(ps_plant.pea_launch_cooldown - (monotonic() - living_plant.lastly_shot), 1)})")
                else:
                    living_plant.slot.configure(text=f"{ps_plant.name.upper()}")

        # Living zombies ticking

        slot_text = ""
        for lane in self.board:
            for zombie in lane.get_entities():
                slot = zombie.lane.slots[floor(zombie.x)]
                if not slot.taken_by:
                    slot.configure(text='')

                if isinstance(zombie, LivingZombie):
                    next_plant = lane.next_plant_from(zombie)
                    if next_plant and next_plant.x <= zombie.x < next_plant.x + zombie.attack_range and current_tick - zombie.last_attacked >= zombie.attack_cooldown: # Attack range
                        next_plant.damage(zombie.attack_damage)
                        zombie.last_attacked = current_tick
                        print(zombie.health, next_plant.health)

                    if next_plant:
                        zombie.x = max(next_plant.x, zombie.x - zombie.speed * dt)
                    else:
                        zombie.x = max(0, zombie.x - zombie.speed * dt)

                    if zombie.x == 0:
                        # GAME OVER LOGIC or lawnmoyer
                        pass

                    if zombie:
                        if floor(zombie.x) < self.board_width - 1:
                            lane.slots[floor(zombie.x) + 1].configure(text='')
                        if not current_tick - zombie.last_attacked >= zombie.attack_cooldown:
                            slot_text += slot.cget('text') + f"{',' if slot.taken_by else ''}{zombie.name.upper()} [{round(zombie.health / zombie.health_scale * 100)}%] ({round(zombie.attack_cooldown - (monotonic() - zombie.last_attacked), 1)})"
                        else:
                            slot_text += slot.cget('text') + f"{',' if slot.taken_by else ''}{zombie.name.upper()} [{round(zombie.health / zombie.health_scale * 100)}%]"
                slot.configure(text=slot.cget('text') + slot_text)

        self.after(1, lambda: self.tick(current_tick))

    # @property
    # def living_plants(self) -> list[LivingPlant]:
    #     plants = []
    #     for lane in self.board:
    #         for slot in lane.slots:
    #             if slot.taken_by: plants.append(slot.taken_by)
    #     return plants

    # @property
    # def living_zombies(self) -> list[LivingZombie]:
    #     zombies = []
    #     for lane in self.board:
    #         zombies += lane.entities
    #     return zombies
