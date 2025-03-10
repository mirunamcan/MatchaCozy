import pygame

class Ingredient:
    def __init__(self, name, color, x, y, width, height):
        self.name = name
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        font = pygame.font.SysFont(None, 20)
        text_surf = font.render(self.name, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)