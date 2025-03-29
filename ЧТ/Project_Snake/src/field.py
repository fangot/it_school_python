from .element import Element
from random import randrange

class Field:
    def __init__(self, width: int, height: int, scale: int) -> None:
        self.width = width * scale
        self.height = height * scale
        self.scale = scale
        
    def randCoords(self) -> Element:
        return Element(randrange(0, self.width // self.scale) * self.scale, randrange(0, self.height // self.scale) * self.scale)
    
    def getStartCoords(self) -> Element:
        return Element(self.width // 2, self.height // 2)
    
    def checkInside(self, element: Element) -> bool:
        return 0 <= element.x < self.width and 0 <= element.y < self.height