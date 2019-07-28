from locals import *

class Screen:
    pygame.display.set_caption("Snake")  # Title bar of window
    surface = pygame.display.set_mode(WINDOW_SIZE)  # Create display surface and set to WINDOW_SIZE
    BG_COLOR = GREY
    SCORE_BAR_COLOR = WHITE
    POSITION = (0, SCREEN_HEIGHT, SCREEN_WIDTH, SCOREBAR)

    def __init__(self):
        """ Initialises new screen with score bar at bottom of window with colour white,
            then draws to display surface """

        self.fill_background()
        self.draw_scorebar()

    @staticmethod
    def fill_background():
        """ Fills background with game_bg_color """
        Screen.surface.fill(Screen.BG_COLOR)  # Fill window with game background colour

    @staticmethod
    def draw_scorebar():
        """ Draws score bar on display surface """
        pygame.draw.rect(Screen.surface, Screen.SCORE_BAR_COLOR, Screen.POSITION)

    @staticmethod
    def display_score(score):
        """ Displays the score onto the bottom of the window where the screen bar is """
        fontObj = pygame.font.Font("freesansbold.ttf",32)
        score_surface = fontObj.render("Score: {}".format(score), True, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT + (SCOREBAR / 2))
        Screen.surface.blit(score_surface, score_rect)

    @staticmethod
    def new_game_msg():
        """ Displays message showing how to start new game """
        fontObj = pygame.font.Font("freesansbold.ttf",22)
        new_game_surface = fontObj.render("Press SPACE to play again", True, BLACK)
        new_game_rect = new_game_surface.get_rect()
        new_game_rect.center = (SCREEN_WIDTH / 2,SCREEN_HEIGHT /2)
        Screen.surface.blit(new_game_surface, new_game_rect)



# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":

    screen = Screen()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
