from locals import *
from snake import Snake
from apple import Apple
from screen import Screen

class Game:

    starting_FPS = 5                # Starting FPS used for resetting the game
    FPS = starting_FPS              # FPS  - this speeds up as game progresses
    fpsClock = pygame.time.Clock()  # Clock object

    def __init__(self):
        """ Initialises the new game with score of 0 and then calls the run method """
        self.score = 0
        self.run()

    def run(self, test=None):
        """ Initialises the Screen, calls Screen.display_score function and initialises a new snake and a new apple """

        Screen.start_screen()         # Start screen
        Screen.display_btm_info(self.score)    # Display score

        snake = Snake()         # Initialise new snake
        apple = Apple(snake.body)  # Initialise new apple

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
                        break
                    elif event.key == K_RIGHT and snake.get_direction() != LEFT:
                        snake.set_direction(RIGHT)
                        break
                    elif event.key == K_UP and snake.get_direction() != DOWN:
                        snake.set_direction(UP)
                        break
                    elif event.key == K_DOWN and snake.get_direction() != UP:
                        snake.set_direction(DOWN)
                        break

            if not snake.move():        # if snake can't move, call Game.gameover(), else move in current direction.
                Game.FPS = Game.starting_FPS          # reset game FPS
                Game.gameover()                       # call Game.gameover() screen

            if snake.eating(apple.x, apple.y):
                apple = Apple(snake.body)
                self.score += 1
                Screen.draw_btm_bar()
                Screen.display_btm_info(self.score)
                snake.grow()
                Game.FPS += 1       # Speed up game after every apple eaten

            Screen.update()
            Game.fpsClock.tick(Game.FPS)

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
                        Game()                  # Restart game

            Screen.display_msg("Press SPACE to play again")       # Displays instructions to restart game
            Screen.update()
            Game.fpsClock.tick(Game.FPS)



# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":
    new_game = Game()


