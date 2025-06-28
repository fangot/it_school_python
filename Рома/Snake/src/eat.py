from .constants import *
from .square import Square

class Eat:
    def __init__(self) -> None:
        self.sqr = None

        while self.sqr is None:
            coords = FIELD.get_rand_coords()
            if coords.is_free():
                self.sqr = coords

    def is_eaten(self) -> bool:
        if not self.sqr.is_free():
            self.sqr.delete()
            del self
            return True
        return False

