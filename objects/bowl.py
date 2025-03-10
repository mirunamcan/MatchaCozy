import pygame

class Bowl:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 150, 80)
        self.ingredients = []
        self.stirred = False
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GREEN = (56, 142, 60)

    def draw(self, screen):
        # Draw the bowl
        pygame.draw.ellipse(screen, self.WHITE, self.rect)
        pygame.draw.ellipse(screen, self.BLACK, self.rect, 2)

        # Draw content based on ingredients
        has_almond_milk = any(i.name == "Almond Milk" for i in self.ingredients)
        has_matcha = any(i.name == "Matcha Powder" for i in self.ingredients)

        if has_matcha or has_almond_milk:
            content_color = self.get_content_color()
            content_rect = pygame.Rect(
                self.rect.x + 10,
                self.rect.y + 20,
                self.rect.width - 20,
                self.rect.height - 30
            )
            pygame.draw.ellipse(screen, content_color, content_rect)

            # Show stirring pattern if stirred
            if self.stirred and has_matcha and has_almond_milk:
                for i in range(3):
                    pygame.draw.arc(
                        screen,
                        self.DARK_GREEN,
                        content_rect,
                        0.3 * i,
                        0.3 * i + 0.9,
                        2
                    )

            # Show matcha powder sprinkles if only matcha is added
            elif has_matcha and not has_almond_milk:
                for i in range(8):
                    x = self.rect.x + 20 + (i * 15) % (self.rect.width - 40)
                    y = self.rect.y + 25 + (i * 7) % (self.rect.height - 40)
                    pygame.draw.circle(screen, self.DARK_GREEN, (x, y), 3)

    def get_content_color(self):
        has_almond_milk = any(i.name == "Almond Milk" for i in self.ingredients)
        has_matcha = any(i.name == "Matcha Powder" for i in self.ingredients)

        if has_almond_milk and has_matcha and self.stirred:
            return (200, 230, 201)  # Light matcha green
        elif has_almond_milk and has_matcha and not self.stirred:
            return (230, 230, 200)  # Unmixed color
        elif has_almond_milk:
            return (240, 240, 230)  # Milk color
        elif has_matcha:
            return self.DARK_GREEN  # Matcha color
        else:
            return self.WHITE  # Empty

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)