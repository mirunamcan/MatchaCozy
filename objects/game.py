import pygame
import time
import os
import random
from objects.bowl import Bowl
from objects.whisk import WhiskTool
from objects.button import Button


class MatchaGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BOWL_X = 325
        self.BOWL_Y = 300
        self.GLASS_X = 600
        self.GLASS_Y = 350

        # Matcha animation attributes
        self.matcha_particles = []
        self.is_matcha_falling = False
        self.matcha_fall_start_time = 0
        self.matcha_fall_duration = 1.5  # seconds

        # Water animation attributes
        self.water_particles = []
        self.is_water_falling = False
        self.water_fall_start_time = 0
        self.water_fall_duration = 1.5  # seconds

        # Milk animation attributes - ADD THESE LINES
        self.milk_particles = []
        self.is_milk_falling = False
        self.milk_fall_start_time = 0
        self.milk_fall_duration = 1.5  # seconds

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Matcha Making Game")

        # Rest of your initialization code...
        # seconds
        # seconds
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (75, 139, 59)
        self.LIGHT_GREEN = (180, 210, 150)
        self.BROWN = (139, 69, 19)



        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Game state
        self.game_state = "start_screen"
        self.running = True

        # THEN load the background
        try:
            bg_path = os.path.join(self.base_dir, 'assets', 'kawaii_kitchen.png')
            print(f"Looking for background at: {bg_path}")
            if os.path.exists(bg_path):
                print(f"File exists: {bg_path}")
                self.background_image = pygame.image.load(bg_path).convert()
                self.background_image = pygame.transform.scale(self.background_image,
                                                               (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            else:
                print(f"File not found: {bg_path}")
                self.background_image = None
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background_image = None

        # Set up the display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Matcha Making Game")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        # Game objects
        self.running = True

        # Setup bowl first - IMPORTANT: Call setup_bowl() instead of direct assignment
        self.setup_bowl()

        self.setup_whisk()
        self.has_matcha = False
        self.has_hot_water = False
        self.is_mixed_with_water = False
        self.has_almond_milk = False
        self.is_fully_mixed = False
        self.is_poured = False
        self.pouring = False
        self.pour_progress = 0.0
        self.pour_animation_start = 0
        self.pour_animation_duration = 2.0  # seconds
        self.pour_angle = 0
        self.glass_ready = False
        self.can_click_glass = False
        self.recipe_complete = False
        self.score = 0
        self.time_left = 60
        self.game_over = False

        # Message system
        self.message = "Start by adding matcha powder to the bowl!"
        self.message_time = time.time()
        self.message_duration = 3.0  # seconds

        # Initialize ingredients
        self.setup_ingredients()

        # Create buttons
        self.setup_buttons()

        # Initialize glass
        self.setup_glass()
        try:
            water_sound_path = os.path.join(self.base_dir, 'assets', 'water_drop.mp3')
            self.water_sound = pygame.mixer.Sound(water_sound_path)
        except Exception as e:
            print(f"Error loading water sound: {e}")
            self.water_sound = None
        try:
            whisk_sound_path = os.path.join(self.base_dir, 'assets', 'whisk.mp3')
            self.whisk_sound = pygame.mixer.Sound(whisk_sound_path)
        except Exception as e:
            print(f"Error loading whisk sound: {e}")
            self.whisk_sound = None
        try:
            milk_sound_path = os.path.join(self.base_dir, 'assets', 'milk_pour.mp3')
            self.milk_sound = pygame.mixer.Sound(milk_sound_path)
        except Exception as e:
            print(f"Error loading milk sound: {e}")
            self.milk_sound = None

    def setup_ingredients(self):
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
                self.rect = pygame.Rect(x, y, width, height)

                if image_path:
                    try:
                        full_path = os.path.join(self.base_dir, image_path)
                        print(f"Loading {name} image from: {full_path}")
                        if os.path.exists(full_path):
                            print(f"File exists for {name}")
                            self.image = pygame.image.load(full_path)
                            self.image = pygame.transform.scale(self.image, (width, height))
                        else:
                            print(f"File not found: {full_path}")
                    except Exception as e:
                        print(f"Error loading {name} image: {e}")
                        self.image = None

            def draw(self, screen):
                if self.visible and self.image:
                    screen.blit(self.image, (self.x, self.y))

            def is_clicked(self, pos):
                return self.rect.collidepoint(pos)

        # Create ingredient instances
        self.ingredients = [
            Ingredient(40, 50, 150, 150, "Matcha", self.base_dir, "assets/matcha_powder.png"),
            Ingredient(40, 220, 150, 150, "Bouillote", self.base_dir, "assets/bouillote.png"),
            Ingredient(50, 340, 100, 100, "Almond Milk", self.base_dir, "assets/almond_milk.png")
        ]
    def setup_bowl(self):
        # Make the bowl much larger and centered on screen
        bowl_width = 600 # Large bowl width
        bowl_height = 500# Large bowl height

        # Center the bowl horizontally and vertically
        bowl_x = (self.SCREEN_WIDTH - bowl_width) // 2
        bowl_y = (self.SCREEN_HEIGHT - bowl_height) // 2

        # Update BOWL_X and BOWL_Y constants for reference elsewhere
        self.BOWL_X = bowl_x
        self.BOWL_Y = bowl_y

        # Create bowl with new dimensions and position
        self.bowl = Bowl(bowl_x, bowl_y, width=bowl_width, height=bowl_height)

        # Add contents attribute if it doesn't exist
        if not hasattr(self.bowl, 'contents'):
            self.bowl.contents = []

    def setup_whisk(self):
        # Position whisk in the center, and make it much larger
        whisk_x = self.SCREEN_WIDTH // 2 - 150  # Centered horizontally
        whisk_y = 20  # Higher position at top
        whisk_width = 300  # Much larger width
        whisk_height = 200  # Much larger height

        # Create whisk with much larger dimensions
        self.whisk = WhiskTool(whisk_x, whisk_y, width=whisk_width, height=whisk_height)

        # Make sure the whisk tool has the necessary attributes and methods
        if not hasattr(self.whisk, 'visible'):
            self.whisk.visible = True

        # Update the draw method if it doesn't display properly
        def enhanced_draw(screen):
            if self.whisk.visible:
                if hasattr(self.whisk, 'image') and self.whisk.image:
                    screen.blit(self.whisk.image, (self.whisk.x, self.whisk.y))
                else:
                    # Fallback drawing if image is missing
                    pygame.draw.ellipse(screen, (150, 75, 0),
                                        (self.whisk.x, self.whisk.y,
                                         self.whisk.width, self.whisk.height))


        # Replace the draw method if needed
        if not hasattr(self.whisk, 'draw') or not callable(self.whisk.draw):
            self.whisk.draw = enhanced_draw
    def setup_glass(self):
        # Define glass class locally
        class Glass:
            def __init__(self, x, y, width=80, height=120):
                self.x = x
                self.y = y
                self.width = width
                self.height = height

            def draw(self,
                     screen, fill_level=0):
                # Draw glass outline
                pygame.draw.rect(screen, (200, 200, 220),
                                 (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.x, self.y, self.width, self.height), 2)

                # Draw liquid if filling
                if fill_level > 0:
                    fill_height = int(self.height * fill_level)
                    fill_y = self.y + self.height - fill_height
                    pygame.draw.rect(screen, (180, 210, 150),
                                     (self.x + 2, fill_y, self.width - 4, fill_height))

                # Draw "GLASS" label
                font = pygame.font.SysFont(None, 20)
                text_surf = font.render("GLASS", True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=(self.x + self.width // 2,
                                                       self.y + self.height + 15))
                screen.blit(text_surf, text_rect)

            def is_clicked(self, pos):
                click_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                return click_rect.collidepoint(pos)

        # Bind Glass to self
        self.Glass = Glass

        # Create glass with explicit position instead of trying to calculate it inside Glass.__init__
        self.glass = Glass(self.GLASS_X, self.GLASS_Y, width=80, height=120)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        if hasattr(self, 'pour_button'):
            self.pour_button.update(mouse_pos)
        if hasattr(self, 'next_button'):
            self.next_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN and self.game_state == "start_screen":
                self.game_state = "game_screen"
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "game_screen":
                # Handle whisk click first
                if self.whisk.is_clicked(mouse_pos) and self.whisk.visible:
                    # Stop milk sound if it's playing when mixing after adding milk
                    if hasattr(self, 'milk_sound') and self.milk_sound and self.has_almond_milk:
                        self.milk_sound.stop()

                    if hasattr(self, 'whisk_sound') and self.whisk_sound:
                        self.whisk_sound.play()

                    if self.has_hot_water and not self.is_mixed_with_water:
                        self.is_mixed_with_water = True
                        self.bowl.is_stirred = True
                        self.message = "Well mixed! Add almond milk now."
                        self.message_time = time.time()
                    elif self.has_almond_milk and not self.is_fully_mixed:
                        self.is_fully_mixed = True
                        self.bowl.is_stirred = True
                        self.message = "Perfect! Your matcha is ready to pour."
                        self.message_time = time.time()
                    return

                if self.is_poured and hasattr(self, 'next_button'):
                    if self.next_button.is_clicked(mouse_pos):
                        print("Next button clicked")  # Debug print
                        self.score += 1
                        self.reset_game()
                        return

                # Handle ingredient clicks
                for ingredient in self.ingredients:
                    if ingredient.is_clicked(mouse_pos) and ingredient.visible:
                        if ingredient.name == "Matcha" and not self.has_matcha:
                            print("Matcha clicked")  # Debug print
                            self.create_matcha_powder_animation()
                            self.bowl.contents.append('matcha')
                            self.has_matcha = True
                            self.message = "Matcha added! Now add hot water."
                            self.message_time = time.time()
                            return
                        elif ingredient.name == "Bouillote" and self.has_matcha and not self.has_hot_water:
                            print("Hot water clicked")  # Debug print
                            if hasattr(self, 'water_sound') and self.water_sound:
                                self.water_sound.play()
                            self.create_water_animation()
                            self.bowl.contents.append('water')
                            self.has_hot_water = True
                            self.message = "Hot water added! Now mix with the whisk."
                            self.message_time = time.time()
                            return
                        elif ingredient.name == "Almond Milk" and self.is_mixed_with_water and not self.has_almond_milk:
                            print("Almond milk clicked")  # Debug print
                            # Stop whisk sound if it's playing
                            if hasattr(self, 'whisk_sound') and self.whisk_sound:
                                self.whisk_sound.stop()
                            # Play milk sound if available
                            if hasattr(self, 'milk_sound') and self.milk_sound:
                                self.milk_sound.play()
                            # Create milk pouring animation
                            self.create_milk_animation()
                            self.bowl.contents.append('milk')
                            self.has_almond_milk = True
                            self.message = "Almond milk added! Mix again to complete."
                            self.message_time = time.time()
                            return
    def update_game_state(self):
        # Update animations, timers, etc.
        self.update_pour_animation()
        self.update_matcha_animation()
        self.update_water_animation()
        self.update_milk_animation()

        # Update timer
        if not self.game_over and not self.recipe_complete:
            self.time_left = max(0, self.time_left - 1 / 60)  # 1/60 second per frame at 60 FPS
            if self.time_left <= 0:
                self.game_over = True
                self.message = f"Game Over! Your score: {self.score}"
                self.message_time = float('inf')  # Keep the message visible

    def update_pour_animation(self):
        if self.pouring:
            current_time = time.time()
            elapsed = current_time - self.pour_animation_start

            # Calculate animation progress (0.0 to 1.0)
            self.pour_progress = min(elapsed / self.pour_animation_duration, 1.0)

            # Update pour angle (0 to 60 degrees)
            self.pour_angle = self.pour_progress * 60

            # When animation completes
            if self.pour_progress >= 1.0:
                self.pouring = False
                self.is_poured = True
                self.glass_ready = True
                self.message = "Matcha poured! Click 'Next Matcha' to make another."
                self.message_time = time.time()
                self.recipe_complete = True

    def reset_game(self):
        # Reset game state for a new matcha
        self.setup_bowl()
        self.pouring = False
        self.pour_progress = 0.0
        self.glass_ready = False
        self.can_click_glass = False

        # Reset recipe status with proper flow
        self.has_matcha = False
        self.has_hot_water = False
        self.is_mixed_with_water = False
        self.has_almond_milk = False
        self.is_fully_mixed = False
        self.is_poured = False
        self.recipe_complete = False

        # Make ingredients visible again - keep this to ensure everything resets properly
        for ingredient in self.ingredients:
            ingredient.visible = True

        self.message = "Start by adding matcha powder to the bowl!"
        self.message_time = time.time()

    def run(self):
        while self.running:
            # Update game state
            if self.game_state == "game_screen":
                self.update_game_state()

            # Handle events
            self.handle_events()

            # Draw appropriate screen
            if self.game_state == "start_screen":
                self.draw_start_screen()
            else:
                self.draw_game_screen()

            # Update display
            pygame.display.flip()
            self.clock.tick(60)
    def draw_start_screen(self):
        # Draw background
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((230, 230, 250))  # Light background

        # Draw title
        font_large = pygame.font.SysFont(None, 72)
        title = font_large.render("Matcha Maker", True, (0, 100, 0))
        self.screen.blit(title, (self.SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        # Draw "press any key" message (blinking)
        if pygame.time.get_ticks() % 1000 < 800:  # Blink effect
            font = pygame.font.SysFont(None, 36)
            text = font.render("Press any key to start", True, (0, 0, 0))
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, 350))

    def draw_game_screen(self):
        # Draw background
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.WHITE)

        # Draw all game elements
        self.bowl.draw(self.screen)
        for ingredient in self.ingredients:
            ingredient.draw(self.screen)
        self.whisk.draw(self.screen)  # Draw whisk only once
        self.draw_matcha_animation()
        self.draw_water_animation()
        self.draw_milk_animation()

        # Draw glass
        if self.glass_ready:
            self.glass.draw(self.screen, fill_level=self.pour_progress)
        else:
            self.glass.draw(self.screen)

        if self.is_fully_mixed and not self.is_poured:
            self.pour_button.draw(self.screen)

        if self.is_poured and self.recipe_complete:
            self.next_button.draw(self.screen)

        # Draw "next matcha" button if poured
        if self.is_poured:
            self.next_button.draw(self.screen)

        # Draw pouring animation
        if self.pouring:
            self.draw_pouring_animation()

        # Draw message
        if self.message:
            message_text = self.font.render(self.message, True, self.BLACK)
            self.screen.blit(message_text, (self.SCREEN_WIDTH // 2 - message_text.get_width() // 2, 520))

        # Draw score and time
        score_text = self.small_font.render(f"Score: {self.score}", True, self.BLACK)
        time_text = self.small_font.render(f"Time: {int(self.time_left)}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(time_text, (self.SCREEN_WIDTH - 100, 10))


    def setup_buttons(self):
        # Define button class
        class Button:
            def __init__(self, x, y, width, height, text, color, hover_color):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.text = text
                self.color = color
                self.hover_color = hover_color
                self.current_color = color
                self.water_particles = []
                self.is_water_falling = False
                self.water_fall_start_time = 0
                self.water_fall_duration = 1.5  # seconds
                self.milk_particles = []
                self.is_milk_falling = False
                self.milk_fall_start_time = 0
                self.milk_fall_duration = 1.5  # seconds

            def draw(self, screen):


                font = pygame.font.SysFont(None, 28)
                text_surf = font.render(self.text, True, (0, 0, 0))
                text_rect = text_surf.get_rect(center=(self.x + self.width // 2,
                                                       self.y + self.height // 2))
                screen.blit(text_surf, text_rect)

            def is_clicked(self, pos):
                click_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                return click_rect.collidepoint(pos)

            def update(self, mouse_pos):
                if self.is_clicked(mouse_pos):
                    self.current_color = self.hover_color
                else:
                    self.current_color = self.color

        # Store Button class
        self.Button = Button

        # Create button instances
        self.pour_button = Button(
            x=400,
            y=450,
            width=150,
            height=50,
            text="Pour Matcha",
            color=(200, 220, 200),
            hover_color=(180, 210, 180)
        )

        self.next_button = Button(
            x=400,
            y=450,
            width=150,
            height=50,
            text="Next Matcha",
            color=(200, 220, 200),
            hover_color=(180, 210, 180)
        )

    def create_matcha_powder_animation(self):
        self.matcha_particles = []
        start_x = self.bowl.x + self.bowl.width // 2
        start_y = 50  # Start position above the bowl

        # Create more particles with adjusted properties
        for _ in range(150):  # Increased number of particles
            particle = {
                'x': start_x + random.randint(-50, 50),  # Tighter spread
                'y': start_y,
                'speed_y': random.uniform(1, 3),  # Slower fall speed
                'speed_x': random.uniform(-0.3, 0.3),  # Reduced horizontal movement
                'size': random.randint(2, 5),  # Slightly larger particles
                'alpha': random.randint(150, 255),  # More varying opacity
                'life': 1.0
            }
            self.matcha_particles.append(particle)
        self.is_matcha_falling = True
        self.matcha_fall_start_time = time.time()

    def draw_matcha_animation(self):
        if not self.is_matcha_falling:
            return

        # Create a surface for all particles
        particles_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)

        for particle in self.matcha_particles:
            if particle['life'] > 0:
                # Matcha green color with alpha
                alpha = int(particle['alpha'] * particle['life'])
                color = (75, 139, 59, alpha)

                # Draw particle
                pygame.draw.circle(particles_surface, color,
                                   (int(particle['x']), int(particle['y'])),
                                   particle['size'])

        # Blit the particles surface to the screen
        self.screen.blit(particles_surface, (0, 0))

    def update_matcha_animation(self):
        if not self.is_matcha_falling:
            return

        current_time = time.time()
        elapsed = current_time - self.matcha_fall_start_time

        # Stop animation after duration
        if elapsed > self.matcha_fall_duration:
            self.is_matcha_falling = False
            return



        # Update each particle
        for particle in self.matcha_particles:
            if particle['life'] > 0:
                # Update position with smoother movement
                particle['x'] += particle['speed_x']
                particle['y'] += particle['speed_y']

                # Gradually reduce life based on vertical position
                bowl_center_y = self.BOWL_Y + 100
                if particle['y'] > bowl_center_y:
                    particle['life'] -= 0.1

                # Add slight wind effect
                particle['speed_x'] += random.uniform(-0.05, 0.05)

                # Apply gentle gravity
                particle['speed_y'] += 0.05



    def create_water_animation(self):
        self.water_particles = []
        start_x = self.bowl.x + self.bowl.width // 2
        start_y = 50  # Start position above the bowl

        # Create water droplets
        for _ in range(100):  # Number of water droplets
            particle = {
                'x': start_x + random.randint(-80, 80),
                'y': start_y,
                'speed_y': random.uniform(5, 8),  # Faster fall speed for water
                'speed_x': random.uniform(-0.2, 0.2),
                'size': random.randint(3, 6),  # Slightly larger drops
                'alpha': random.randint(150, 200),  # More transparency for water
                'life': 1.0
            }
            self.water_particles.append(particle)
        self.is_water_falling = True
        self.water_fall_start_time = time.time()

    def draw_water_animation(self):
        if not self.is_water_falling:
            return

        # Create a surface for all water particles
        particles_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)

        for particle in self.water_particles:
            if particle['life'] > 0:
                # Water blue color with alpha
                alpha = int(particle['alpha'] * particle['life'])
                color = (150, 200, 255, alpha)  # Light blue color

                # Draw water droplet as a vertical oval
                pygame.draw.ellipse(particles_surface, color,
                                    (int(particle['x'] - particle['size'] / 2),
                                     int(particle['y'] - particle['size']),
                                     particle['size'],
                                     particle['size'] * 2))

        # Blit the particles surface to the screen
        self.screen.blit(particles_surface, (0, 0))

    def update_water_animation(self):
        if not self.is_water_falling:
            return

        current_time = time.time()
        elapsed = current_time - self.water_fall_start_time

        # Stop animation after duration
        if elapsed > self.water_fall_duration:
            self.is_water_falling = False
            return

        # Update each particle
        for particle in self.water_particles:
            if particle['life'] > 0:
                # Update position
                particle['x'] += particle['speed_x']
                particle['y'] += particle['speed_y']

                # Gradually reduce life based on vertical position
                bowl_center_y = self.BOWL_Y + 100
                if particle['y'] > bowl_center_y:
                    particle['life'] -= 0.1

                # Add slight acceleration for gravity
                particle['speed_y'] += 0.2

    def create_milk_animation(self):
        self.milk_particles = []
        start_x = self.bowl.x + self.bowl.width // 2
        start_y = 50  # Start position above the bowl

        # Create main milk stream
        for _ in range(150):
            particle = {
                'x': start_x + random.randint(-60, 60),
                'y': start_y,
                'speed_y': random.uniform(4, 8),
                'speed_x': random.uniform(-0.3, 0.3),
                'size': random.randint(3, 8),
                'alpha': random.randint(180, 230),
                'life': 1.0,
                'is_splash': False
            }
            self.milk_particles.append(particle)

        self.is_milk_falling = True
        self.milk_fall_start_time = time.time()

    def draw_milk_animation(self):
        if not self.is_milk_falling:
            return

        particles_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)

        for particle in self.milk_particles:
            if particle['life'] > 0:
                # Creamy white color with alpha
                alpha = int(particle['alpha'] * particle['life'])
                color = (240, 235, 220, alpha)  # Creamy white color

                # Draw milk droplet as an oval
                pygame.draw.ellipse(particles_surface, color,
                                    (int(particle['x'] - particle['size'] / 2),
                                     int(particle['y'] - particle['size']),
                                     particle['size'],
                                     particle['size'] * 2))

        self.screen.blit(particles_surface, (0, 0))

    def update_milk_animation(self):
        if not self.is_milk_falling:
            return

        current_time = time.time()
        elapsed = current_time - self.milk_fall_start_time

        # Stop animation after duration
        if elapsed > self.milk_fall_duration:
            self.is_milk_falling = False
            return

        # Bowl impact position
        bowl_center_y = self.BOWL_Y + 100

        # Update each particle
        for particle in self.milk_particles:
            if particle['life'] > 0:
                # Update position
                particle['x'] += particle['speed_x']
                particle['y'] += particle['speed_y']

                # Add gravity
                particle['speed_y'] += 0.2

                # Create splash when hitting the bowl
                if particle['y'] > bowl_center_y and not particle.get('is_splash', False):
                    # Create splash particles
                    if random.random() < 0.05:  # Only some particles create splashes
                        self.create_splash(particle['x'], bowl_center_y)

                    # Reduce life of main droplet
                    particle['life'] -= 0.1

                    # Fade out particles gradually
                    particle['alpha'] = max(0, particle['alpha'] - 3)
                elif particle.get('is_splash', False):
                    # Splash particles fade more quickly
                    particle['life'] -= 0.05
                    particle['alpha'] = max(0, particle['alpha'] - 5)

    def create_splash(self, x, y):
        # Create 3-7 splash particles at impact point
        for _ in range(random.randint(3, 7)):
            # Splash particles move outward and slightly upward
            splash = {
                'x': x,
                'y': y,
                'speed_x': random.uniform(-2, 2),  # Move outward in x direction
                'speed_y': random.uniform(-3, -1),  # Move slightly upward
                'size': random.randint(1, 4),  # Smaller than regular drops
                'alpha': random.randint(100, 180),  # More transparent
                'life': 0.8,  # Shorter lifespan
                'is_splash': True
            }
            self.milk_particles.append(splash)