import pygame, sys, random                  # sys for closing programm.  random for Apple position
from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

# =========== User changeable data =========== #
GRID_SIZE = 10                      # pixels
GRID_WIDTH, GRID_HEIGHT = 30, 30    # grid cells
STARTING_FPS = 5                    # Starting speed

# =========== CONSTANTS =========== #

# Score bar height bar in pixels
BOTTOMBAR = 50
# Size of playing area in pixels
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE
# Size of window in pixels
WINDOW_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOMBAR)    # Tuple of window size()
# Midpoint of grid in cells
GRID_MID_Y = SCREEN_HEIGHT / 2 / GRID_SIZE  # Mid point on y axis in Grid coordinates
GRID_MID_X = SCREEN_WIDTH / 2 / GRID_SIZE   # Mid point on x axis in Grid coordinates

# Confirm Screen size is divisible by the grid size
assert(SCREEN_WIDTH % GRID_SIZE == 0)
assert(SCREEN_HEIGHT % GRID_SIZE == 0)

# =========== COLOURS =========== #
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
GREY =  (155,155,155)
RED   = (255,  0,  0)

# =========== KEYWORDS =========== #
x = "x"
y = "y"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

####################################

class Game:

    score = 0
    snake = None
    apple = None
    fps = STARTING_FPS
    fpsClock = None

    @classmethod
    def run(cls):
        """ Initialise pygame, start Screen and reset Game with new snake and apple """
        pygame.init()
        pygame.display.set_caption("Snake")
        cls.fpsClock = pygame.time.Clock()
        Screen.reset_screen()
        cls.reset()

        ##### Game loop #####
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Arrow controls direction, and blocks going directly to direction it came from
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT and cls.snake.get_direction() != RIGHT:
                        cls.snake.set_direction(LEFT)
                    elif event.key == K_RIGHT and cls.snake.get_direction() != LEFT:
                        cls.snake.set_direction(RIGHT)
                    elif event.key == K_UP and cls.snake.get_direction() != DOWN:
                        cls.snake.set_direction(UP)
                    elif event.key == K_DOWN and cls.snake.get_direction() != UP:
                        cls.snake.set_direction(DOWN)
                    break

            if not cls.snake.move():
                Game.gameover()

            if cls.snake.eating(cls.apple[0], cls.apple[1]):
                cls.score += 1
                cls.set_apple_pos()
                Screen.draw_apple(cls.apple)
                Screen.draw_btm_bar()
                Screen.display_btm_msg(f"Score: {cls.score}")
                cls.snake.grow()
                cls.fps += 1

            pygame.display.update()
            cls.fpsClock.tick(cls.fps)

    @classmethod
    def gameover(cls):
        """ Check for quit, or space bar which resets game.
            Display game-over message over image of last lost position """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        Screen.reset_screen()
                        cls.reset()
                        return

            Screen.display_centre_msg("Press SPACE to play again")
            pygame.display.update()
            cls.fpsClock.tick(cls.fps)

    @classmethod
    def set_apple_pos(cls):
        """ Set class property 'apple' to a random position within the grid """
        cls.apple = (random.randint(0, GRID_WIDTH - 1),
                     random.randint(0, GRID_HEIGHT - 1))

    @classmethod
    def reset(cls):
        """ Reset game state with score of 0, a new snake, and a random apple position,
            then draw apple to screen and display score """
        cls.score = 0
        cls.snake = Snake()
        cls.set_apple_pos()
        Screen.draw_apple(cls.apple)
        Screen.display_btm_msg(f"Score: {cls.score}")


