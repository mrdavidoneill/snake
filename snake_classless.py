# A version of snake coded without classes #

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

DISPLAY = pygame.display.set_mode(WINDOW_SIZE)
BTM_BAR = (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOMBAR)

# =========== COLOURS =========== #
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
GREY =  (155,155,155)
RED   = (255,  0,  0)

# Asset colours #
SNAKE_COLOUR = BLACK
BG_COLOUR = GREY
APPLE_COLOUR = RED
BTM_BAR_COLOR = WHITE
GAME_BG_COLOR = GREY

# =========== KEYWORDS =========== #
x = "x"
y = "y"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0
BODY = "body"
DIRECTION_X = "DIRECTION_X"
DIRECTION_Y = "DIRECTION_Y"


# =========== Functions =========== #

def play():
    """ Initialise pygame, reset score, speed, snake and apple and start game loop """

    pygame.init()
    pygame.display.set_caption("Snake")

    reset_screen()
    score = 0
    display_btm_msg(f"Score: {score}")
    snake = reset_snake()
    apple = rand_apple_pos()
    draw_apple(apple)

    fps = STARTING_FPS
    fps_clock = pygame.time.Clock()

    ##### Game loop #####
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Arrow controls direction, and blocks going directly to direction it came from
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and get_direction(snake) != RIGHT:
                    set_direction(snake, LEFT)
                elif event.key == K_RIGHT and get_direction(snake) != LEFT:
                    set_direction(snake, RIGHT)
                elif event.key == K_UP and get_direction(snake) != DOWN:
                    set_direction(snake, UP)
                elif event.key == K_DOWN and get_direction(snake) != UP:
                    set_direction(snake, DOWN)
                break

        if not move_snake(snake):
            gameover()
            fps = STARTING_FPS
            reset_screen()
            score = 0
            display_btm_msg(f"Score: {score}")
            snake = reset_snake()
            apple = rand_apple_pos()
            draw_apple(apple)

        if eating(snake, apple[0], apple[1]):
            score += 1
            apple = rand_apple_pos()
            draw_apple(apple)
            draw_btm_bar()
            display_btm_msg(f"Score: {score}")
            grow(snake)
            fps += 1

        pygame.display.update()
        fps_clock.tick(fps)


def gameover():
    """ Display game-over message and check for quit, or space bar."""
    display_centre_msg("Press SPACE to play again")
    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                return


def rand_apple_pos():
    """ Return a random cell position within the grid """
    apple = (random.randint(0, GRID_WIDTH - 1),
                 random.randint(0, GRID_HEIGHT - 1))
    return apple


def reset_snake():
    """ Reset the snake BODY, position and direction """
    snake = {BODY: [{x: GRID_MID_X + 0, y: GRID_MID_Y},
                    {x: GRID_MID_X + 1, y: GRID_MID_Y},
                    {x: GRID_MID_X + 2, y: GRID_MID_Y}],
             DIRECTION_X: -1,
             DIRECTION_Y: 0}
    return snake


def draw_snake(snake):
    """ Draw snake on DISPLAY surface """
    for block in snake[BODY]:
        block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(DISPLAY, SNAKE_COLOUR, block_position)


def erase_snake(snake):
    """ Erase snake from DISPLAY surface """
    for block in snake[BODY]:
        block_position = (block[x] * GRID_SIZE, block[y] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(DISPLAY, BG_COLOUR, block_position)


def move_snake(snake):
    """ Erase snake from DISPLAY surface, delete last tail position and add new head position in direction
        heading.  Then draw snake in new position.
        If it's outside the screen, or hit its own tail and if so: return False,
                                                            else: return True """
    erase_snake(snake)
    snake[BODY].pop()
    new_head = [{x: snake[BODY][HEAD][x] + snake[DIRECTION_X], y: snake[BODY][HEAD][y] + snake[DIRECTION_Y]}]
    snake[BODY] = new_head + snake[BODY]
    draw_snake(snake)
    if hit_boundary(snake):
        return False
    if hit_body(snake):
        return False
    return True


def set_direction(snake, dir):
    """ Set snake direction to given argument of one of:
        UP, DOWN, RIGHT, LEFT """
    if dir == UP:
        snake[DIRECTION_X] = 0
        snake[DIRECTION_Y] = -1
    elif dir == DOWN:
        snake[DIRECTION_X] = 0
        snake[DIRECTION_Y] = 1
    elif dir == RIGHT:
        snake[DIRECTION_X] = 1
        snake[DIRECTION_Y] = 0
    elif dir == LEFT:
        snake[DIRECTION_X] = -1
        snake[DIRECTION_Y] = 0


def get_direction(snake):
    """ Return the direction the snake is headed """
    if snake[DIRECTION_X] == 1:
        return RIGHT
    elif snake[DIRECTION_X] == -1:
        return  LEFT
    elif snake[DIRECTION_Y] == -1:
        return UP
    elif snake[DIRECTION_Y] == 1:
        return DOWN


def eating(snake, apple_x, apple_y):
    """ Return True if snake head has hit the apple """
    if snake[BODY][HEAD][x] == apple_x and snake[BODY][HEAD][y] == apple_y:
        return True


def grow(snake):
    """ Increase snake BODY size by one """
    new_head = [{x: snake[BODY][HEAD][x] + snake[DIRECTION_X], y: snake[BODY][HEAD][y] + snake[DIRECTION_Y]}]
    snake[BODY] = new_head + snake[BODY]


def hit_body(snake):
    """ Return True if head hits its own BODY, else return False """
    for block in snake[BODY][1:]:
        if block[x] == snake[BODY][HEAD][x] and block[y] == snake[BODY][HEAD][y]:
            return True


def hit_boundary(snake):
    """ Return True if head hits outside the screen """
    if snake[BODY][HEAD][x] < 0 or snake[BODY][HEAD][x] == GRID_WIDTH:
        return True
    if snake[BODY][HEAD][y] < 0 or snake[BODY][HEAD][y] == GRID_HEIGHT:
        return True


def reset_screen():
    """ Starts the screen with score bar at bottom of window,
        then draws to DISPLAY """
    fill_background()
    draw_btm_bar()


def fill_background():
    """ Fills background with GAME_BG_COLOR """
    DISPLAY.fill(GAME_BG_COLOR)  # Fill window with game background colour


def draw_btm_bar():
    """ Draws bottom bar on DISPLAY surface """
    pygame.draw.rect(DISPLAY, BTM_BAR_COLOR, BTM_BAR)


def draw_apple(pos):
    """ Draws apple to the DISPLAY surface """
    x, y = pos
    block_position = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(DISPLAY, APPLE_COLOUR, block_position)


def display_btm_msg(msg):
    """ Displays the score onto the bottom of the window where the screen bar is """
    fontObj = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH / 10), 32))
    score_surface = fontObj.render(msg, True, BLACK)
    score_rect = score_surface.get_rect()
    score_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT + (BOTTOMBAR / 2))
    DISPLAY.blit(score_surface, score_rect)


def display_centre_msg(msg):
    """ Displays message showing how to start new game """
    fontObj = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH / 14), 25))
    new_game_surface = fontObj.render(msg, True, BLACK)
    new_game_rect = new_game_surface.get_rect()
    new_game_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT /2)
    DISPLAY.blit(new_game_surface, new_game_rect)


if __name__ == "__main__":
    play()
