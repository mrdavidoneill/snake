from locals import *

class Screen:

    ######## USER CHANGEABLE DATA ########

    S_TITLE = "Snake"  # Window title
    SCREEN_SIZE = (30, 30)  # Playing area in grid cells
    GRID_SIZE = 10          # Grid size in pixels
    BG_COLOR = GREY         # Playing area background colour
    T_BG_COLOR = R_BG_COLOR = B_BG_COLOR = L_BG_COLOR = BLACK   # Side panels background colour
    T_SIZE, R_SIZE, B_SIZE, L_SIZE = (5, 5, 10, 5)              # Side panels sizes in grid cells (0 = Non existent)

    ############### END ###################

    # Outside panel sizes in pixels
    TOPBAR = GRID_SIZE * T_SIZE
    RIGHTBAR = GRID_SIZE * R_SIZE
    BOTTOMBAR = GRID_SIZE * B_SIZE
    LEFTBAR = GRID_SIZE * L_SIZE

    SCREEN_WIDTH = GRID_SIZE * SCREEN_SIZE[0]  # Playing screen width in pixels
    SCREEN_HEIGHT = GRID_SIZE * SCREEN_SIZE[1]  # Playing screen height in pixels

    WINDOW_WIDTH = SCREEN_WIDTH + LEFTBAR + RIGHTBAR
    WINDOW_HEIGHT = SCREEN_HEIGHT + TOPBAR + BOTTOMBAR
    WINDOW_SIZE = (WINDOW_WIDTH,  WINDOW_HEIGHT)

    GRID_WIDTH = int(SCREEN_WIDTH / GRID_SIZE)  # Total number of grid squares on x axis
    GRID_HEIGHT = int(SCREEN_HEIGHT / GRID_SIZE)  # Total number of grid squares on y axis

    GRID_MID_Y = int(((SCREEN_HEIGHT / 2 + TOPBAR) / GRID_SIZE))  # Mid point on y axis in Grid coordinates
    GRID_MID_X = int(((SCREEN_WIDTH / 2 + LEFTBAR) / GRID_SIZE)) # Mid point on x axis in Grid coordinates

    # Grid boundaries in grid coordingates
    GRIDX_0 = int(LEFTBAR / GRID_SIZE)
    GRIDX_MAX = int((SCREEN_WIDTH + LEFTBAR) / GRID_SIZE)

    GRIDY_0 = int(TOPBAR / GRID_SIZE)
    GRIDY_MAX = int((SCREEN_HEIGHT + TOPBAR) / GRID_SIZE)

    TOP_BAR = (0,0,WINDOW_WIDTH,T_SIZE * GRID_SIZE)
    BTM_BAR = (0, WINDOW_HEIGHT - (B_SIZE * GRID_SIZE), WINDOW_WIDTH, WINDOW_HEIGHT)
    LEFT_BAR = (0, 0, L_SIZE * GRID_SIZE, WINDOW_HEIGHT)
    RIGHT_BAR = (WINDOW_WIDTH - (R_SIZE * GRID_SIZE), 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    surface = None

    BTM_FONT = pygame.font.Font("freesansbold.ttf", min(int(SCREEN_WIDTH/10), 40))
    ONSCREEN_FONT = pygame.font.Font("freesansbold.ttf", int(SCREEN_WIDTH/15))

    @staticmethod
    def start_screen():
        """ Starts screen with options as spceified above in the class fields """

        Screen.surface = pygame.display.set_mode(Screen.WINDOW_SIZE)
        pygame.display.set_caption(Screen.S_TITLE)

        Screen.fill_background()
        Screen.draw_top_bar()
        Screen.draw_btm_bar()
        Screen.draw_left_bar()
        Screen.draw_right_bar()

    @staticmethod
    def fill_background():
        """ Fills background with game_bg_color """
        Screen.surface.fill(Screen.BG_COLOR)

    @staticmethod
    def draw_top_bar():
        """ Draws score bar on display surface """
        pygame.draw.rect(Screen.surface, Screen.T_BG_COLOR, Screen.TOP_BAR)

    @staticmethod
    def draw_right_bar():
        """ Draws score bar on display surface """
        pygame.draw.rect(Screen.surface, Screen.R_BG_COLOR, Screen.RIGHT_BAR)

    @staticmethod
    def draw_btm_bar():
        """ Draws score bar on display surface """
        pygame.draw.rect(Screen.surface, Screen.B_BG_COLOR, Screen.BTM_BAR)

    @staticmethod
    def draw_left_bar():
        """ Draws score bar on display surface """
        pygame.draw.rect(Screen.surface, Screen.L_BG_COLOR, Screen.LEFT_BAR)

    @staticmethod
    def display_btm_info(score):
        """ Displays the score onto the bottom of the window where the bottom bar is """
        score_surface = Screen.BTM_FONT.render("Score: {}".format(score), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.center = (Screen.WINDOW_WIDTH / 2, Screen.WINDOW_HEIGHT - (Screen.BOTTOMBAR / 2))
        Screen.surface.blit(score_surface, score_rect)

    @staticmethod
    def display_msg(msg):
        """ Displays message showing how to start new game """
        new_game_surface = Screen.ONSCREEN_FONT.render(msg, True, BLACK)
        new_game_rect = new_game_surface.get_rect()
        new_game_rect.center = (Screen.WINDOW_WIDTH / 2,
                                (Screen.WINDOW_HEIGHT - Screen.BOTTOMBAR - Screen.TOPBAR) /2 + Screen.TOPBAR)
        Screen.surface.blit(new_game_surface, new_game_rect)

    @staticmethod
    def update():
        """ Updates Screen """
        pygame.display.update()

# ================ FOR TESTING PURPOSES ================ #

if __name__ == "__main__":

    Screen.start_screen()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        Screen.update()
