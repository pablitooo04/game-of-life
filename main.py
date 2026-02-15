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


def auto_loop() -> None:
    """
    Simple function to scroll through generations.
    """
    try:
        if auto_mode:
            I1.compute_next_generation()
            root.after(1, auto_loop)
    except KeyboardInterrupt:
        exit(1)


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

        for i in range(len(self.matrix) + 1):
            pos = int(i * self.gap)
            canvas.create_line(pos, 0, pos, self.size, fill="#C7C6C6")
            canvas.create_line(0, pos, self.size, pos, fill="#C7C6C6")

        for n_ligne in range(len(self.matrix)):
            for n_case in range(len(self.matrix)):
                if self.matrix[n_ligne][n_case] != 0:
                    canvas.create_rectangle(
                        int(n_case * self.gap),
                        int(n_ligne * self.gap),
                        int((n_case + 1) * self.gap),
                        int((n_ligne + 1) * self.gap),
                        fill=dico_couleurs[self.matrix[n_ligne][n_case]],
                        outline="#C7C6C6"
                    )

        canvas.place(x=0, y=0)

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
        self.draw_grid(self.matrix)

    def draw_grid(self, current_matrix: list[list[int]]) -> None:
        """Redraw the grid on the canvas based on the given matrix."""
        canvas.delete("all")
        for i in range(len(self.matrix) + 1):
            pos = int(i * self.gap)
            canvas.create_line(pos, 0, pos, self.size, fill="#C7C6C6")
            canvas.create_line(0, pos, self.size, pos, fill="#C7C6C6")

        self.new_matrix = current_matrix
        for n_line in range(len(self.new_matrix)):
            for n_col in range(len(self.new_matrix)):
                if self.new_matrix[n_line][n_col] != 0:
                    canvas.create_rectangle(
                        int(n_col * self.gap),
                        int(n_line * self.gap),
                        int((n_col + 1) * self.gap),
                        int((n_line + 1) * self.gap),
                        fill=dico_couleurs[self.new_matrix[n_line][n_col]],
                        outline="#C6C6C6"
                    )

    def toggle_edit(self) -> None:
        """Toggle edit mode and update the canvas background.

        Edit mode can only be changed when automatic mode is disabled.
        """
        if not auto_mode:
            if not I1.edit_mode:
                self.edit_mode = True
                canvas.configure(bg="#7799d1")
            else:
                self.edit_mode = False
                canvas.configure(bg="#f6f6f6")

    def set_random_grid(self):
        """
        Set a random grid pressing the 'r' key.

        all cell has a chance of 50% to be alive.
        """

        self.matrix = np.random.randint(
            0, 2, (len(self.matrix), len(self.matrix)))
        self.draw_grid(self.matrix)


def on_click(event: tk.Event) -> None:
    """
    Handle a left-click on the grid.

    If edit mode is disabled, compute the next generation.
    If edit mode is enabled, activate the clicked cell.
    """
    if not auto_mode:
        if not I1.edit_mode:
            I1.compute_next_generation()
        else:
            cell = (
                min(int(event.x / I1.gap), len(I1.matrix[0]) - 1),
                min(int(event.y / I1.gap), len(I1.matrix) - 1),
            )
            I1.matrix[cell[1]][cell[0]] = 1

            canvas.create_rectangle(
                int(cell[0]*I1.gap),
                int(cell[1]*I1.gap),
                int((cell[0]+1)*I1.gap),
                int((cell[1]+1)*I1.gap),
                fill=dico_couleurs[1]
            )


def toggle_auto_mode(event: tk.Event):
    """
    Toggle automatic simulation mode handling spacebar press.

    Automatic mode can only be enabled when edit mode is disabled.
    """
    global auto_mode
    if not I1.edit_mode:
        auto_mode = not auto_mode
        if auto_mode:
            auto_loop()


if __name__ == "__main__":
    # === Proprities ===

    dico_couleurs = {
        0: "#FFFFFF",
        1: "#000000",
    }

    auto_mode = False

    matrix_size = 250

    window_size = 1000

    # === Config ===

    root = tk.Tk()
    root.geometry(f"{window_size}x{window_size}")
    root.resizable(False, False)
    root.title("Conway’s Game of Life")

    icon = tk.PhotoImage(file="assets/icon.png")
    root.iconphoto(True, icon)

    canvas = tk.Canvas(width=window_size, height=window_size)

    matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]

    I1 = Interface(matrix, window_size)

    # === Binds ===

    root.bind("<space>", toggle_auto_mode)
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Button-3>", lambda event: I1.toggle_edit())
    root.bind("r", lambda event: I1.set_random_grid())

    # === Run ===

    root.mainloop()
