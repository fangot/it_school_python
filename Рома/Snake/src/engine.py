import pygame
from .constants import *
from .direction import Direction
from .colors import Colors
from .square import Square

class Engine:
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode([FIELD.width, FIELD.height])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FIELD.scale)
        
    def is_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
    
    def get_press_button(self) -> Direction | None:
        button = pygame.key.get_pressed()
        if button[pygame.K_UP]:
            return Direction.UP
        if button[pygame.K_DOWN]:
            return Direction.DOWN
        if button[pygame.K_RIGHT]:
            return Direction.LEFT
        if button[pygame.K_LEFT]:
            return Direction.RIGHT
        return None
    
    def set_default_cursor(self) -> None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def fill_display(self) -> None:
        self.display.fill(Colors.FIELD)
     
    def draw_square(self, sqr: Square, color: str) -> None:
        pygame.draw.rect(\
            self.display,\
            pygame.Color(color),\
            (sqr.x, sqr.y, ELEMENT_SIZE, ELEMENT_SIZE),\
            0,\
            0\
        )
        
    def draw_text(self, text: str, color: str, position) -> None:
        message = self.font.render(text, True, pygame.Color(color))
        if position == "center":
            position = message.get_rect(center = (FIELD.width // 2, FIELD.height // 2))
        self.display.blit(message, position)
        
    def draw_score(self, score: int) -> None:
        self.draw_text(\
            "SCORE: " + str(score),\
            Colors.SCORE,
            (5, 5)\
        )

    def draw_button(self, text: str, coords, size, color, action: str = None) -> str | None:
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
        
    def draw_restart_button(self) -> str | None:
        width = 200
        height = 40
        x_offset = 0
        y_offset = 70
        return self.draw_button(\
            "RESTART",\
            (\
                (FIELD.width - width) // 2 + x_offset,\
                (FIELD.height - height) // 2 + y_offset\
            ),\
            (width, height),\
            (Colors.RESTART_BG, Colors.RESTART_BG_HOVER, Colors.RESTART_BLACK),\
            "restart"\
        )
    
    def draw_game_over(self) -> None:
        self.draw_text(\
            "GAME OVER",\
            Colors.GAME_OVER,\
            "center"\
        )

    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS)
        
    def quit(self) -> None:
        pygame.quit()