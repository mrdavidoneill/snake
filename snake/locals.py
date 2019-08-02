import pygame, sys, random                  # sys for closing programm.  random for Apple position
from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

pygame.init()  # Initialises pygame for all

# =========== CONSTANTS =========== #

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
