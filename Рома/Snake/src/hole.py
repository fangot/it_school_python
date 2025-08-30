from .square import Square
from .item import Item
from .constants import *
import random

class Hole (Item):
    def __init__(self, snake_head: Square, tick: int) -> None:
        self.sqr = None
        self.lifetime = tick + random.randint(HOLE_LIFETIME - 30, HOLE_LIFETIME + 30)
        self.body = []

        while self.sqr is None or self.sqr.distant_to(snake_head) <= HOLE_DISTANCE:
            super().__init__()

        self.body.append(self.sqr)

    def delete(self) -> None:
        for item in self.body:
            item.delete()
        del self

    def is_eaten(self) -> bool:
        for item in self.body:
            if not item.is_free():
                self.delete()
                return True
        return False

    def growth(self) -> None:
        body_to_growth = self.body.copy()

        for sqr in body_to_growth:
            max_loop = 10

            while max_loop > 0:
                max_loop -= 1
                x = random.randint(-1, 1)
                if x == 0:
                    y = random.choice([1, -1])
                else:
                    y = random.randint(-1, 1)

                new_sqr = Square(
                    sqr.x + x * SCALE,
                    sqr.y + y * SCALE
                )

                if new_sqr.is_free():
                    self.body.append(new_sqr)
                    break
                else:
                    new_sqr.delete()