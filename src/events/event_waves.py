from typing import Literal
from time import monotonic

from events.eventClass import Event
from entities.zombiesClass import Zombie, ZOMBIES, BOSSES
from ui.lane import Lane

class Waves(Event):
    def __init__(self,
                 game,
                 event_name: str,
                 wave_interval: float = 10,
                 zombie_spawn_interval: float = 5,
                 max_wave_duration: float = 60,
                 min_zombie_hp: int = 1000,
                 per_plant_zombie_hp: int = 250,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        self.wave_interval = wave_interval
        self.zombie_spawn_interval = zombie_spawn_interval
        self.max_wave_duration = max_wave_duration
        
        self.creation_time = monotonic()
        self.wave_began_timestamp = 0
        self.wave_ended_timestamp = 0
        self.has_last_wave_ended = False

        self.per_plant_zombie_hp = per_plant_zombie_hp
        self.min_zombie_hp = min_zombie_hp
        self.total_zombie_hp = 0
        self.last_zombie_spawn_timestamp = 0
        self.zombie_stack = []


    def update(self, current_tick: float, last_tick: float) -> None:
        # 1 plant <> 250 zombie hp
        # Min difficulty : 1000 zombie hp
        if self.state != 1:
            return
        
        if current_tick - self.wave_began_timestamp <= self.max_wave_duration and not self.has_last_wave_ended: # ongoing wave
            if len(self.zombie_stack) > 0: # more zombies to come
                pass
            else: # no more :>
                self.wave_ended_timestamp = current_tick
                self.has_last_wave_ended = True
                print("a zombie wave has ended. (before max duration)")
                print("a zombie wave will begin in {} seconds".format(
                    (self.wave_interval + (self.wave_began_timestamp + self.max_wave_duration  - current_tick))
                ))

        elif current_tick - self.wave_began_timestamp > self.max_wave_duration and not self.has_last_wave_ended: # wave duration expired
            print("a zombie wave has ended. (exceeded max duration)")
            self.wave_ended_timestamp = current_tick
            self.has_last_wave_ended = True
        
        if self.has_last_wave_ended and current_tick - self.wave_ended_timestamp > self.wave_interval: # new wave after interval
            # make new zombie stack 
            self.zombie_stack = self.make_zombie_stack()
            self.has_last_wave_ended = False
            self.wave_began_timestamp = current_tick
    
    def make_zombie_stack(self) -> list[Zombie]:
        max_zombie_hp = self.min_zombie_hp
        max_zombie_hp += self.game.player.amount_living_plants * self.per_plant_zombie_hp
        print("making new waves with %d HP" % max_zombie_hp)

        all_zombies = list(ZOMBIES.values()) + list(BOSSES.values())
        all_zombies.sort(reverse=True, key=self._sort_zombie_by_hp)

        # algo glouton

        new_zombies = []
        for zombie in all_zombies:
            while max_zombie_hp >= zombie.health:
                new_zombies.append(zombie)
                max_zombie_hp -= zombie.health
        
        print("new wave counts %d zombies" % len(new_zombies))
        return new_zombies

    def _sort_zombie_by_hp(self, val: Zombie) -> int:
        return val.health