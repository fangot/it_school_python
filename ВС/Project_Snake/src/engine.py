import pygame
from .element import Element
from .direction import Direction
from .color import Color
from .constants import *

class Engine:
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode([FIELD.width, FIELD.height])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FIELD.scale)
        
    def isQuit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def getPressButton(self) -> Direction | None:
        button = pygame.key.get_pressed()
        if button[pygame.K_UP]:
            return Direction.DOWN
        if button[pygame.K_DOWN]:
            return Direction.UP
        if button[pygame.K_RIGHT]:
            return Direction.RIGHT
        if button[pygame.K_LEFT]:
            return Direction.LEFT
        return None

    def fillDisplay(self) -> None:
        self.display.fill(Color.DISPLAY)

    def drawElement(self, elem: Element, color: str) -> None:
        pygame.draw.rect(\
            self.display,\
            pygame.Color(color),\
            (elem.x, elem.y, ELEMENT_SIZE, ELEMENT_SIZE),\
            0,\
            0\
        )

    def drawText(self, text: str, color: str, position: (int, int)) -> None:
        message = self.font.render(text, True, pygame.Color(color))
        if position == "center":
            position = message.get_rect(center = (FIELD.width // 2, FIELD.height // 2))
        self.display.blit(\
            message,\
            position\
        )

    def drawScore(self, score: int) -> None:
        self.drawText(\
            "SCORE: " + str(score),\
            Color.SCORE,\
            (5, 5)\
        )

    def drawGameOver(self) -> None:
        self.drawText(\
            "GAME OVER!",\
            Color.GAME_OVER,\
            "center"\
        )

    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS)

    def quit(self) -> None:
        pygame.quit()