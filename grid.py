try:
    import numpy as np
except ImportError:
    print("numpy not found")
    exit(1)

class Grid:
    def __init__(self, size: tuple[int, int] | None=None, matrix: np.ndarray | None=None):
        if size is None and matrix is None:
            self.matrix = np.zeros((50, 30), dtype=np.uint8)
            self.size = (30, 50)
        elif matrix is None:
            self.matrix = np.zeros((size[1], size[0]), dtype=np.uint8)
            self.size = size
        elif size is None:
            self.matrix = matrix
            self.size = matrix.shape
        else:
            self.matrix = matrix
            self.size = size

        if (
            any(pos <= 0 for pos in self.size) 
            or self.matrix.shape != (self.size[1], self.size[0])
        ):
            raise ValueError("Error: Invalid grid!")

    
    def set_cell(self, pos: tuple[int, int], value):
        if (
            any(p < 0 for p in pos)
            or pos[0] >= self.matrix.shape[1]
            or pos[1] >= self.matrix.shape[0]
            or value not in {0, 1}
        ):
            raise ValueError("Error: pos out of bounds!")
        else:
            self.matrix[pos[1], pos[0]] = value

    def get_cell(self, pos: tuple[int, int]) -> int:
        if (
            any(p < 0 for p in pos)
            or pos[0] >= self.matrix.shape[1]
            or pos[1] >= self.matrix.shape[0]
        ):
            raise ValueError("Error: pos out of bounds!")
        else:
            return self.matrix[pos[1], pos[0]]
    
    def set_random_grid(self):
        """
        Set a random grid pressing the 'r' key.
        all cell has a chance of 50% to be alive.
        """
        self.matrix = np.random.randint(0, 2, (self.matrix.shape), dtype=np.uint8)

    def clear_grid(self):
        self.matrix = np.zeros((self.matrix.shape), dtype=np.uint8)

    #DEV 
    def print_tab(self):
        print(self.matrix)
        print("grid size:", self.size)

