import pygame
import time
import sys
from objects.button import Button
from objects.ingredient import Ingredient
from objects.bowl import Bowl
from objects.whisk import WhiskTool


class MatchaGame:
    def __init__(self):
        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (76, 175, 80)
        self.LIGHT_GREEN = (200, 230, 201)
        self.DARK_GREEN = (56, 142, 60)
        self.RED = (229, 57, 53)
        self.GRAY = (200, 200, 200)
        self.GLASS_COLOR = (220, 240, 255)
        self.LIGHT_PINK = (255, 230, 240)
        self.FANTASY_GREEN = (45, 162, 95)

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Matcha Cozy")
        self.clock = pygame.time.Clock()

        # Load the kitchen background image from assets folder
        try:
            self.game_background = pygame.image.load("assets/kawaii_kitchen.png").convert()
            # Scale the image to fit the screen if necessary
            self.game_background = pygame.transform.scale(self.game_background,
                                                          (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except pygame.error:
            # Create kawaii kitchen background for gameplay if image can't be loaded
            self.game_background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.game_background.fill((255, 230, 240))  # Soft pink background

            # Add kawaii elements to the background
            pygame.draw.circle(self.game_background, (255, 255, 200), (100, 100), 50)  # Yellow sun
            pygame.draw.rect(self.game_background, (200, 230, 255), (600, 100, 150, 150))  # Blue window
            pygame.draw.rect(self.game_background, (245, 245, 220), (50, 300, 200, 200))  # Counter
            pygame.draw.rect(self.game_background, (220, 220, 220), (300, 350, 150, 150))  # Stove
            print("Failed to load background image, using fallback")
        # Create title screen elements
        try:
            self.title_font = pygame.font.SysFont("comicsansms", 72, bold=True)
        except:
            # Fallback font if Comic Sans is not available
            self.title_font = pygame.font.SysFont(None, 72, bold=True)

        try:
            self.arcade_font = pygame.font.SysFont("impact", 36)
        except:
            self.arcade_font = pygame.font.SysFont(None, 36)

        self.title_text = self.title_font.render("Matcha Cozy", True, self.FANTASY_GREEN)

        # Create blinking effect for "Press Enter to Start"
        self.show_press_enter = True
        self.blink_timer = 0
        self.blink_speed = 500  # milliseconds

        self.score = 0
        self.time_left = 60
        self.game_running = False
        self.is_title_screen = True
        self.start_time = 0
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)

        self.bowl = None
        self.ingredients = []
        self.whisk = None
        self.glass = pygame.Rect(600, 350, 60, 100)
        self.pour_button = None

        self.message = ""
        self.message_time = 0

        # Recipe status
        self.has_almond_milk = False
        self.has_matcha = False
        self.is_stirred = False
        self.is_poured = False
        self.recipe_complete = False

    def setup_game_elements(self):
        # Create bowl
        self.bowl = Bowl(self.SCREEN_WIDTH // 2 - 75, self.SCREEN_HEIGHT // 2 - 40)

        # Create ingredients (removed Sugar)
        self.ingredients = [
            Ingredient("Almond Milk", (240, 240, 230), 200, 400, 120, 50),
            Ingredient("Matcha Powder", self.DARK_GREEN, 400, 400, 120, 50),
        ]

        # Create whisk
        self.whisk = WhiskTool(650, 200)

        # Create pour button (only visible when recipe is stirred)
        self.pour_button = Button(self.SCREEN_WIDTH // 2 - 50, 480, 100, 50, "Pour", self.GREEN)

        # Reset recipe status
        self.has_almond_milk = False
        self.has_matcha = False
        self.is_stirred = False
        self.is_poured = False
        self.recipe_complete = False

    def start_game(self):
        self.game_running = True
        self.is_title_screen = False
        self.score = 0
        self.time_left = 60
        self.start_time = time.time()
        self.setup_game_elements()

    def check_recipe(self):
        if self.has_almond_milk and self.has_matcha and self.is_stirred and self.is_poured and not self.recipe_complete:
            self.score += 1
            self.message = "Matcha Completed and served! +1 point"
            self.message_time = time.time()
            self.recipe_complete = True

    def update_timer(self):
        if self.game_running:
            elapsed = int(time.time() - self.start_time)
            self.time_left = max(60 - elapsed, 0)
            if self.time_left <= 0:
                self.game_running = False
                self.is_title_screen = True

    def handle_ingredient_click(self, pos):
        # Check if any ingredient button is clicked
        clicked_ingredient = None
        for ingredient in self.ingredients:
            if ingredient.is_clicked(pos):
                clicked_ingredient = ingredient
                break

        if clicked_ingredient:
            # Add ingredient directly when clicked (if following correct sequence)
            if clicked_ingredient.name == "Matcha Powder" and not self.has_matcha:
                # First step: Add matcha powder
                self.bowl.add_ingredient(clicked_ingredient)
                self.has_matcha = True
                self.message = "Added Matcha Powder"
                self.message_time = time.time()
                return True
            elif clicked_ingredient.name == "Almond Milk" and self.has_matcha and not self.has_almond_milk:
                # Second step: Add almond milk (only if matcha is already added)
                self.bowl.add_ingredient(clicked_ingredient)
                self.has_almond_milk = True
                self.message = "Added Almond Milk"
                self.message_time = time.time()
                return True
            elif clicked_ingredient.name == "Almond Milk" and not self.has_matcha:
                # If trying to add milk before matcha
                self.message = "Add Matcha Powder first!"
                self.message_time = time.time()
                return True
            elif self.has_almond_milk and self.has_matcha:
                # If both ingredients already added
                self.message = "Now use the whisk to mix!"
                self.message_time = time.time()
                return True
        return False

    def handle_whisk_click(self, pos):
        if self.whisk.is_clicked(pos):
            if self.has_almond_milk and self.has_matcha and not self.is_stirred:
                # Start mixing animation
                self.bowl.stirred = True
                self.is_stirred = True
                self.message = "Matcha stirred! Now pour it into the glass!"
                self.message_time = time.time()
            elif not self.has_matcha:
                self.message = "Add Matcha Powder first!"
                self.message_time = time.time()
            elif not self.has_almond_milk:
                self.message = "Add Almond Milk first!"
                self.message_time = time.time()
            else:
                self.message = "Already stirred! Pour it into the glass!"
                self.message_time = time.time()
            return True
        return False

    def handle_pour_click(self, pos):
        if self.pour_button.is_clicked(pos) and self.is_stirred and not self.is_poured:
            self.is_poured = True
            self.message = "Matcha poured into glass! Recipe complete!"
            self.message_time = time.time()
            self.check_recipe()
            return True
        return False

    def reset_bowl(self):
        if self.recipe_complete:
            self.setup_game_elements()
            self.message = "Starting new matcha..."
            self.message_time = time.time()

    def draw_title_screen(self):
        # Fill with light pink background
        self.screen.fill(self.LIGHT_PINK)

        # Draw title
        title_x = self.SCREEN_WIDTH // 2 - self.title_text.get_width() // 2
        title_y = self.SCREEN_HEIGHT // 3
        self.screen.blit(self.title_text, (title_x, title_y))

        # Draw blinking "Press Enter to Start" text
        if self.show_press_enter:
            press_enter_text = self.arcade_font.render("PRESS ENTER TO START", True, self.BLACK)
            press_enter_x = self.SCREEN_WIDTH // 2 - press_enter_text.get_width() // 2
            press_enter_y = self.SCREEN_HEIGHT * 2 // 3
            self.screen.blit(press_enter_text, (press_enter_x, press_enter_y))

        # Update blink timer
        current_time = pygame.time.get_ticks()
        if current_time - self.blink_timer > self.blink_speed:
            self.show_press_enter = not self.show_press_enter
            self.blink_timer = current_time

    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.is_title_screen:
                        self.start_game()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_title_screen:
                    pos = pygame.mouse.get_pos()

                    if self.game_running:
                        # Handle ingredient clicks
                        if self.handle_ingredient_click(pos):
                            continue

                        # Handle whisk clicks
                        if self.handle_whisk_click(pos):
                            continue

                        # Handle pour button clicks
                        if self.is_stirred and self.handle_pour_click(pos):
                            continue

                        # Handle bowl click for reset
                        if self.bowl and self.bowl.is_clicked(pos) and self.recipe_complete:
                            self.reset_bowl()

            # Update game state
            if self.game_running:
                self.update_timer()

            # Clear the message after 2 seconds
            if self.message and time.time() - self.message_time > 2:
                self.message = ""

            # Draw appropriate screen based on game state
            if self.is_title_screen:
                self.draw_title_screen()
            else:
                # Draw gameplay screen with kawaii background
                self.screen.blit(self.game_background, (0, 0))

                # Draw title
                title_text = self.font.render("MATCHA COZY", True, self.BLACK)
                self.screen.blit(title_text, (self.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

                # Draw game info
                score_text = self.font.render(f"Score: {self.score}", True, self.BLACK)
                time_text = self.font.render(f"Time: {self.time_left}s", True, self.BLACK)
                self.screen.blit(score_text, (50, 80))
                self.screen.blit(time_text, (self.SCREEN_WIDTH - time_text.get_width() - 50, 80))

                if self.game_running:
                    # Draw instructions
                    instruction = self.small_font.render(
                        "Make matcha by adding matcha powder, almond milk, then stirring!",
                        True, self.BLACK)
                    self.screen.blit(instruction, (self.SCREEN_WIDTH // 2 - instruction.get_width() // 2, 120))

                    if self.recipe_complete:
                        instruction2 = self.small_font.render("Click on the bowl to make a new matcha!", True,
                                                              self.GREEN)
                        self.screen.blit(instruction2, (self.SCREEN_WIDTH // 2 - instruction2.get_width() // 2, 150))

                    # Draw game elements
                    if self.bowl:
                        self.bowl.draw(self.screen)

                    for ingredient in self.ingredients:
                        ingredient.draw(self.screen)

                    if self.whisk:
                        self.whisk.draw(self.screen)

                    # Draw glass
                    pygame.draw.rect(self.screen, self.GLASS_COLOR, self.glass)
                    pygame.draw.rect(self.screen, self.BLACK, self.glass, 2)

                    # Draw matcha in glass if poured
                    if self.is_poured:
                        matcha_in_glass = pygame.Rect(self.glass.x + 5, self.glass.y + 5,
                                                      self.glass.width - 10, self.glass.height - 10)
                        pygame.draw.rect(self.screen, self.LIGHT_GREEN, matcha_in_glass)

                    # Draw pour button if stirred
                    if self.is_stirred and not self.is_poured:
                        self.pour_button.draw(self.screen)

                    # Draw message
                    if self.message:
                        msg_text = self.font.render(self.message, True, self.GREEN)
                        self.screen.blit(msg_text, (self.SCREEN_WIDTH // 2 - msg_text.get_width() // 2, 200))
                else:
                    # Draw game over message if time is up
                    if self.time_left <= 0 and self.score > 0:
                        game_over = self.font.render(f"Time's up! You made {self.score} matcha drinks!", True,
                                                     self.BLACK)
                        self.screen.blit(game_over,
                                         (self.SCREEN_WIDTH // 2 - game_over.get_width() // 2,
                                          self.SCREEN_HEIGHT // 2 - 50))

                        # Show "Press Enter to return to title" message
                        return_text = self.small_font.render("Press Enter to return to title screen", True, self.BLACK)
                        self.screen.blit(return_text,
                                         (self.SCREEN_WIDTH // 2 - return_text.get_width() // 2,
                                          self.SCREEN_HEIGHT // 2))

                        # If Enter is pressed after game over, return to title screen
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_RETURN]:
                            self.is_title_screen = True

            pygame.display.flip()