from typing import cast
from math import floor

from livingentities.livingplants.livingplantClass import LivingPlant

from entities.plantsClass import Plant, Landmine

from ui.slot import Slot

class LivingLandmine(LivingPlant):
	def __init__(self, plant: Plant, slot: Slot, master: "Game", is_invulnerable: bool = True) -> None:
		super().__init__(plant=plant, slot=slot, master=master, is_invulnerable=is_invulnerable)
		self.ll_plant = cast(Landmine, plant)
		self.radius = self.ll_plant.radius
		self.explosion_damage = self.ll_plant.explosion_damage
		self.countdown_time = self.ll_plant.countdown_time
		self.primed_at = 0
		self.is_primed = False
		self.has_blown = False
		self.blink = 0
		self.explosion_timestamp = 0

	def _explode(self, current_tick: float) -> None:
		zombie = self.lane.get_zombie()
		while zombie != None and self.x - self.radius <= zombie.x <= self.x + self.radius:
			zombie.kill()
		self.explosion_timestamp = current_tick

	def update(self, current_tick: float, last_tick: float) -> None:
		if self.is_primed:
			return

		zombie = self.lane.get_zombie()

		if zombie != None and self.x - self.radius <= zombie.x <= self.x + self.radius:
			self.is_primed = True
			self.primed_at = current_tick

		if current_tick - self.primed_at > self.countdown_time and not self.has_blown:
			self.has_blown = True
			self._explode(current_tick)

	def sous_texte(self, current_tick: float, last_tick: float) -> str:
		text = self.name.upper()
		if self.is_primed:
			text += f" {round(current_tick - self.primed_at, 1)}"

		return text

	def ui_update(self, current_tick: float, last_tick: float) -> dict:

		if self.is_primed and not self.has_blown:
			if current_tick - self.blink > .5:
				self.blink = current_tick
				return {"content": {floor(self.x): {"bg": "orange"}}, "priority": 2}
		elif self.has_blown and current_tick - self.explosion_timestamp:
			return {"content": {"-1": {"bg": "orange"}, "+1": {"bg": "orange"}}, "priority": 2}

		return {}
