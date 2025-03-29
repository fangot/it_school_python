import pygame
from .constants import *
from .direction import Direction
from .color import Color
from .element import Element

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
    
    def setDefaultCursor(self) -> None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
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
        
    def drawText(self, text: str, color: str, position) -> None:
        message = self.font.render(text, True, pygame.Color(color))
        if position == "center":
            position = message.get_rect(center = (FIELD.width // 2, FIELD.height // 2))
        self.display.blit(message, position)
        
    def drawScore(self, score: int) -> None:
        self.drawText(\
            "SCORE: " + str(score),\
            Color.SCORE,\
            (5, 5)\
        )

    def drawButton(self, text: str, coords, size, color, action: str = None) -> str | None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if (coords[0] + size[0] > mouse[0] > coords[0]) and\
           (coords[1] + size[1] > mouse[1] > coords[1]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.draw.rect(\
                self.display,\
                pygame.Color(color[1]),\
                (coords[0], coords[1], size[0], size[1]),\
                0,\
                0\
            )
            if click[0] == 1:
                return action
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.draw.rect(\
                self.display,\
                pygame.Color(color[0]),\
                (coords[0], coords[1], size[0], size[1]),\
                0,\
                0\
            )
        message = self.font.render(text, True, pygame.Color(color[2]))
        position = message.get_rect(center = (coords[0] + size[0] // 2, coords[1] + size[1] // 2))
        self.display.blit(message, position)
        
    def drawRestartButton(self) -> str | None:
        width = 100
        height = 40
        x_offset = 0
        y_offset = 70
        return self.drawButton(\
            "RESTART",\
            (\
                (FIELD.width - width) // 2 + x_offset,\
                (FIELD.height - height) // 2 + y_offset\
            ),\
            (width, height),\
            (Color.RESTART, Color.RESTART_HOVER, Color.RESTART_TEXT),\
            "restart"\
        )
    
    def drawGameOver(self) -> None:
        self.drawText(\
            "GAME OVER",\
            Color.GAME_OVER,\
            "center"\
        )

    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS)
        
    def quit(self) -> None:
        pygame.quit()