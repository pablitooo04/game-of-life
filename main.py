try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter module not found!")
    exit(1)


def auto_loop() -> None:
    """
    Simple function to scroll through generations.
    """
    if auto_mode:
        I1.compute_next_generation()
        root.after(1, auto_loop)


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

    def get_neighbors(self, cell: tuple[int, int])\
            -> tuple[list[tuple], dict[int, int]]:
        """Return the neighbors of a cell and the count of each type.

        Args:
            C (tuple[int, int]): Coordinates of the target cell (row, col).

        Returns:
            list: A list containing:
                - a list of neighbor coordinates
                - a dictionary counting occurrences of each cell type
        """
        neighbors: list[tuple[int, int]] = []
        dict_pop: dict = {0: 0, 1: 0}

        for addition_x in [-1, 0, 1]:
            for addition_y in [-1, 0, 1]:
                if (
                    cell[0]+addition_x in range(0, len(self.matrix))
                    and cell[1] + addition_y in range(0, len(self.matrix))
                    and (cell[0]+addition_x, cell[1]+addition_y) != cell
                ):
                    neighbors.append((cell[0]+addition_x, cell[1]+addition_y))

        for neighbor in neighbors:
            dict_pop[self.matrix[neighbor[0]][neighbor[1]]] += 1

        return (neighbors, dict_pop)

    def compute_next_generation(self) -> None:
        """
        Compute the next generation of the grid using Conway's rules.

        Updates the temporary matrix based on the current state, then replaces
        the main matrix and triggers a redraw of the interface.
        """
        self.tmp_matrix: list[list[0]] = [
            [0 for _ in range(len(self.matrix))]
            for _ in range(len(self.matrix))
        ]

        for lignes in range(len(self.matrix)):
            for cases in range(len(self.matrix)):

                neighbors, counts = self.get_neighbors((lignes, cases))
                alive = counts[1]

                if (
                    self.matrix[lignes][cases] == 0
                    and alive == 3
                ):
                    self.tmp_matrix[lignes][cases] = 1
                elif (
                    self.matrix[lignes][cases] == 1
                    and alive in [2, 3]
                ):
                    self.tmp_matrix[lignes][cases] = 1
                elif (
                    self.matrix[lignes][cases] == 1
                    and alive not in [2, 3]
                ):
                    self.tmp_matrix[lignes][cases] = 0

        self.matrix = self.tmp_matrix
        self.draw_grid(self.tmp_matrix)

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

    matrix_size = 50

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

    # === Run ===

    root.mainloop()