class Snake:
    HEAD = 0
    COLOR = BLACK

    def __init__(self):
        """ Initialise a snake with a 3 block body.
            Direction set to left, """

        self.body = [{x: GRID_MID_X + 0, y: GRID_MID_Y},
                     {x: GRID_MID_X + 1, y: GRID_MID_Y},
                     {x: GRID_MID_X + 2, y: GRID_MID_Y}]
        self.direction_x = -1
        self.direction_y = 0

    def draw(self):
        """ Draw snake on display surface """
        for block in self.body:
            block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(Screen.display, Snake.COLOR, block_position)

    def erase(self):
        """ Erase snake from display surface """
        for block in self.body:
            block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(Screen.display, Screen.game_bg_color, block_position)

    def move(self):
        """ Erase snake from display surface, delete last tail position and add new head position in direction
            heading.  Then draw snake in new position.
            Calculate if it's outside the screen, or hit its own tail and if so: stop snake and return False,
            else return True """
        self.erase()
        self.body.pop()
        new_head = [{x: self.body[Snake.HEAD][x] + self.direction_x, y: self.body[Snake.HEAD][y] + self.direction_y}]
        self.body = new_head + self.body
        self.draw()
        if self.body[Snake.HEAD][x] < 0 or self.body[Snake.HEAD][x] == GRID_WIDTH:
            self.stop()
            return False
        if self.body[Snake.HEAD][y] < 0 or self.body[Snake.HEAD][y] == GRID_HEIGHT:
            self.stop()
            return False
        if self.hit_body():
            return False
        return True

    def stop(self):
        """ Stop snake by setting it's X and Y direction to 0 """
        self.direction_x = 0
        self.direction_y = 0

    def set_direction(self, dir):
        """ Set its direction to given argument of one of:
            UP, DOWN, RIGHT, LEFT """
        if dir == UP:
            self.direction_x = 0
            self.direction_y = -1
        elif dir == DOWN:
            self.direction_x = 0
            self.direction_y = 1
        elif dir == RIGHT:
            self.direction_x = 1
            self.direction_y = 0
        elif dir == LEFT:
            self.direction_x = -1
            self.direction_y = 0

    def get_direction(self):
        """ Return the direction the snake is headed """
        if self.direction_x == 1:
            return RIGHT
        elif self.direction_x == -1:
            return  LEFT
        elif self.direction_y == -1:
            return UP
        elif self.direction_y == 1:
            return DOWN

    def eating(self, apple_x, apple_y):
        """ Return True if snake head has hit the apple """
        if self.body[Snake.HEAD][x] == apple_x and self.body[Snake.HEAD][y] == apple_y:
            return True

    def grow(self):
        """ Increase its body size by one """
        new_head = [{x: self.body[Snake.HEAD][x] + self.direction_x, y: self.body[Snake.HEAD][y] + self.direction_y}]
        self.body = new_head + self.body

    def hit_body(self):
        """ Return True if head hits its own body, else return False """
        for block in self.body[1:]:
            if block[x] == self.body[Snake.HEAD][x] and block[y] == self.body[Snake.HEAD][y]:
                return True
        else:
            return False


class Screen:

    display = pygame.display.set_mode(WINDOW_SIZE)
    btm_bar_color = WHITE
    game_bg_color = GREY
    btm_bar = (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOMBAR)

    @classmethod
    def reset_screen(cls):
        """ Starts the screen with score bar at bottom of window,
            then draws to display """

        cls.fill_background()
        cls.draw_btm_bar()

    @classmethod
    def fill_background(cls):
        """ Fills background with game_bg_color """
        cls.display.fill(cls.game_bg_color)  # Fill window with game background colour


    @classmethod
    def draw_btm_bar(cls):
        """ Draws bottom bar on display surface """
        pygame.draw.rect(cls.display, cls.btm_bar_color, cls.btm_bar)

    @classmethod
    def draw_apple(cls, pos):
        """ Draws apple to the display surface """
        x, y = pos
        block_position = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(cls.display, RED, block_position)

    @classmethod
    def display_btm_msg(cls, msg):
        """ Displays the score onto the bottom of the window where the screen bar is """
        fontObj = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH / 10), 32))
        score_surface = fontObj.render(msg, True, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + (BOTTOMBAR / 2))
        cls.display.blit(score_surface, score_rect)

    @classmethod
    def display_centre_msg(cls, msg):
        """ Displays message showing how to start new game """
        fontObj = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH / 14), 25))
        new_game_surface = fontObj.render(msg, True, BLACK)
        new_game_rect = new_game_surface.get_rect()
        new_game_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT /2)
        cls.display.blit(new_game_surface, new_game_rect)


if __name__ == "__main__":
    Game.run()
