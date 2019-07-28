from locals import *
from screen import Screen

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
        pygame.draw.rect(Screen.surface, self.color, block_position)


# ================ FOR TESTING PURPOSES ================ #
if __name__ == "__main__":
    TESTSURFACE = pygame.display.set_mode(WINDOW_SIZE)  # Create display surface and set to WINDOW_SIZE
    TESTSURFACE.fill(WHITE)

    apple = Apple()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
