import pygame
import os


class WhiskTool:
    def __init__(self, x, y, width=300, height=200):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.image = None

        # Charge l'image du fouet
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            image_path = os.path.join(base_dir, 'assets', 'whisk.png')
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width, height))
        except Exception as e:
            print(f"Erreur chargement image fouet: {e}")
            # Pas de surface de repli - on laisse self.image comme None

    def draw(self, screen):
        if self.visible:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            # Ne rien dessiner si pas d'image

    def is_clicked(self, pos):
        if not self.visible:
            return False
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def stir(self):
        # Animation de mélange peut être ajoutée ici
        pass