try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter module not found!")
    exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy module not found!")
    exit(1)

from time import time


class Interface:
    def __init__(self, matrix: list[list[int]], size: int) -> None:
        """Initialize the interface and draw the initial grid.

        Args:
            matrix (list[list[int]]): Initial state of the grid.
            size (int): Size of the canvas in pixels.
        """
        self.matrix: list[list[int]] = matrix
        self.size: int = size
        self.edit_mode: bool = False
        self.gap: float = self.size/len(self.matrix)
        self.edit_on_img = tk.PhotoImage(file="assets/edit_on.png")
        self.edit_off_img = tk.PhotoImage(file="assets/edit_off.png")
        self.play_img = tk.PhotoImage(file="assets/play.png")
        self.stop_img = tk.PhotoImage(file="assets/stop.png")
        self.auto_mode = False
        self.gen_per_second = 999999
        self.last_frame_time = time()
        self.fps = 0
        self.colors = {
            0: "#FFFFFF",
            1: "#000000",
        }
        self.canvas = tk.Canvas(width=window_size, height=window_size)
        self.canvas.configure(bg=self.colors[0])

        self.draw_grid()

        self.canvas.place(x=0, y=0)

    def get_neighbors(self, cell: tuple[int, int]) -> int:
        """Return the neighbors count of a cell.

        Args:
            C (tuple[int, int]): Coordinates of the target cell (row, col).

        Returns:
            int: the neighbors count of a cell.
        """
        neighbors = 0

        for diff_x in [-1, 0, 1]:
            for diff_y in [-1, 0, 1]:
                if (
                    cell[0]+diff_x in range(0, len(self.matrix))
                    and cell[1] + diff_y in range(0, len(self.matrix))
                    and not (diff_x == 0 and diff_y == 0)
                    and self.matrix[cell[0] + diff_x][cell[1] + diff_y] == 1
                ):
                    neighbors += 1

        return neighbors

    def compute_next_generation(self):

        grid = np.array(self.matrix, dtype=int)

        neighbors = (
            np.roll(np.roll(grid,  1, 0),  1, 1) +
            np.roll(np.roll(grid,  1, 0),  0, 1) +
            np.roll(np.roll(grid,  1, 0), -1, 1) +
            np.roll(np.roll(grid,  0, 0),  1, 1) +
            np.roll(np.roll(grid,  0, 0), -1, 1) +
            np.roll(np.roll(grid, -1, 0),  1, 1) +
            np.roll(np.roll(grid, -1, 0),  0, 1) +
            np.roll(np.roll(grid, -1, 0), -1, 1)
        )

        new_grid = ((neighbors == 3) | (
            (grid == 1) & (neighbors == 2))).astype(int)

        self.matrix = new_grid.tolist()
        self.draw_grid()

    def draw_grid(self) -> None:
        """Redraw the grid on the canvas based on the given matrix."""
        self.canvas.delete("all")
        for i in range(len(self.matrix) + 1):
            pos = int(i * self.gap)
            self.canvas.create_line(pos, 0, pos, self.size, fill="#C6C6C6")
            self.canvas.create_line(0, pos, self.size, pos, fill="#C6C6C6")

        self.new_matrix = self.matrix
        for n_line in range(len(self.new_matrix)):
            for n_col in range(len(self.new_matrix)):
                if self.new_matrix[n_line][n_col] != 0:
                    self.canvas.create_rectangle(
                        int(n_col * self.gap),
                        int(n_line * self.gap),
                        int((n_col + 1) * self.gap),
                        int((n_line + 1) * self.gap),
                        fill=self.colors[self.new_matrix[n_line][n_col]],
                        outline="#C6C6C6"
                    )

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

    def set_random_grid(self):
        """
        Set a random grid pressing the 'r' key.

        all cell has a chance of 50% to be alive.
        """

        self.matrix = np.random.randint(
            0, 2, (len(self.matrix), len(self.matrix)))
        self.draw_grid()

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

    def auto_loop(self):
        if not self.auto_mode:
            return

        # Calcul du temps écoulé
        now = time()
        dt = now - self.last_frame_time
        self.last_frame_time = now

        # Calcul FPS (évite division par zéro)
        if dt > 0:
            self.fps = 1 / dt

        # Affichage dans le titre
        root.title(f"Conway’s Game of Life — {self.fps:.2f} FPS")

        # Next frame
        self.compute_next_generation()
        root.after(
            int(1000/self.gen_per_second) +
            int(not bool(int(1000/self.gen_per_second))),
            self.auto_loop
        )

    def on_click(self, event: tk.Event) -> None:
        """
        Handle a left-click on the grid.

        If edit mode is disabled, compute the next generation.
        If edit mode is enabled, activate the clicked cell.
        """

        if not self.edit_mode:
            self.compute_next_generation()
        else:
            cell = (
                min(int(event.x / self.gap), len(self.matrix[0]) - 1),
                min(int(event.y / self.gap), len(self.matrix) - 1),
            )
            self.matrix[cell[1]][cell[0]] = 1

            self.canvas.create_rectangle(
                int(cell[0]*I1.gap),
                int(cell[1]*I1.gap),
                int((cell[0]+1)*I1.gap),
                int((cell[1]+1)*I1.gap),
                fill=self.colors[1]
            )


if __name__ == "__main__":
    # === Proprities ===

    matrix_size = 500

    window_size = 1000

    # === Config ===

    root = tk.Tk()
    root.geometry(f"{window_size}x{window_size}")
    root.resizable(False, False)
    root.title("Conway’s Game of Life")

    icon = tk.PhotoImage(file="assets/icon.png")
    root.iconphoto(True, icon)

    matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    I1 = Interface(matrix, window_size)

    # === Binds ===

    root.bind("<space>", I1.toggle_auto_mode)
    root.bind("r", lambda event: I1.set_random_grid())
    I1.canvas.bind("<Button-1>", I1.on_click)
    I1.canvas.bind("<Button-3>", I1.toggle_edit)

    # === Run ===

    root.mainloop()
