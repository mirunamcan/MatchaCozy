import pygame


class Glass:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.GLASS_COLOR = (220, 240, 255, 150)
        self.LIGHT_GREEN = (200, 230, 201)

    def draw(self, screen, filled=False, fill_level=0):
        # Draw glass with better shape
        # Glass exterior
        pygame.draw.rect(screen, self.GLASS_COLOR, (self.x, self.y, self.width, self.height))

        # Glass edges with gradient for 3D effect
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, (180, 200, 225), (self.x + self.width, self.y),
                         (self.x + self.width, self.y + self.height), 2)

        # Glass top and bottom edges
        pygame.draw.line(screen, (200, 220, 240), (self.x, self.y), (self.x + self.width, self.y), 1)
        pygame.draw.line(screen, (150, 180, 210), (self.x, self.y + self.height - 1),
                         (self.x + self.width, self.y + self.height - 1), 2)

        # Draw liquid if filled
        if filled:
            matcha_in_glass = pygame.Rect(
                self.x + 3,
                self.y + 3,
                self.width - 6,
                self.height - 6
            )
            pygame.draw.rect(screen, self.LIGHT_GREEN, matcha_in_glass)

            # Add shine to liquid
            shine_height = min(8, (self.height - 6) // 3)
            shine = pygame.Rect(
                self.x + 6,
                self.y + 6,
                self.width // 3,
                shine_height
            )
            pygame.draw.rect(screen, (220, 255, 220), shine)

        # Draw partially filled
        elif fill_level > 0:
            fill_height = int(fill_level * (self.height - 6))
            matcha_in_glass = pygame.Rect(
                self.x + 3,
                self.y + self.height - 3 - fill_height,
                self.width - 6,
                fill_height
            )


            # Add liquid shine
            if fill_height > 10:
                shine = pygame.Rect(
                    self.x + 6,
                    self.y + self.height - 3 - fill_height + 2,
                    self.width // 3,
                    min(6, fill_height // 4)
                )
                pygame.draw.rect(screen, (220, 255, 220), shine)
