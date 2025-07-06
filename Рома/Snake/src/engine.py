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

    def set_hand_cursor(self) -> None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    
    def fill_display(self) -> None:
        self.display.fill(Colors.FIELD)
     
    def draw_square(self, sqr: Square, color: str, size: list[int, int] = (ELEMENT_SIZE, ELEMENT_SIZE)) -> None:
        pygame.draw.rect(
            self.display,
            pygame.Color(color),
            (sqr.x, sqr.y, size[0], size[1]),
            0,
            0
        )
        
    def draw_text(self, text: str, color: str, position: list[int, int], is_center: bool = False) -> None:
        message = self.font.render(text, True, pygame.Color(color))
        if is_center:
            position = message.get_rect(center = position)
        self.display.blit(message, position)
        
    def draw_score(self, score: int) -> None:
        self.draw_text(
            "SCORE: " + str(score),
            Colors.SCORE,
            (5, 5)
        )

    def draw_button(self, text: str, coords: list[int, int], size: list[int, int], color: list[str, str, str], action: str) -> str | None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if (coords[0] + size[0] > mouse[0] > coords[0]) and (coords[1] + size[1] > mouse[1] > coords[1]):
            self.set_hand_cursor()
            self.draw_square(
                Square(coords[0], coords[1]),
                color[1],
                (size[0], size[1])
            )
            if click[0] == 1:
                return action
        else:
            self.set_default_cursor()
            self.draw_square(
                Square(coords[0], coords[1]),
                color[0],
                (size[0], size[1])
            )

        self.draw_text(
            text,
            color[2],
            (coords[0] + size[0] // 2, coords[1] + size[1] // 2),
            True
        )
        
    def draw_restart_button(self, action: str) -> str | None:
        width = 200
        height = 40
        x_offset = 0
        y_offset = 70
        return self.draw_button(
            "RESTART",
            (
                (FIELD.width - width) // 2 + x_offset,
                (FIELD.height - height) // 2 + y_offset
            ),
            (width, height),
            (Colors.RESTART_BG, Colors.RESTART_BG_HOVER, Colors.RESTART_BLACK),
            action
        )
    
    def draw_game_over(self) -> None:
        self.draw_text(
            "GAME OVER",
            Colors.GAME_OVER,
            (FIELD.width // 2, FIELD.height // 2),
            True
        )

    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(FPS)
        
    def quit(self) -> None:
        pygame.quit()