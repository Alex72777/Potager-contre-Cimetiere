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
        self.default_foreground_color = "black"
        self.ui_updated_priority = 0

        self.configure(bg=self.default_color,
                       width=20,
                       height=8,
                       borderwidth=0)

    def update_text(self, current_tick: float, last_tick: float) -> None:
        """Updates button text accordingly to plant and/or zombies on it."""
        game = self.lane.player.master
        if self.ui_updated_priority == 0:
            self.configure(bg=self.default_color, fg=self.default_foreground_color)
        slot_text = ""
        ui_conf = {"content": {}, "priority": 0}

        lawnmoyer = self.lane.lawnmoyer
        if lawnmoyer != None and self.x <= lawnmoyer.x < self.x + 1:
            lawnmoyer_conf = lawnmoyer.ui_update(current_tick, last_tick)
            if lawnmoyer_conf['priority'] > ui_conf['priority']:
                ui_conf = lawnmoyer_conf
            slot_text += lawnmoyer.sous_texte()

        if self.taken_by != None:
            plant_ui_conf = self.taken_by.ui_update(current_tick, last_tick)

            if not "priority" in plant_ui_conf.keys():
                plant_ui_conf["priority"] = 0

            if plant_ui_conf["priority"] > ui_conf["priority"]:
                ui_conf = plant_ui_conf

            slot_text += self.taken_by.sous_texte(current_tick, last_tick)

        for zombie in self.lane.zombies:
            if self.x <= zombie.x < self.x + 1:
                slot_text += " {} ".format(zombie.sous_texte(current_tick, last_tick))

                zombie_ui_conf = zombie.ui_update(current_tick, last_tick)

                if not "priority" in zombie_ui_conf.keys():
                    zombie_ui_conf["priority"] = 0

                if zombie_ui_conf["priority"] > ui_conf["priority"]:
                    ui_conf = zombie_ui_conf

        for event in game.events.values():
            # print(event.event_name, event.state)
            event_ui_conf: dict = event.ui_conf
            if event.priority > ui_conf["priority"] and self.pos in event_ui_conf.keys():
                ui_conf['content'][self.x] = event_ui_conf[self.pos]
        # print(ui_conf)
        self["text"] = slot_text
        self._ui_update(ui_conf)
        self.ui_updated_priority = 0

    def _ui_update(self, options: dict) -> None:
        """
        {"content": {"-1": {"bg": "red"}, "+1": {"bg": "red"}, pos.x: {"bg": "red"}}, "priority": 1}
        """
        valid_options = ["bg", "fg"]
        if not "content" in options.keys():
            return

        cursors: dict[int, dict] = {}
        for opt, val in options['content'].items():
            if not str(opt).isdigit() and opt[0] == "+":
                for i in range(self.x, min(self.lane.len_slots, self.x + int(opt[1:]) + 1)):
                    if not i in cursors:
                        cursors[i] = val
            elif not str(opt).isdigit() and opt[0] == "-":
                for i in range(self.x, max(0, self.x - int(opt[1:])) - 1, -1):
                    if not i in cursors:
                        cursors[i] = val
            else:
                if not int(opt) in cursors:
                    cursors[int(opt)] = val

        # print(cursors)
        for i, content in cursors.items():
            # i: 0 content: {"bg": "purple"}
            # print(i, content)
            for opt, val in content.items():
                # opt: "bg" val: "purple"
                # print(opt)
                self.lane.slots[i][opt] = val
                self.lane.slots[i].ui_updated_priority = options["priority"]

    @property
    def pos(self) -> tuple[int, int]:
        """Returns tuple as: (y, x)"""
        return (self.lane.y, self.x)