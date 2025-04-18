from .constants import *
from .snake import Snake

class Apple:
    def __init__(self, snake: Snake) -> None:
        self.elem = None
        while self.elem is None:
            self.elem = FIELD.randCoords()
            if snake.checkInside(self.elem):
                self.elem = None