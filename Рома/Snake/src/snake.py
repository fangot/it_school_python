from collections import deque
from .constants import *
from .direction import Direction
from .square import Square


class Snake:
    def __init__(self, head: Square, speed: int) -> None:
        self.speed = speed
        self.direction = Direction.RAND
        self.body = deque()
        self.body.append(head)
        self.body.append(self.get_tail())

    def get_new_square(self, forward: int) -> Square:
        sign = forward * FIELD.scale
        if self.direction.value > 2:
            sign = -forward * FIELD.scale

        if self.direction.value % 2 == 0:
            x = self.body[0].x - sign
            y = self.body[0].y
        else:
            x = self.body[0].x
            y = self.body[0].y - sign

        return Square(x, y)

    def set_direction(self, new_direction: Direction) -> None:
        if self.direction.value % 2 != new_direction.value % 2:
            self.direction = new_direction

    def add_square(self, head: Square) -> None:
        self.body.appendleft(head)

    def del_square(self) -> None:
        self.body.pop()

    def get_tail(self) -> Square:
        return self.get_new_square(-1)

    def get_new_head(self) -> Square:
        return self.get_new_square(1)

    def check_inside(self, sqr: Square) -> bool:
        try:
            self.body.index(sqr)
            return True
        except ValueError:
            return False

    def up_speed(self) -> None:
        self.speed *= UP_SPEED_STEP
