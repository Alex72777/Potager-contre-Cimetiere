from tkinter import Button, Frame

from lawnmoyersClass import Lawnmoyer

class HouseSlot(Button):
    def __init__(self,
                 master: Frame,
                 lane: "Lane",
                 taken_by: Lawnmoyer | None,) -> None:
        super().__init__(master)
        self.taken_by = taken_by
        self.lane = lane

        self.configure(bg='dimgray',
                       width=20,
                       height=8,
                       borderwidth=0,
                       text=(self.taken_by.name.upper() if self.taken_by else ""))

    def update(self, current_tick: float, last_tick: float) -> None:
        if self.taken_by != None:
            self.configure(text=self.taken_by.name.upper())
        else:
            self.configure(text='')