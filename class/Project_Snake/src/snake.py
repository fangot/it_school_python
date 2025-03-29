from collections import deque
from .constants import *
from .element import Element
from .direction import Direction

class Snake:
    def __init__(self, head: Element, speed: int) -> None:
        self.body = deque()
        self.body.append(head)
        self.direction = Direction.RAND
        self.speed = speed
        
    def setDirection(self, newDirection: Direction) -> None:
        if newDirection.value % 2 != self.direction.value % 2:
            self.direction = newDirection
            
    def upSpeed(self) -> None:
        self.speed = self.speed // UP_SPEED_STEP
            
    def addElem(self, head: Element) -> None:
        self.body.appendleft(head)
        
    def delElem(self) -> None:
        self.body.pop()
        
    def getNewHead(self) -> Element:
        head = self.body[0]
        match self.direction:
            case Direction.UP:
                return Element(head.x, head.y + FIELD.scale)
            case Direction.DOWN:
                return Element(head.x, head.y - FIELD.scale)
            case Direction.RIGHT:
                return Element(head.x + FIELD.scale, head.y)
            case Direction.LEFT:
                return Element(head.x - FIELD.scale, head.y)
            
    def checkInside(self, elem: Element) -> bool:
        try:
            self.body.index(elem)
            return True
        except ValueError:
            return False