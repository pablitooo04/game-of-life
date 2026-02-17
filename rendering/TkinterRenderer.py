import tkinter as tk

from simulation import Simulation
from time import time
from rendering.BaseRenderer import BaseRenderer

class TkinterRenderer(BaseRenderer):
    def __init__(self, simulation: Simulation) -> None:
        self.simulation = simulation
        self.edit_mode: bool = False
        self.root = tk.Tk()

        self.window_size = (1920, 1080)
        self.gap: float = 50
        self.canvas_size = (self.gap*self.simulation.grid.size[0], self.gap*self.simulation.grid.size[1])
        self.canvas = tk.Canvas(width=self.window_size[0], height=self.window_size[1])
        self.canvas.place(x=0, y=0)
        self.colors = {
            0: "#FFFFFF",
            1: "#AA0000",
        }
        self.canvas.configure(bg=self.colors[0])

        self.root.bind("<space>", self.toggle_auto_mode)
        self.root.bind("r", lambda event: self.simulation.grid.set_random_grid())
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.toggle_edit)

        self.edit_on_img = tk.PhotoImage(file="assets/edit_on.png")
        self.edit_off_img = tk.PhotoImage(file="assets/edit_off.png")
        self.play_img = tk.PhotoImage(file="assets/play.png")
        self.stop_img = tk.PhotoImage(file="assets/stop.png")

        self.auto_mode = False
        self.gen_per_second = 999999
        self.last_frame_time = time()
        self.fps = 0
        self.display_grid()
        self.root.mainloop()

    
    def display_grid(self) -> None:
        self.canvas.delete("all")
        x_cells, y_cells = self.simulation.grid.size

        for x in range(x_cells + 1):
            px = x * self.gap
            self.canvas.create_line(px, 0, px, y_cells * self.gap, fill="#C6C6C6")

        for y in range(y_cells + 1):
            py = y * self.gap
            self.canvas.create_line(0, py, x_cells * self.gap, py, fill="#C6C6C6")
    
    def draw_buttons(self):
        if self.edit_mode:
            self.canvas.create_image(
                15, 15, image=self.edit_on_img, anchor="nw")
        else:
            self.canvas.create_image(
                15, 15, image=self.edit_off_img, anchor="nw")

        if self.auto_mode:
            self.canvas.create_image(
                15 + 128 + 15, 15, image=self.play_img, anchor="nw")
        else:
            self.canvas.create_image(
                15 + 128 + 15, 15, image=self.stop_img, anchor="nw")


    def toggle_edit(self, event=None) -> None:
        """Toggle edit mode and update the canvas background.

        Edit mode can only be changed when automatic mode is disabled.
        """
        if not self.auto_mode:
            if not self.edit_mode:
                self.edit_mode = True
                self.canvas.configure(bg="#7799d1")
            else:
                self.edit_mode = False
                self.canvas.configure(bg=self.colors[0])

        if self.edit_mode:
            self.canvas.create_image(
                15, 15, image=self.edit_on_img, anchor="nw")
        else:
            self.canvas.create_image(
                15, 15, image=self.edit_off_img, anchor="nw")
    
    def toggle_auto_mode(self, event=None):
        """
        Toggle automatic simulation mode handling spacebar press.

        Automatic mode can only be enabled when edit mode is disabled.
        """
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.canvas.create_image(
                15 + 128 + 15, 15, image=self.play_img, anchor="nw")
            self.auto_loop()
        else:
            self.canvas.create_image(
                15 + 128 + 15, 15, image=self.stop_img, anchor="nw")

    
    def on_click(self, event: tk.Event) -> None:
        if not self.edit_mode:
            self.simulation.compute_next_generation()
            self.display_grid()
        else:
            x_cells, y_cells = self.simulation.grid.size

            cell_x = min(event.x // self.gap, x_cells - 1)
            cell_y = min(event.y // self.gap, y_cells - 1)

            cell_value = self.simulation.grid.get_cell((cell_x, cell_y))
            self.simulation.grid.set_cell((cell_x, cell_y), int(not bool(cell_value)))

            self.canvas.create_rectangle(
                cell_x * self.gap,
                cell_y * self.gap,
                (cell_x + 1) * self.gap,
                (cell_y + 1) * self.gap,
                outline="#C6C6C6",
                fill="#7799d1" if cell_value else self.colors[1]
            )
