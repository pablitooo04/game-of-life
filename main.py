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

""" class Grid:
    def __init__(self, matrix: np.array | None=None, self.size: tuple | None=None):
        self.size = self.size = 
        self.matrix = np.zeros((self.size())) if matrix is not None else matrix """


""" if __name__ == "__main__":
    # === Proprities ===

    # === Config ===

    root = tk.Tk()
    root.geometry(f"{window_size}x{window_size}")
    root.resizable(False, False)
    root.title("Conway’s Game of Life")

    icon = tk.PhotoImage(file="assets/icon.png")
    root.iconphoto(True, icon)

    matrix = [[1 for _ in range(matrix_size)] for _ in range(matrix_size)]

    I1 = Interface(matrix, window_size)

    # === Binds ===

    

    # === Run ===

    root.mainloop() """

from simulation import Simulation
from rendering.TkinterRenderer import TkinterRenderer

if __name__ == "__main__":

    sim = Simulation()
    renderer = TkinterRenderer(sim)