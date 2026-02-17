from abc import ABC, abstractmethod

class BaseRenderer(ABC):
    @abstractmethod
    def display_grid(self):
        ...