from .square import Square
from .item import Item
from .constants import *
import random

class Hole (Item):
    def __init__(self, snake_head: Square, tick: int) -> None:
        self.lifetime = tick + random.randint(HOLE_LIFETIME - 30, HOLE_LIFETIME + 30)
        self.body = []

        while self.sqr is None or self.sqr.distant_to(snake_head) <= HOLE_DISTANCE:
            super().__init__()

        self.body.append(self.sqr)

    def growth(self) -> None:
        x = random.randint(-1, 1)
        if x == 0:
            y = random.choice([1, -1])
        else:
            y = random.randint(-1, 1)

        new_sqr = Square(
            self.sqr.x + x * SCALE,
            self.sqr.y + y * SCALE
        )
        self.body.append(new_sqr)