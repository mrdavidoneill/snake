import pygame, sys, random                  # sys for closing programm.  random for Apple position
from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

pygame.init()                               # Initialise pygame
pygame.display.set_caption("Snake")         # Title bar of window

starting_FPS = 5                            # Starting FPS used for resetting the game
FPS = starting_FPS                          # FPS  - this speeds up as game progresses
fpsClock = pygame.time.Clock()              # Clock object

# =========== CONSTANTS =========== #
SCOREBAR = 50                               # Score bar height bar
SCREEN_WIDTH  = 400                         # Playing screen width in pixels
SCREEN_HEIGHT = 400                         # Playing screen height in pixels
WINDOW_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT + SCOREBAR)    # Tuple of window size()
GRID_SIZE     = 10                          # Grid size in pixels
GRID_MID_Y = SCREEN_HEIGHT / 2 / GRID_SIZE  # Mid point on y axis in Grid coordinates
GRID_MID_X = SCREEN_WIDTH / 2 / GRID_SIZE   # Mid point on x axis in Grid coordinates
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE       # Total number of grid squares on x axis
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE     # Total number of grid squares on y axis

assert(SCREEN_WIDTH % GRID_SIZE == 0)       # Confirm that SCREEN_WIDTH is divisible by GRID_SIZE
assert(SCREEN_HEIGHT % GRID_SIZE == 0)      # Confirm that SCREEN_HEIGHT is divisible by GRID_SIZE

# =========== COLOURS =========== #
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
GREY = (155,155,155)
RED   = (255,  0,  0)

BG_COLOR = GREY

x = "x"
y = "y"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)  # Create display surface and set to WINDOW_SIZE



class Main:
    def __init__(self):
        """ Main class to start game.  Creates a new game """
        Game()

class Game:

    def __init__(self):
        """ Initialises the new game with score of 0 and then calls the run method """
        self.score = 0
        self.run()

    def run(self):
        """ Initialises the Screen, calls Screen.display_score function and initialises a new snake and a new apple """

        global FPS              # Global used to speed up game after every apple eaten

        screen = Screen()         # Initialise screen bar
        Screen.display_score(self.score)    # Display score
        snake = Snake()         # Initialise new snake
        apple = Apple()         # Initialise new apple

        ##### Game loop #####
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Arrow controls direction, and checks to not go directly to direction it came from
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT and snake.get_direction() != RIGHT:
                        snake.set_direction(LEFT)
                    elif event.key == K_RIGHT and snake.get_direction() != LEFT:
                        snake.set_direction(RIGHT)
                    elif event.key == K_UP and snake.get_direction() != DOWN:
                        snake.set_direction(UP)
                    elif event.key == K_DOWN and snake.get_direction() != UP:
                        snake.set_direction(DOWN)

            if not snake.move():        # if snake can't move, call Game.gameover(), else move in current direction.
                FPS = starting_FPS          # reset game FPS
                Game.gameover()             # call Game.gameover() screen

            if snake.eating(apple.x, apple.y):
                apple = Apple()
                self.score += 1
                screen.draw_scorebar()
                screen.display_score(self.score)
                snake.grow()
                FPS += 1       # Speed up game after every apple eaten

            pygame.display.update()
            fpsClock.tick(FPS)

    @staticmethod
    def gameover():
        """ Checks for quit, or space bar which starts a new game.
            Displays gameover message over image of last lost position """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        DISPLAYSURF.fill(BG_COLOR)  # Fill window with background colour to clear last game
                        Main()                  # Restart game

            Screen.new_game_msg()       # Displays instructions to restart game
            pygame.display.update()
            fpsClock.tick(FPS)

class Snake:
    HEAD = 0

    def __init__(self):
        """ Initialises new snake with colour of black, and a 3 block body.
            Direction set to left, """
        self.color = BLACK
        self.body = [{x: GRID_MID_X + 0, y: GRID_MID_Y},
                     {x: GRID_MID_X + 1, y: GRID_MID_Y},
                     {x: GRID_MID_X + 2, y: GRID_MID_Y}]
        self.direction_x = -1
        self.direction_y = 0

    def draw(self):
        """ Draws snake on display surface """
        for block in self.body:
            block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(DISPLAYSURF, self.color, block_position)

    def erase(self):
        """ Erases snake from display surface """
        for block in self.body:
            block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(DISPLAYSURF, BG_COLOR, block_position)

    def move(self):
        """ Erases snake from display surface, deletes last tail position and adds new head position in direction
            heading.  Then draws snake in new position.
            Calculates if it's outside the screen, or hit its own tail and if so: returns False, else returns True """
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
        """ Stops snake by setting it's X and Y direction to 0 """
        self.direction_x = 0
        self.direction_y = 0

    def set_direction(self, dir):
        """ Sets its direction to given argument of one of:
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
        """ Returns the direction the snake is headed """
        if self.direction_x == 1:
            return RIGHT
        elif self.direction_x == -1:
            return  LEFT
        elif self.direction_y == -1:
            return UP
        elif self.direction_y == 1:
            return DOWN

    def eating(self, apple_x, apple_y):
        """ Returns True if snake head has hit the apple """
        if self.body[Snake.HEAD][x] == apple_x and self.body[Snake.HEAD][y] == apple_y:
            return True

    def grow(self):
        """ Increases its body size by one """
        new_head = [{x: self.body[Snake.HEAD][x] + self.direction_x, y: self.body[Snake.HEAD][y] + self.direction_y}]
        self.body = new_head + self.body

    def hit_body(self):
        """ Returns True if head hits its own body, else returns False """
        for block in self.body[1:]:
            if block[x] == self.body[Snake.HEAD][x] and block[y] == self.body[Snake.HEAD][y]:
                return True
        else:
            return False

class Apple:
    count = 0         # Apple count keeping track of how many apples have been initialised in the current game
    def __init__(self):
        """ Initialises new apple with colour of red, at a random x, y coordinate and adds 1 to the count.
            then draws to display surface """
        self.color = RED
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        Apple.count += 1
        self.draw()

    def draw(self):
        """ Draws apple to the display surface """
        block_position = (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(DISPLAYSURF, self.color, block_position)


class Screen:
    def __init__(self):
        """ Initialises new screen with score bar at bottom of window with colour white,
            then draws to display surface """
        self.scorebar_color = WHITE
        self.game_bg_color = GREY
        self.position = (0, SCREEN_HEIGHT, SCREEN_WIDTH, SCOREBAR)
        self.fill_background()
        self.draw_scorebar()

    def fill_background(self):
        """ Fills background with game_bg_color """
        DISPLAYSURF.fill(self.game_bg_color)  # Fill window with game background colour


    def draw_scorebar(self):
        """ Draws score bar on display surface """
        pygame.draw.rect(DISPLAYSURF, self.scorebar_color, self.position)

    @staticmethod
    def display_score(score):
        """ Displays the score onto the bottom of the window where the screen bar is """
        fontObj = pygame.font.Font("freesansbold.ttf",32)
        score_surface = fontObj.render("Score: {}".format(score), True, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT + (SCOREBAR / 2))
        DISPLAYSURF.blit(score_surface, score_rect)

    @staticmethod
    def new_game_msg():
        """ Displays message showing how to start new game """
        fontObj = pygame.font.Font("freesansbold.ttf",22)
        new_game_surface = fontObj.render("Press SPACE to play again", True, BLACK)
        new_game_rect = new_game_surface.get_rect()
        new_game_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT /2)
        DISPLAYSURF.blit(new_game_surface, new_game_rect)

if __name__ == "__main__":
    Main()