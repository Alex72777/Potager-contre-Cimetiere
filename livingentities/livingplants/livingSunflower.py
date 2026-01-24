from livingentities.livingplants import livingplantClass
from plantsClass import Sunflower
from time import monotonic

class LivingSunflower(livingplantClass.LivingPlant):
    def __init__(self, plant: "Sunflower", slot: "Slot", master: "Game"):
        if not isinstance(plant, Sunflower):
            raise TypeError("LivingSunflower requires a Sunflower class instance")

        super().__init__(plant=plant, slot=slot, master=master)
        self.lastly_produced: float = monotonic() - self.plant.suns_cooldown + 5 # Timestamp of last production
        self.blinked_slot: float = 0 # used for the production notification (timestamp)

    def update(self, current_tick: float, last_tick: float) -> None:
        """
        Méthode de ticking pour la classe LivingSunflower.
        """
        sf_plant: Sunflower = self.plant
        if current_tick - self.lastly_produced >= sf_plant.suns_cooldown:
            self.master.player.add_suns(sf_plant.suns_income)
            self.lastly_produced = current_tick
            self.blinked_slot = current_tick

    def sous_texte(self, current_tick: float, last_tick: float) -> str:
        sf_plant: Sunflower = self.plant
        text = f"{self.name.upper()} ({round(sf_plant.suns_cooldown - (monotonic() - self.lastly_produced), 1)})"

        if self.health < self.health_scale:
            text += f" [{round(self.health / self.health_scale * 100)}%]"

        return text

    def ui_update(self, current_tick: float, last_tick: float) -> dict:
        """
        Pour changer la couleur ici
        """
        if current_tick - self.blinked_slot >= 1:
            return {"bg": self.slot.default_color, "priority": 1}
        else:
            return {"bg": "yellow", "priority": 1}