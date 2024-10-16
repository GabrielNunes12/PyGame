import pygame
from GameEngine.gameEngine import GameEngine


def main():
    pygame.init()
    game = GameEngine()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()