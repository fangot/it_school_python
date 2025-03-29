from enum import Enum
from random import randint

class Direction(Enum):
    UP = 1
    DOWN = 3
    RIGHT = 2
    LEFT = 4
    RAND = randint(1, 4)