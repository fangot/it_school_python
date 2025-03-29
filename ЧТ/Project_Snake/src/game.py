from .constants import *
from .element import Element
from .snake import Snake
from .apple import Apple
from .color import Color
from .engine import Engine

class Game:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.snake = Snake(FIELD.getStartCoords(), START_SPEED)
        self.apple = Apple(self.snake).init
        self.tick = 0
        self.score = 0
        self.isSetDirection = False
        self.isRunning = True
        self.isGameOver = False
        
    def events(self) -> None:
        self.isRunning = not self.engine.isQuit()
        
        newDirection = self.engine.getPressButton()
        if newDirection is not None and self.isSetDirection == False:
            self.snake.setDirection(newDirection)
            self.isSetDirection = True
            
    def chekGameOver(self, head: Element) -> bool:
        return not FIELD.checkInside(head) or self.snake.checkInside(head)
    
    def updateState(self) -> None:
        if self.isGameOver:
            return
        
        self.tick += 1
        if not self.tick % self.snake.speed:
            self.isSetDirection = False
            newHead = self.snake.getNewHead()
            if self.chekGameOver(newHead):
                self.isGameOver = True
            else:
                self.snake.addElem(newHead)
                if newHead == self.apple:
                    self.score += 1
                    self.apple = Apple(self.snake).init
                    if not self.score % UP_SPEED_DELAY:
                        self.snake.upSpeed()
                else:
                    self.snake.delElem()
                    
    def render(self) -> None:
        self.engine.fillDisplay()
        
        for elem in self.snake.body:
            self.engine.drawElement(elem, Color.SNAKE)
        self.engine.drawElement(self.apple, Color.APPLE)
        
        self.engine.drawScore(self.score)
        
        if self.isGameOver:
            self.engine.drawGameOver()
            
        self.engine.update()
        
    def start(self) -> None:
        while self.isRunning:
            self.events()
            self.updateState()
            self.render()
        self.engine.quit()