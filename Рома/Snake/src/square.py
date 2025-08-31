import math

class Square:
    squares = []

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        Square.squares.append(self)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def distant_to(self, other) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def delete(self) -> None:
        if self in Square.squares:
            Square.squares.remove(self)

    def is_free(self) -> bool:
        sum = 0
        for sqr in Square.squares:
            if sqr == self:
                sum += 1
        if sum > 1:
            return False

        return True