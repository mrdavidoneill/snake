import pygame, sys, random                  # sys for closing programm.  random for Apple position
from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

pygame.init()  # Initialises pygame for all

# =========== CONSTANTS =========== #
SCOREBAR = 50                               # Score bar height bar
GRID_SIZE     = 10                          # Grid size in pixels
SCREEN_WIDTH  = GRID_SIZE * 40              # Playing screen width in pixels
SCREEN_HEIGHT = GRID_SIZE * 40              # Playing screen height in pixels
WINDOW_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT + SCOREBAR)    # Tuple of window size()
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

# =========== KEYWORDS =========== #
x = "x"
y = "y"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

