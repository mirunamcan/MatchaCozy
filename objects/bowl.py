import os
import pygame
import time
import math
import random


class Bowl:
    def __init__(self, x, y, width=400, height=250):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.contents = []
        self.is_stirred = False

        # Load bowl image
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            bowl_path = os.path.join(base_dir, 'assets', 'bowl.png')
            self.image = pygame.image.load(bowl_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except Exception as e:
            print(f"Error loading bowl image: {e}")
            self.image = None
            # Create a fallback image
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 150, 100))

        # Milk surface
        self.milk_image = pygame.Surface((self.width - 40, self.height - 20), pygame.SRCALPHA)
        self.milk_image.fill((240, 240, 230, 200))  # Off-white with transparency

        # Matcha powder surface - USES PARTICLE SYSTEM INSTEAD OF SOLID COLOR
        self.matcha_image = pygame.Surface((self.width - 40, self.height - 20), pygame.SRCALPHA)
        # Don't fill with solid color - draw particles instead
        self.draw_matcha_powder(self.matcha_image)

        # Mixed matcha surface
        self.mixed_image = pygame.Surface((self.width - 40, self.height - 20), pygame.SRCALPHA)
        self.mixed_image.fill((180, 210, 150, 200))  # Light green with transparency
    def draw(self, screen):
        # First draw the bowl image
        screen.blit(self.image, (self.x, self.y))


    def draw_matcha_powder(self, surface):
        # Use a solid color with transparency instead of particles
        color = (75, 139, 59, 100)  # Light green with high transparency

    def is_clicked(self, pos):
        click_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return click_rect.collidepoint(pos)

    def stop_milk_sound(self):
        # This method will be called when mixer is clicked
        if 'milk' in self.contents and hasattr(self, 'milk_sound') and self.milk_sound.get_busy():
            self.milk_sound.stop()