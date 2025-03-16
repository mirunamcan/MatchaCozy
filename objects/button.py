import pygame
class Button:
    def __init__(self, x, y, width, height, text, color=(76, 175, 80), hover_color=(56, 142, 60), font_size=32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font_size = font_size
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # Draw shadow
        shadow_rect = pygame.Rect(self.x + 3, self.y + 3, self.width, self.height)
        pygame.draw.rect(screen, (100, 100, 100), shadow_rect, border_radius=15)

        # Draw main button with gradient effect
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=15)

        # Draw inner highlight
        highlight_rect = pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height // 2 - 3)
        pygame.draw.rect(screen, (*[min(255, c + 30) for c in self.current_color[:3]], 150),
                         highlight_rect, border_radius=15)

        # Draw border
        pygame.draw.rect(screen, (60, 100, 60), self.rect, 2, border_radius=15)

        # Add button text with shadow
        font = pygame.font.SysFont('arial', self.font_size, bold=True)

        # Text shadow
        text_shadow = font.render(self.text, True, (50, 80, 50))
        text_shadow_rect = text_shadow.get_rect(center=(self.x + self.width // 2 + 2,
                                                        self.y + self.height // 2 + 2))
        screen.blit(text_shadow, text_shadow_rect)

        # Main text
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2,
                                               self.y + self.height // 2))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color