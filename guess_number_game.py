"""
Guess the Number Game
Interactive number guessing game with difficulty levels and statistics
"""

import random
import time
from typing import Tuple, Dict
import json
import os


class GuessNumberGame:
    """Interactive number guessing game with multiple features"""
    
    def __init__(self):
        self.stats_file = "guess_number_stats.json"
        self.load_statistics()
        
    def load_statistics(self):
        """Load game statistics from file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            else:
                self.stats = {
                    'games_played': 0,
                    'total_guesses': 0,
                    'best_score': float('inf'),
                    'average_guesses': 0,
                    'difficulty_stats': {
                        'easy': {'games': 0, 'best_score': float('inf')},
                        'medium': {'games': 0, 'best_score': float('inf')},
                        'hard': {'games': 0, 'best_score': float('inf')},
                        'expert': {'games': 0, 'best_score': float('inf')}
                    }
                }
        except Exception:
            self.stats = {
                'games_played': 0,
                'total_guesses': 0,
                'best_score': float('inf'),
                'average_guesses': 0,
                'difficulty_stats': {
                    'easy': {'games': 0, 'best_score': float('inf')},
                    'medium': {'games': 0, 'best_score': float('inf')},
                    'hard': {'games': 0, 'best_score': float('inf')},
                    'expert': {'games': 0, 'best_score': float('inf')}
                }
            }
    
    def save_statistics(self):
        """Save game statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Could not save statistics: {e}")
    
    def get_difficulty_settings(self, difficulty: str) -> Tuple[int, str]:
        """Get range and hints for difficulty level"""
        settings = {
            'easy': (1, 50, "Easy mode: Number between 1 and 50"),
            'medium': (1, 100, "Medium mode: Number between 1 and 100"),
            'hard': (1, 500, "Hard mode: Number between 1 and 500"),
            'expert': (1, 1000, "Expert mode: Number between 1 and 1000")
        }
        return settings.get(difficulty, (1, 100, "Default mode: Number between 1 and 100"))
    
    def get_hint(self, secret_number: int, guess: int, difficulty: str) -> str:
        """Generate hint based on guess"""
        difference = abs(secret_number - guess)
        
        if difficulty == 'easy':
            if difference == 0:
                return "🎉 Perfect! You got it!"
            elif difference <= 5:
                return "🔥 Very hot! You're extremely close!"
            elif difference <= 10:
                return "♨️ Hot! You're very close!"
            elif difference <= 20:
                return "🌡️ Warm! Getting warmer!"
            else:
                return "❄️ Cold! Try a different range!"
        
        elif difficulty == 'medium':
            if difference == 0:
                return "🎉 Perfect! You got it!"
            elif difference <= 10:
                return "🔥 Very hot! You're extremely close!"
            elif difference <= 25:
                return "♨️ Hot! You're very close!"
            elif difference <= 50:
                return "🌡️ Warm! Getting warmer!"
            else:
                return "❄️ Cold! Try a different range!"
        
        elif difficulty == 'hard':
            if difference == 0:
                return "🎉 Perfect! You got it!"
            elif difference <= 25:
                return "🔥 Very hot! You're extremely close!"
            elif difference <= 75:
                return "♨️ Hot! You're very close!"
            elif difference <= 150:
                return "🌡️ Warm! Getting warmer!"
            else:
                return "❄️ Cold! Try a different range!"
        
        else:  # expert
            if difference == 0:
                return "🎉 Perfect! You got it!"
            elif difference <= 50:
                return "🔥 Very hot! You're extremely close!"
            elif difference <= 150:
                return "♨️ Hot! You're very close!"
            elif difference <= 300:
                return "🌡️ Warm! Getting warmer!"
            else:
                return "❄️ Cold! Try a different range!"
    
    def play_game(self, difficulty: str = 'medium') -> Dict:
        """Play a single game"""
        min_num, max_num, description = self.get_difficulty_settings(difficulty)
        secret_number = random.randint(min_num, max_num)
        
        print(f"\n🎮 {description}")
        print("💡 Type 'quit' to exit the game")
        print("💡 Type 'hint' for a special hint")
        print("=" * 50)
        
        guesses = 0
        start_time = time.time()
        guess_history = []
        
        while True:
            try:
                user_input = input(f"\n🎯 Enter your guess ({min_num}-{max_num}): ").strip().lower()
                
                if user_input == 'quit':
                    print(f"\n👋 Game quit! The number was {secret_number}")
                    return {'won': False, 'guesses': guesses, 'time': time.time() - start_time}
                
                if user_input == 'hint':
                    if guesses >= 3:
                        if secret_number % 2 == 0:
                            print("💡 Hint: The number is EVEN")
                        else:
                            print("💡 Hint: The number is ODD")
                        
                        if secret_number % 5 == 0:
                            print("💡 Hint: The number is divisible by 5")
                        elif secret_number % 3 == 0:
                            print("💡 Hint: The number is divisible by 3")
                    else:
                        print("💡 You need to make at least 3 guesses before getting a hint!")
                    continue
                
                guess = int(user_input)
                
                if guess < min_num or guess > max_num:
                    print(f"❌ Please enter a number between {min_num} and {max_num}")
                    continue
                
                guesses += 1
                guess_history.append(guess)
                
                if guess == secret_number:
                    end_time = time.time()
                    time_taken = end_time - start_time
                    
                    print(f"\n🎉 CONGRATULATIONS! You guessed it!")
                    print(f"🎯 The number was: {secret_number}")
                    print(f"📊 Guesses taken: {guesses}")
                    print(f"⏱️ Time taken: {time_taken:.1f} seconds")
                    print(f"📝 Your guesses: {', '.join(map(str, guess_history))}")
                    
                    return {'won': True, 'guesses': guesses, 'time': time_taken}
                
                # Provide feedback
                if guess < secret_number:
                    print(f"📈 Too LOW! Try a higher number")
                else:
                    print(f"📉 Too HIGH! Try a lower number")
                
                # Give temperature hint
                hint = self.get_hint(secret_number, guess, difficulty)
                print(f"💡 {hint}")
                
                # Show progress
                progress = f"📈 Progress: {guesses} guesses"
                if guesses > 1:
                    prev_guess = guess_history[-2]
                    if abs(secret_number - guess) < abs(secret_number - prev_guess):
                        progress += " 🔥 Getting warmer!"
                    else:
                        progress += " ❄️ Getting colder!"
                print(progress)
                
            except ValueError:
                print("❌ Please enter a valid number!")
            except KeyboardInterrupt:
                print(f"\n👋 Game interrupted! The number was {secret_number}")
                return {'won': False, 'guesses': guesses, 'time': time.time() - start_time}
    
    def update_statistics(self, game_result: Dict, difficulty: str):
        """Update game statistics"""
        self.stats['games_played'] += 1
        self.stats['total_guesses'] += game_result['guesses']
        
        if game_result['won']:
            if game_result['guesses'] < self.stats['best_score']:
                self.stats['best_score'] = game_result['guesses']
        
        self.stats['average_guesses'] = self.stats['total_guesses'] / self.stats['games_played']
        
        # Update difficulty-specific stats
        diff_stats = self.stats['difficulty_stats'][difficulty]
        diff_stats['games'] += 1
        if game_result['won'] and game_result['guesses'] < diff_stats['best_score']:
            diff_stats['best_score'] = game_result['guesses']
        
        self.save_statistics()
    
    def show_statistics(self):
        """Display game statistics"""
        print("\n📊 GAME STATISTICS")
        print("=" * 50)
        print(f"🎮 Total Games Played: {self.stats['games_played']}")
        print(f"🔢 Total Guesses Made: {self.stats['total_guesses']}")
        print(f"📈 Average Guesses per Game: {self.stats['average_guesses']:.1f}")
        
        if self.stats['best_score'] != float('inf'):
            print(f"🏆 Best Score (fewest guesses): {self.stats['best_score']}")
        else:
            print("🏆 Best Score: No games won yet")
        
        print("\n📈 Statistics by Difficulty:")
        print("-" * 30)
        
        for difficulty, stats in self.stats['difficulty_stats'].items():
            print(f"\n{difficulty.upper()}:")
            print(f"  Games played: {stats['games']}")
            if stats['best_score'] != float('inf'):
                print(f"  Best score: {stats['best_score']} guesses")
            else:
                print(f"  Best score: No wins yet")
    
    def show_menu(self):
        """Display main menu"""
        print("\n🎮 GUESS THE NUMBER GAME")
        print("=" * 50)
        print("1. 🎯 Play Game")
        print("2. 📊 View Statistics")
        print("3. 🎚️ Change Difficulty")
        print("4. 📖 How to Play")
        print("5. 🚪 Exit")
        print("=" * 50)
    
    def show_instructions(self):
        """Show game instructions"""
        print("\n📖 HOW TO PLAY")
        print("=" * 50)
        print("🎯 The computer will think of a random number")
        print("🔢 You need to guess what that number is")
        print("💡 The game will tell you if your guess is too high or too low")
        print("🌡️ Temperature hints help you know how close you are")
        print("🏆 Try to guess the number in as few attempts as possible!")
        print("\n🎚️ DIFFICULTY LEVELS:")
        print("• EASY: Numbers 1-50 (more detailed hints)")
        print("• MEDIUM: Numbers 1-100 (moderate hints)")
        print("• HARD: Numbers 1-500 (basic hints)")
        print("• EXPERT: Numbers 1-1000 (minimal hints)")
        print("\n💡 SPECIAL COMMANDS:")
        print("• Type 'hint' after 3 guesses for a mathematical hint")
        print("• Type 'quit' to exit the current game")
        print("=" * 50)
    
    def run(self):
        """Main game loop"""
        current_difficulty = 'medium'
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    # Play game
                    result = self.play_game(current_difficulty)
                    self.update_statistics(result, current_difficulty)
                    
                    if result['won']:
                        print(f"\n🎉 Great job! You completed the {current_difficulty} level!")
                    
                    # Ask to play again
                    play_again = input("\n🎮 Play again? (y/n): ").strip().lower()
                    if play_again != 'y':
                        print("\n👋 Thanks for playing!")
                        break
                
                elif choice == '2':
                    # Show statistics
                    self.show_statistics()
                    input("\nPress Enter to continue...")
                
                elif choice == '3':
                    # Change difficulty
                    print("\n🎚️ SELECT DIFFICULTY")
                    print("1. 🟢 EASY (1-50)")
                    print("2. 🟡 MEDIUM (1-100)")
                    print("3. 🟠 HARD (1-500)")
                    print("4. 🔴 EXPERT (1-1000)")
                    
                    diff_choice = input("\nSelect difficulty (1-4): ").strip()
                    difficulties = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'expert'}
                    
                    if diff_choice in difficulties:
                        current_difficulty = difficulties[diff_choice]
                        print(f"\n✅ Difficulty set to {current_difficulty.upper()}")
                    else:
                        print("\n❌ Invalid choice! Using MEDIUM difficulty")
                        current_difficulty = 'medium'
                
                elif choice == '4':
                    # Show instructions
                    self.show_instructions()
                    input("\nPress Enter to continue...")
                
                elif choice == '5':
                    # Exit
                    print("\n👋 Thanks for playing Guess the Number!")
                    print(f"📊 Final Stats: {self.stats['games_played']} games played")
                    break
                
                else:
                    print("\n❌ Invalid choice! Please enter 1-5")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main():
    """Main function to run the guess the number game"""
    print("🎮 GUESS THE NUMBER GAME")
    print("=" * 30)
    print("Starting interactive number guessing game...")
    
    game = GuessNumberGame()
    game.run()


if __name__ == "__main__":
    main()
