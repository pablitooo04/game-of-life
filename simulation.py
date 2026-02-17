from grid import Grid

try: 
    import numpy as np
except ImportError:
    print("numpy not found!")

class Simulation:
    def __init__(self, grid: Grid | None=None) -> None:
        """Initialize the grid

        Args:
            matrix (list[list[int]]): Initial state of the grid.
            size (int): Size of the canvas in pixels.
        """
        if grid is None:
            self.grid = Grid()
        else:
            self.grid = grid
        
        self.generation = 1

    def compute_next_generation(self):
        neighbors = (
            np.roll(np.roll(self.grid.matrix,  1, 0),  1, 1) +
            np.roll(np.roll(self.grid.matrix,  1, 0),  0, 1) +
            np.roll(np.roll(self.grid.matrix,  1, 0), -1, 1) +
            np.roll(np.roll(self.grid.matrix,  0, 0),  1, 1) +
            np.roll(np.roll(self.grid.matrix,  0, 0), -1, 1) +
            np.roll(np.roll(self.grid.matrix, -1, 0),  1, 1) +
            np.roll(np.roll(self.grid.matrix, -1, 0),  0, 1) +
            np.roll(np.roll(self.grid.matrix, -1, 0), -1, 1)
        )

        new_grid = ((neighbors == 3) | (
            (self.grid.matrix == 1) & (neighbors == 2))).astype(int)

        self.grid.matrix = new_grid


    """  """

    """ def auto_loop(self):
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
        ) """
    
if __name__ == "__main__":
    print("Test :\n")

    grid_a = Grid(size=(10, 20))
    grid_a.set_cell((5, 10), 1)
    grid_a.set_cell((4, 10), 1)
    grid_a.set_cell((4, 9), 1)
    grid_a.set_cell((5, 9), 1)
    
    grid_a.print_tab()
    sim_a = Simulation(grid_a)
    sim_a.compute_next_generation()
    grid_a.print_tab()

    