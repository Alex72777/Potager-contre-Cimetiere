from typing import Literal
from random import randint
from time import monotonic
from tkinter import StringVar

from events.eventClass import Event

from entities.zombiesClass import Zombie, ZOMBIES

from livingentities.livingzombies.livingzombieClass import LivingZombie

from ui.lane import Lane

class Waves(Event):
    def __init__(self,
                 game,
                 event_name: str,
                 grace_period: float = 15,
                 wave_interval: float = 20,
                 boss_wave_interval: int = 5,
                 min_zombie_spawn_interval: float = 1,
                 max_zombie_spawn_interval: float = 30,
                 max_wave_duration: float = 90,
                 min_zombie_hp: int = 1000,
                 state: Literal['disabled'] | Literal['paused'] | Literal['enabled'] | Literal[-1] | Literal[0] | Literal[1] = 'disabled') -> None:
        super().__init__(game=game, event_name=event_name, state=state, priority=5)
        self.added_at = monotonic()

        self.grace_period = grace_period
        self.wave_interval = wave_interval
        self.min_zombie_spawn_interval = min_zombie_spawn_interval
        self.max_zombie_spawn_interval = max_zombie_spawn_interval
        self.boss_wave_interval = boss_wave_interval
        self.max_wave_duration = max_wave_duration
        
        self.wave_count = 0
        self.wave_began_timestamp = 0
        self.wave_ended_timestamp = 0
        self.has_last_wave_ended = True

        self.min_zombie_hp = min_zombie_hp
        self.total_zombie_hp = 0
        self.last_zombie_spawn_timestamp = 0
        self.zombie_stack = []
        self.total_zombie = 0
        self.zombie_spawn_interval = 0

        self.debug_stats = {
            'wave_count': StringVar(game, name='Wave count'),
            'ongoing_wave_timer': StringVar(game, name='Wave timer'),
            'next_wave_timer': StringVar(game, name='Next Wave In'),
            'remaining_zombie': StringVar(game, name='Remaining zombies'),
            'total_zombie_wave': StringVar(game, name='Total Zombie Wave'),
            'total_zombie_hp': StringVar(game, name='Total Zombie HP'),
            'min_zombie_hp': StringVar(game, value= '%d' % self.min_zombie_hp, name='Minimal Wave Zombie HP'),
            'is_boss_wave': StringVar(game, name='Is Boss Wave'),
            'has_wave_ended': StringVar(game, name='Has Wave Ended'),
            'grace_period': StringVar(game, name='Grace Period'),
            'zombie_spawn_interval': StringVar(game, name='Zombie Spawning Interval'),
            'wave_interval': StringVar(game, value= '%.1f' % self.wave_interval, name='Wave Interval'),
            'max_wave_duration': StringVar(game, value='%.1f' % self.max_wave_duration, name='Maximum Wave Duration')
        }


    def update(self, current_tick: float, last_tick: float) -> None:
        # Min difficulty : 1000 zombie hp + each living plants hp
        self._update_debug_stats(current_tick)
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
            self.zombie_stack.clear()
        
        if self.has_last_wave_ended and current_tick - self.wave_ended_timestamp > self.wave_interval: # new wave after interval or on first enabled event
            # make new zombie stack 
            self.wave_count += 1
            self.zombie_stack = self.make_zombie_stack()
            self.zombie_spawn_interval = min(self.max_zombie_spawn_interval, max(self.min_zombie_spawn_interval, self.max_wave_duration / len(self.zombie_stack)))
            self.has_last_wave_ended = False
            self.wave_began_timestamp = current_tick
            print("new wave incoming, interval is %.2f" % self.zombie_spawn_interval)
    
    def make_zombie_stack(self) -> list[Zombie]:
        max_zombie_hp = self.min_zombie_hp
        max_zombie_hp += self.game.player.sum_livingplant_hp
        self.total_zombie_hp = max_zombie_hp
        print("making new waves with %d HP" % max_zombie_hp)

        all_zombies = []
        if self.wave_count % self.boss_wave_interval == 0:
            all_zombies = list(ZOMBIES.values())
        else:
            for zombie in ZOMBIES.values():
                if not zombie.is_boss:
                    all_zombies.append(zombie)
        
        all_zombies.sort(reverse=True, key=self._sort_zombie_by_hp)

        # algo glouton

        new_zombies = []
        for zombie in all_zombies:
            while max_zombie_hp >= zombie.health:
                new_zombies.append(zombie)
                max_zombie_hp -= zombie.health
        
        self.total_zombie = len(new_zombies)
        print("new wave counts %d zombies" % len(new_zombies))
        return new_zombies

    def _update_debug_stats(self, current_tick: float) -> None:
        for stat in self.debug_stats.keys():
            if hasattr(self, '_update_%s' % stat):
                getattr(self, '_update_%s' % stat)(current_tick, stat)

    def _update_wave_count(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('%d' % self.wave_count)
    
    def _update_ongoing_wave_timer(self, current_tick, stat_name) -> None:
        if not self.has_last_wave_ended:
            self.debug_stats[stat_name].set(round(self.max_wave_duration - (current_tick - self.wave_began_timestamp), 1))
        else:
            self.debug_stats[stat_name].set('0')
    
    def _update_next_wave_timer(self, current_tick, stat_name) -> None:
        if self.has_last_wave_ended:
            self.debug_stats[stat_name].set('%.1f' % (current_tick + self.wave_interval - self.wave_ended_timestamp))
        else:
             self.debug_stats[stat_name].set('0')
    
    def _update_remaining_zombie(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('%d' % len(self.zombie_stack))
    
    def _update_total_zombie_wave(self, current_tick, stat_name) -> None: 
        self.debug_stats[stat_name].set('%d' % self.total_zombie)
    
    def _update_total_zombie_hp(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('%d' % self.total_zombie_hp)
    
    def _update_is_boss_wave(self, current_tick, stat_name) -> None:
        if self.wave_count % self.boss_wave_interval == 0:
            self.debug_stats[stat_name].set('Yes')
        else:
            self.debug_stats[stat_name].set('No')
    
    def _update_has_wave_ended(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('Yes' if self.has_last_wave_ended else 'No')
    
    def _update_grace_period(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('%.1f' % max(0, self.added_at + self.grace_period - current_tick))
    
    def _update_zombie_spawn_interval(self, current_tick, stat_name) -> None:
        self.debug_stats[stat_name].set('%.1f' % self.zombie_spawn_interval)
    
    def _on_enable(self) -> None:
        super()._on_enable()
        if self.grace_period > 0:
            print("for this time, waves have a grace period of %.1f seconds" % self.grace_period)

    def _sort_zombie_by_hp(self, val: Zombie) -> int:
        return val.health
