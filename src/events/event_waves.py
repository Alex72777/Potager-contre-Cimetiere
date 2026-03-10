from typing import Literal
from random import randint
from time import monotonic

from events.eventClass import Event

from entities.zombiesClass import Zombie, ZOMBIES, BOSSES

from livingentities.livingzombies.livingzombieClass import LivingZombie

from ui.lane import Lane

class Waves(Event):
    def __init__(self,
                 game,
                 event_name: str,
                 grace_period: float = 15,
                 wave_interval: float = 20,
                 min_zombie_spawn_interval: float = 1,
                 max_zombie_spawn_interval: float = 30,
                 max_wave_duration: float = 90,
                 min_zombie_hp: int = 1000,
                 per_plant_zombie_hp: int = 250,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        self.added_at = monotonic()

        self.grace_period = grace_period
        self.wave_interval = wave_interval
        self.min_zombie_spawn_interval = min_zombie_spawn_interval
        self.max_zombie_spawn_interval = max_zombie_spawn_interval
        self.max_wave_duration = max_wave_duration
        
        self.wave_began_timestamp = 0
        self.wave_ended_timestamp = 0
        self.has_last_wave_ended = True

        self.per_plant_zombie_hp = per_plant_zombie_hp
        self.min_zombie_hp = min_zombie_hp
        self.total_zombie_hp = 0
        self.last_zombie_spawn_timestamp = 0
        self.zombie_stack = []


    def update(self, current_tick: float, last_tick: float) -> None:
        # 1 plant <> 250 zombie hp
        # Min difficulty : 1000 zombie hp
        if self.state != 1 or current_tick - self.added_at < self.grace_period:
            return
        
        if current_tick - self.wave_began_timestamp <= self.max_wave_duration and not self.has_last_wave_ended: # ongoing wave and not expired
            if len(self.zombie_stack) > 0 and current_tick - self.last_zombie_spawn_timestamp > self.zombie_spawn_interval: # more zombies to come and can spawn
                lanes: list[Lane] = self.game.board
                random_lane = lanes[randint(0, len(lanes) - 1)]

                spawning_zombie = self.zombie_stack.pop() # stack logic
                random_lane.enfiler_zombie(LivingZombie(spawning_zombie, random_lane.width, random_lane, self.game, is_boss=spawning_zombie.is_boss))
                self.last_zombie_spawn_timestamp = current_tick
                print("new zombie seen at lane %d!" % random_lane.y)
            
            if len(self.zombie_stack) == 0: # no more :>
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
            self.zombie_spawn_interval = min(self.max_zombie_spawn_interval, max(self.min_zombie_spawn_interval, self.max_wave_duration / len(self.zombie_stack)))
            self.has_last_wave_ended = False
            self.wave_began_timestamp = current_tick
            print("new wave incoming, interval is %.2f" % self.zombie_spawn_interval)
    
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