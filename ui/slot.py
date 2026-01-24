from tkinter import Button, Frame

class Slot(Button):
    def __init__(self,
                 master: Frame,
                 x: int,
                 lane: "Lane",
                 taken_by: "LivingPlant | None" = None,):
        super().__init__(master)
        self.taken_by = taken_by
        self.x = x
        self.lane = lane
        self.default_color = ("green2" if self.x % 2 else 'chartreuse3')

        self.configure(bg=self.default_color,
                       width=20,
                       height=8,
                       borderwidth=0)

    def update_text(self, current_tick: float, last_tick: float) -> None:
        """Updates button text accordingly to plant and/or zombies on it."""
        slot_text = ""
        ui_conf = {}

        lawnmoyer = self.lane.lawnmoyer
        #lawn_ui_conf = lawn_ui_conf.ui_update(current_tick, last_tick)
        if lawnmoyer != None and self.x <= lawnmoyer.x < self.x + 1:
            ui_conf = lawnmoyer.ui_update(current_tick, last_tick)
            slot_text += lawnmoyer.sous_texte()

        if not "priority" in ui_conf.keys():
            ui_conf["priority"] = 0

        if self.taken_by != None:
            plant_ui_conf = self.taken_by.ui_update(current_tick, last_tick)
            if plant_ui_conf["priority"] > ui_conf["priority"]:
                ui_conf = plant_ui_conf

            slot_text += self.taken_by.sous_texte(current_tick, last_tick)
        else:
            self.configure(bg=self.default_color)

        if not "priority" in ui_conf.keys():
            ui_conf["priority"] = 0

        for zombie in self.lane.zombies:
            if self.x < zombie.x <= self.x + 1:
                slot_text += " {} ".format(zombie.sous_texte(current_tick, last_tick))

                zombie_ui_conf = zombie.ui_update(current_tick, last_tick)

                if not "priority" in zombie_ui_conf.keys():
                    zombie_ui_conf["priority"] = 0

                if zombie_ui_conf["priority"] > ui_conf["priority"]:
                    ui_conf = zombie_ui_conf

        self["text"] = slot_text
        self._ui_update(ui_conf)

    def _ui_update(self, options: dict) -> None:
        valid_options = ["bg", "fg"]
        for opt, val in options.items():
            if opt in valid_options:
                self[opt] = val