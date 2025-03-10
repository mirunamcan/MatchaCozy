import pygame

class WhiskTool:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 100)
        self.selected = False
        self.BROWN = (165, 42, 42)
        self.GRAY = (200, 200, 200)
        self.RED = (229, 57, 53)

    def draw(self, screen):
        # Draw handle
        pygame.draw.rect(screen, self.BROWN, (self.rect.x + 15, self.rect.y, 10, 70))

        # Draw whisk part
        whisk_rect = pygame.Rect(self.rect.x, self.rect.y + 70, 40, 30)
        pygame.draw.ellipse(screen, self.GRAY, whisk_rect)

        if self.selected:
            pygame.draw.rect(screen, self.RED, self.rect, 2)  # Highlight when selected

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)