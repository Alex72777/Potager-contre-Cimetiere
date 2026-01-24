from typing import cast

from livingentities.livingplants.livingplantClass import LivingPlant

from entities.plantsClass import Plant, Wallnut

from ui.slot import Slot

class LivingWallnut(LivingPlant):
  def __init__(self, plant: Plant, slot: Slot, master: "Game"):
    super().__init__(master=master, plant=plant, slot=slot)
    self.wn_plant = cast(Wallnut, plant)

  def update(self, current_tick: float, last_tick: float) -> None:
    return super().update(current_tick, last_tick)

  def sous_texte(self, current_tick: float, last_tick: float) -> str:
    text = self.name.upper() + f" [{round(self.health / self.health_scale * 100)}%]"
    return text

  def ui_update(self, current_tick: float, last_tick: float) -> dict:
    healh = self.health / self.health_scale
    if healh <= .1:
      return {"content": {self.slot.x: {"bg": "red"}}, "priority": 1}
    elif healh <= .25:
      return {"content": {self.slot.x: {"bg": "orange"}}, "priority": 1}
    else:
      return {}