from .constants import *
from .square import Square
from .engine import Engine
from .snake import Snake
from .apple import Apple
from .colors import Colors

class Game:
    def __init__(self, engine: Engine) -> None:
        self.engine =  engine
        self.apple = None
        self.tick = None
        self.score = None
        self.snake = None
        self.is_running = None
        self.game_over = None
        self.is_set_direction = None
        self.init()

    def init(self) -> None:
        self.engine.set_default_cursor()
        self.snake = Snake(FIELD.get_start_coords(), START_SPEED)
        self.apple = Apple()
        self.tick = 0
        self.score = 0
        self.is_running = True
        self.game_over = False
        self.is_set_direction = False

    def check_game_over(self, head: Square) -> None:
        return not FIELD.check_inside(head) or self.snake.check_inside(head)

    def events(self) -> None:
        self.is_running = not self.engine.is_quit()

        new_direction = self.engine.get_pressed_button()
        if new_direction is not None and self.is_set_direction == False:
            if self.snake.set_direction(new_direction):
                self.is_set_direction = True

    def snake_state(self) -> None:
        if self.tick % round((FPS / self.snake.speed) * FPS):
            return

        self.is_set_direction = False
        new_head = self.snake.get_new_head()
        if self.check_game_over(new_head):
            self.game_over = True
            return

        self.snake.add_square(new_head)
        if self.apple.is_eaten():
            self.score += 1
            self.apple = Apple()
            self.snake.up_speed()
        else:
            self.snake.del_square()

    def update_state(self) -> None:
        if self.game_over:
            return

        self.tick += 1
        self.snake_state()
        
    def render(self) -> None:
        self.engine.fill_display()

        self.engine.draw_square(self.apple.sqr, Colors.APPLE)
        for sqr in self.snake.body:
            self.engine.draw_square(sqr,Colors.SNAKE)
        self.engine.draw_score(self.score)

        if self.game_over:
            self.engine.draw_game_over()
            action = self.engine.draw_restart_button(Game.init.__name__)
            if action is not None:
                exec("self." + str(action) + "()")

        self.engine.update()

    def start(self) -> None:
        while self.is_running:
            self.events()
            self.update_state()
            self.render()
        exit()
        self.engine.quit()