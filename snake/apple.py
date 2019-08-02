from locals import *
from screen import Screen

class Apple:
    count = 0         # Apple count keeping track of how many apples have been initialised in the current game

    gridx_min = Screen.GRIDX_0
    gridx_max = Screen.GRIDX_MAX
    gridy_min = Screen.GRIDY_0
    gridy_max = Screen.GRIDY_MAX


    def __init__(self, snake=None):
        """ Initialises new apple with colour of red, at a random x, y coordinate and adds 1 to the count.
            then draws to display surface """

        self.x = Screen.GRID_MID_X
        self.y = Screen.GRID_MID_Y

        # Check not underneath snake body
        flag = True
        while flag and snake:
            flag = False
            self.x = random.randint(Apple.gridx_min, Apple.gridx_max - 1)
            self.y = random.randint(Apple.gridy_min, Apple.gridy_max - 1)
            for block in snake:
                if self.x == block[x] and self.y == block[y]:
                    flag = True
                    continue

        self.color = RED
        Apple.count += 1
        self.draw()


    def show_legal_apples(self):
        """ Paints all possible apple positions on to the screen and prints to console in grid coordinates """
        print(f"Possible apple grid positions: {Apple.gridx_min},{Apple.gridy_min} to {Apple.gridx_max},{Apple.gridy_max}")
        for x in range(Apple.gridx_min, Apple.gridx_max):
            self.x = x
            for y in range(Apple.gridy_min, Apple.gridy_max):
                self.y = y
                self.draw()


    def draw(self):
        """ Draws apple to the display surface """
        block_position = (self.x * Screen.GRID_SIZE, self.y * Screen.GRID_SIZE, Screen.GRID_SIZE, Screen.GRID_SIZE)
        pygame.draw.rect(Screen.surface, self.color, block_position)


# ================ FOR TESTING PURPOSES ================ #
if __name__ == "__main__":
    Screen.start_screen()
    apple = Apple()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        Screen.update()
