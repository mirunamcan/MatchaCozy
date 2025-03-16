import pygame
from objects.game import MatchaGame


def main():
    pygame.init()
    game = MatchaGame()
    pygame.display.set_caption("Matcha Cozy")
    pygame.display.set_icon(pygame.image.load("assets/logo.png"))
    game.game_state = "start_screen"
    game.running = True
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()