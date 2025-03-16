import time
import random
import os


class MatchaCLI:
    def __init__(self):
        # Game state
        self.player_name = ""
        self.score = 0
        self.time_left = 60
        self.game_over = False

        # Matcha preparation state
        self.has_matcha = False
        self.has_hot_water = False
        self.has_almond_milk = False
        self.is_mixed_with_water = False
        self.is_fully_mixed = False
        self.is_poured = False
        self.recipe_complete = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_game(self):
        self.clear_screen()
        print("╔════════════════════════════════════════╗")
        print("║        MATCHA GAME - CLI VERSION       ║")
        print("╚════════════════════════════════════════╝")
        self.get_player_name()
        self.game_loop()

    def get_player_name(self):
        print("\n📝 Please tell us your name to begin:")
        self.player_name = input("➤ ")
        print("\n┌─────────────────────────────────────────┐")
        print(f"│ 👋 Welcome, {self.player_name}!".ljust(42) + "│")
        print("│ 🍵 Let's make some delicious matcha!".ljust(42) + "│")
        print("│ ⏱️  You have 60 seconds to make as many".ljust(42) + "│")
        print("│    matcha drinks as possible.".ljust(42) + "│")
        print("└─────────────────────────────────────────┘")
        input("\nPress ENTER to start the game... ")

    def display_options(self):
        print("\n🎮 ACTIONS AVAILABLE:")
        print("┌────┬─────────────────────────┐")
        print("│ 1  │ Add matcha powder       │")
        print("│ 2  │ Add hot water           │")
        print("│ 3  │ Whisk the mixture       │")
        print("│ 4  │ Add almond milk         │")
        print("│ 5  │ Pour into glass         │")
        print("│ 6  │ Quit game               │")
        print("└────┴─────────────────────────┘")

    def game_loop(self):
        start_time = time.time()
        self.matcha_count = 0

        while not self.game_over:
            self.clear_screen()

            # Update time
            elapsed = time.time() - start_time
            self.time_left = max(0, 60 - int(elapsed))

            if self.time_left <= 0:
                self.game_over = True
                break

            # Display current state
            print("╔═══════════════════════════════════════════════╗")
            print(f"║ ⏱️  TIME LEFT: {self.time_left}s".ljust(41) + "║")
            print(f"║ 🍵 MATCHA COMPLETED: {self.matcha_count}".ljust(41) + "║")
            print(f"║ 🏆 CURRENT SCORE: {self.score}".ljust(41) + "║")
            print("╚═══════════════════════════════════════════════╝")
            self.display_current_state()

            # Display recipe guide
            self.display_recipe_guide()

            self.display_options()

            # Get player action
            print("\n❓ What would you like to do next?")
            try:
                choice = int(input("➤ Enter your choice (1-6): "))
                self.process_action(choice)

                # Add a small delay to show messages instead of prompting for ENTER
                if choice != 6:  # Don't delay if quitting
                    time.sleep(1.5)

            except ValueError:
                print("⚠️  Please enter a number between 1 and 6.")
                time.sleep(1)

            # Check if recipe is complete
            if self.recipe_complete:
                self.clear_screen()
                print("\n🎉 MATCHA COMPLETED SUCCESSFULLY! +10 POINTS! 🎉")
                print("╔══════════════════════════════════════════╗")
                print(f"║   Your matcha latte is ready to serve!   ║")
                print("╚══════════════════════════════════════════╝")
                self.score += 10
                self.matcha_count += 1
                self.reset_recipe()
                time.sleep(2)  # Show completion message briefly

        # Game over
        self.show_results()

    def display_current_state(self):
        print("\n📊 CURRENT PROGRESS:")
        print("┌────────────────────────┬─────────┐")
        print(f"│ Matcha powder          │ {'✅' if self.has_matcha else '❌'} │")
        print(f"│ Hot water              │ {'✅' if self.has_hot_water else '❌'} │")
        print(f"│ Whisked with water     │ {'✅' if self.is_mixed_with_water else '❌'} │")
        print(f"│ Almond milk            │ {'✅' if self.has_almond_milk else '❌'} │")
        print(f"│ Fully mixed            │ {'✅' if self.is_fully_mixed else '❌'} │")
        print(f"│ Poured into glass      │ {'✅' if self.is_poured else '❌'} │")
        print("└────────────────────────┴─────────┘")

    def display_recipe_guide(self):
        next_step = ""
        if not self.has_matcha:
            next_step = "First, you need to add matcha powder (option 1)"
        elif not self.has_hot_water:
            next_step = "Now add hot water (option 2)"
        elif not self.is_mixed_with_water:
            next_step = "Whisk the matcha with water (option 3)"
        elif not self.has_almond_milk:
            next_step = "Add almond milk (option 4)"
        elif not self.is_fully_mixed:
            next_step = "Whisk everything together (option 3)"
        elif not self.is_poured:
            next_step = "Pour into a glass (option 5)"

        if next_step:
            print("\n💡 NEXT STEP: " + next_step)

    def process_action(self, choice):
        if choice == 1:  # Add matcha powder
            if not self.has_matcha:
                print("🍵 Adding matcha powder to the bowl...")
                time.sleep(0.8)
                self.has_matcha = True
                print("✅ Matcha powder added successfully!")
            else:
                print("⚠️  You've already added matcha powder!")

        elif choice == 2:  # Add hot water
            if not self.has_hot_water:
                if self.has_matcha:
                    print("🌊 Adding hot water...")
                    time.sleep(0.8)
                    self.has_hot_water = True
                    print("✅ Hot water added successfully!")
                else:
                    print("❌ You need to add matcha powder first!")
            else:
                print("⚠️  You've already added hot water!")

        elif choice == 3:  # Whisk the mixture
            if self.has_matcha and self.has_hot_water:
                if not self.is_mixed_with_water:
                    print("🔄 Whisking the matcha and water...")
                    time.sleep(1)
                    self.is_mixed_with_water = True
                    print("✅ Basic mixture complete!")
                elif self.has_almond_milk and not self.is_fully_mixed:
                    print("🔄 Whisking everything together...")
                    time.sleep(1)
                    self.is_fully_mixed = True
                    print("✅ Mixture fully whisked and ready!")
                else:
                    print("⚠️  You've already whisked the current ingredients!")
            else:
                print("❌ You need both matcha powder and hot water to whisk!")

        elif choice == 4:  # Add almond milk
            if not self.has_almond_milk:
                if self.is_mixed_with_water:
                    print("🥛 Adding almond milk...")
                    time.sleep(0.8)
                    self.has_almond_milk = True
                    print("✅ Almond milk added successfully!")
                else:
                    print("❌ You need to mix the matcha and water first!")
            else:
                print("⚠️  You've already added almond milk!")

        elif choice == 5:  # Pour into glass
            if self.is_fully_mixed:
                print("🫖 Pouring the matcha into a glass...")
                time.sleep(1)
                self.is_poured = True
                self.recipe_complete = True
                print("✅ Matcha latte prepared successfully!")
            else:
                print("❌ You need to fully mix all ingredients first!")

        elif choice == 6:  # Quit game
            self.game_over = True
            print("👋 Game ended early.")
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")

    def reset_recipe(self):
        self.has_matcha = False
        self.has_hot_water = False
        self.has_almond_milk = False
        self.is_mixed_with_water = False
        self.is_fully_mixed = False
        self.is_poured = False
        self.recipe_complete = False

    def show_results(self):
        self.clear_screen()
        print("\n╔═════════════════════════════════════╗")
        print("║            GAME OVER                ║")
        print("╚═════════════════════════════════════╝")
        print(f"\n👤 Player: {self.player_name}")
        print(f"🏆 Final score: {self.score}")
        print(f"🍵 Matcha drinks completed: {self.matcha_count}")
        print("\n🌟 Thanks for playing! 🌟")


if __name__ == "__main__":
    game = MatchaCLI()
    game.start_game()