from .square import Square
from random import randrange

class Field:
    def __init__(self, width: int, height: int, scale: int) -> None:
        self.width = width * scale
        self.height = height * scale
        self.scale = scale
    def get_start_coords(self) -> Square:

        return Square(
           int((self.width / self.scale) // 2) * self.scale,
           int((self.height / self.scale) // 2) * self.scale
        )
    def get_rand_coords(self) -> Square:
        return Square(
            randrange(0, self.width // self.scale) * self.scale,
            randrange(0, self.height // self.scale) * self.scale
        )

    def check_inside(self, sqr: Square) -> bool:
        return 0 <= sqr.x < self.width and 0 <= sqr.y < self.height