from .constants import *
from .snake import Snake

class Apple:
    def __init__(self, snake: Snake) -> None:
        apple = None
        while apple is None:
            apple = FIELD.randCoords()
            if snake.checkInside(apple):
                apple = None
        self.init = apple