import pygame
from .constants import *
from .direction import Direction
from .colors import Colors
from .square import Square

class Engine:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.display = pygame.display.set_mode([FIELD.width, FIELD.height])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FIELD.scale)
        
    def is_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False
    
    def get_pressed_button(self) -> Direction | None:
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
     
    def draw_square(self, sqr: Square, color: str, size: tuple[int, int] = (FILL_SIZE, FILL_SIZE)) -> None:
        pygame.draw.rect(
            self.display,
            pygame.Color(color),
            (sqr.x, sqr.y, size[0], size[1]),
            0,
            2
        )
        
    def draw_text(self, text: str, color: str, position: tuple[int, int], is_center: bool = False) -> None:
        message = self.font.render(text, True, pygame.Color(color))
        if is_center:
            position = message.get_rect(center = position)
        self.display.blit(message, position)
        
    def draw_score(self, score: int) -> None:
        self.draw_text(
            "SCORE: " + str(score),
            Colors.SCORE,
            (FIELD.width // 2, self.font.get_height() // 2 + 5),
            True
        )

    def draw_button(self, text: str, coords: tuple[int, int], size: tuple[int, int], color: tuple[str, str, str], action: str) -> str | None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        width = size[0]
        height = size[1]
        text_rect = self.font.render(text, True, pygame.Color(color[2]))
        if width - 10 < text_rect.get_width():
            width = text_rect.get_width() + 10
        if height - 10 < text_rect.get_height():
            height = text_rect.get_height() + 10
        
        if (coords[0] + width > mouse[0] > coords[0]) and (coords[1] + height > mouse[1] > coords[1]):
            self.set_hand_cursor()
            self.draw_square(
                Square(coords[0], coords[1]),
                color[1],
                (width, height)
            )
            if click[0] == 1:
                return action
        else:
            self.set_default_cursor()
            self.draw_square(
                Square(coords[0], coords[1]),
                color[0],
                (width, height)
            )

        self.draw_text(
            text,
            color[2],
            (coords[0] + width // 2, coords[1] + height // 2),
            True
        )
        
    def draw_restart_button(self, action: str) -> str | None:
        width = 100
        height = 50
        left_offset = 15
        bottom_offset = 15

        return self.draw_button(
            "RESTART",
            (left_offset, FIELD.height - bottom_offset - height),
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