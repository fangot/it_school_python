from .snake import Snake
from .element import Element
from .constants import *

class Fruit:
    fruits = []
    
    def __init__(self, snake: Snake, tick: int, lifetime: int) -> None:
        self.tickToDelete = tick + lifetime
        self.elem = None
        while self.elem is None:
            self.elem = FIELD.randCoords()
            if snake.checkInside(self.elem) or self.checkInside(self.elem):
                self.elem = None
        Fruit.fruits.append(self)
        
    def __del__(self) -> None:
        Fruit.fruits.remove(self)
        
    def checkInside(self, elem: Element) -> bool:
        for fruit in Fruit.fruits:
            if elem == fruit.elem:
                return True
        return False