from typing import cast
from time import monotonic

from livingentities.livingplants.livingplantClass import LivingPlant

from entities.plantsClass import Plant, Landmine

from ui.slot import Slot

class LivingLandmine(LivingPlant):
	def __init__(self, plant: Plant, slot: Slot, master: "Game") -> None:
		super().__init__(plant=plant, slot=slot, master=master)
		self.ll_plant = cast(Landmine, plant)
		self.radius = self.ll_plant.radius
		self.explosion_damage = self.ll_plant.explosion_damage
		self.countdown_time = self.ll_plant.countdown_time
		self.primed_at = 0
		self.is_primed = False
		self.has_blown = False

	def _explode(self) -> None:
		pass

	def update(self, current_tick: float, last_tick: float) -> None:
		if self.is_primed:
			return

		zombie = self.lane.get_zombie()

		if zombie != None and self.x - self.radius <= zombie.x <= self.x + self.radius:
			self.is_primed = True
			self.primed_at = monotonic()

	def sous_texte(self, current_tick: float, last_tick: float) -> str:
		text = self.name.upper()
		if self.is_primed:
			text += f" {round(monotonic() + self.countdown_time - monotonic(), 1)}"

		return text

	def ui_update(self, current_tick: float, last_tick: float) -> dict:
		if self.is_primed and not self.has_blown:
			pass