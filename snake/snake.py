from locals import *
from screen import Screen


class Snake:
    HEAD = 0

    gridx_min = Screen.GRIDX_0
    gridx_max = Screen.GRIDX_MAX
    gridy_min = Screen.GRIDY_0
    gridy_max = Screen.GRIDY_MAX

    def __init__(self):
        """ Initialises new snake with colour of black, and a 3 block body.
            Direction set to left, """
        self.color = BLACK
        self.surface = Screen.surface
        self.body = [{x: Screen.GRID_MID_X + 0, y: Screen.GRID_MID_Y},
                     {x: Screen.GRID_MID_X + 1, y: Screen.GRID_MID_Y},
                     {x: Screen.GRID_MID_X + 2, y: Screen.GRID_MID_Y}]
        self.direction_x = -1
        self.direction_y = 0


    def show_legal_heads(self):
        """ Paints all possible head positions on to the screen and prints to console in grid coordinates """
        print(f"Possible head grid positions: {Snake.gridx_min},{Snake.gridy_min} to {Snake.gridx_max},{Snake.gridy_max}")
        self.direction_x = 0
        for sx in range(Snake.gridx_min, Snake.gridx_max):
            self.body[Snake.HEAD][x] = sx
            for sy in range(Snake.gridy_min, Snake.gridy_max):
                self.body[Snake.HEAD][y] = sy
                self.draw()

    def draw(self):
        """ Draws snake on display surface """
        for block in self.body:
            block_position = (block[x] * Screen.GRID_SIZE, block[y] * Screen.GRID_SIZE, Screen.GRID_SIZE, Screen.GRID_SIZE)
            pygame.draw.rect(self.surface, self.color, block_position)

    def erase(self):
        """ Erases snake from display surface """
        for block in self.body:
            block_position = (block[x] * Screen.GRID_SIZE, block[y] * Screen.GRID_SIZE, Screen.GRID_SIZE, Screen.GRID_SIZE)
            pygame.draw.rect(self.surface, Screen.BG_COLOR, block_position)

    def move(self):
        """ Erases snake from display surface, deletes last tail position and adds new head position in direction
            heading.  Then draws snake in new position.
            Calculates if it's outside the screen, or hit its own tail and if so: returns False, else returns True """
        self.erase()
        self.body.pop()
        new_head = [{x: self.body[Snake.HEAD][x] + self.direction_x, y: self.body[Snake.HEAD][y] + self.direction_y}]
        self.body = new_head + self.body
        self.draw()
        if self.body[Snake.HEAD][x] < Snake.gridx_min or self.body[Snake.HEAD][x] == Snake.gridx_max:
            self.stop()
            return False
        if self.body[Snake.HEAD][y] < Snake.gridy_min or self.body[Snake.HEAD][y] == Snake.gridy_max:
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

if __name__ == "__main__":

    Screen.start_screen()
    fpsClock = pygame.time.Clock()

    snake = Snake()
    # snake.show_legal_heads()

    # Set of moves for testing #
    MOVES = [LEFT,  LEFT,  LEFT,  LEFT,
               UP,    UP,    UP,    UP,
            RIGHT, RIGHT, RIGHT, RIGHT,
             DOWN,  DOWN,  DOWN,  DOWN]

    move = 0        # index of current move

    # Game loop #
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        snake.move()
        snake.set_direction(MOVES[move])        # Set direction according to current move

        # Reset move index when it reaches the end, else increment
        if move == len(MOVES) - 1:
            move = 0
        else:
            move += 1

        Screen.update()
        fpsClock.tick(5)
