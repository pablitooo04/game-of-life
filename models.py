from pydantic import BaseModel, model_validator
import numpy as np

class GridModel(BaseModel):
    size: tuple[int, int],
    matrix: np.array

    @model_validator(mode='after')
    def validation(self):
        if not any(x > 0 and x < 10 for x in size):
            raise ValueError("Error: Invalid size!")
        