import pygame
from objects.game import MatchaGame

def main():
    pygame.init()
    game = MatchaGame()
    game.game_state = "start_screen"
    game.running = True
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()