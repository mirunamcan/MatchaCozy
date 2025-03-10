import pygame
import sys
from objects.game import MatchaGame

# Initialize pygame
pygame.init()

if __name__ == "__main__":
    game = MatchaGame()
    try:
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()