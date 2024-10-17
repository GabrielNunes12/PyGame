#Enum for the game state to be used in the game engine

class GameState(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3
    PAUSE = 4
    QUIT = 5