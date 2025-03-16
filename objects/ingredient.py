import pygame
import os


class Ingredient:
    def __init__(self, x, y, width, height, name, base_dir, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.visible = True
        self.image = None
        self.base_dir = base_dir

        if image_path:
            try:
                full_path = os.path.join(self.base_dir, image_path)
                print(f"Loading {name} image from: {full_path}")  # Debug print
                if os.path.exists(full_path):
                    print(f"File exists for {name}")  # Debug print
                    self.image = pygame.image.load(full_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (width, height))
                    print(f"Successfully loaded {name} image")  # Debug print
                else:
                    print(f"File not found: {full_path}")  # Debug print
                    self.image = None
            except Exception as e:
                print(f"Error loading {name} image: {e}")  # Debug print
                self.image = None
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))
            # Text rendering completely removed

    def is_clicked(self, pos):
        if not self.visible:
            return False
        return self.rect.collidepoint(pos)