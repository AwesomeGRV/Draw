"""
Snowflake Pattern Generator using Turtle Graphics
Creates beautiful snowflake patterns with customizable parameters
"""

import turtle
import random
import sys


class SnowflakeGenerator:
    """Class to generate snowflake patterns using turtle graphics"""
    
    def __init__(self, colors=None, bg_color="grey", branch_length=30, branches=8):
        """
        Initialize the snowflake generator
        
        Args:
            colors (list): List of colors for the snowflake
            bg_color (str): Background color
            branch_length (int): Length of each branch segment
            branches (int): Number of main branches
        """
        self.colors = colors or ["cyan", "purple", "white", "blue", "lightblue"]
        self.bg_color = bg_color
        self.branch_length = branch_length
        self.branches = branches
        self.screen = None
        self.turtle = None
        
    def setup_screen(self):
        """Setup the turtle screen"""
        self.screen = turtle.Screen()
        self.screen.title("Snowflake Pattern Generator")
        self.screen.bgcolor(self.bg_color)
        self.screen.setup(width=800, height=800)
        
    def setup_turtle(self):
        """Setup the turtle for drawing"""
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)  # Fastest speed
        self.turtle.width(2)
        
        # Random initial color
        self.turtle.color(random.choice(self.colors))
        
        # Position turtle
        self.turtle.penup()
        self.turtle.forward(90)
        self.turtle.left(45)
        self.turtle.pendown()
        
    def draw_branch(self):
        """Draw a single branch of the snowflake"""
        for _ in range(3):
            # Change color randomly for variety
            self.turtle.color(random.choice(self.colors))
            
            for _ in range(3):
                self.turtle.forward(self.branch_length)
                self.turtle.backward(self.branch_length)
                self.turtle.right(45)
            
            self.turtle.left(90)
            self.turtle.backward(self.branch_length)
            self.turtle.left(45)
        
        self.turtle.right(90)
        self.turtle.forward(self.branch_length * 3)
        
    def draw_snowflake(self):
        """Draw the complete snowflake pattern"""
        for i in range(self.branches):
            self.draw_branch()
            self.turtle.left(360 / self.branches)
            
    def add_completion_text(self):
        """Add completion text to the screen"""
        self.turtle.penup()
        self.turtle.goto(0, -self.screen.window_height() // 2 + 50)
        self.turtle.color("white")
        self.turtle.write("Snowflake Complete! Click to close.", 
                         align="center", font=("Arial", 16, "bold"))
        self.turtle.hideturtle()
        
    def generate(self):
        """Generate the snowflake pattern"""
        try:
            self.setup_screen()
            self.setup_turtle()
            self.draw_snowflake()
            self.add_completion_text()
            
            # Wait for click to close
            self.screen.exitonclick()
            
        except turtle.Terminator:
            print("Graphics window was closed.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up turtle resources"""
        try:
            if self.screen:
                turtle.bye()
        except:
            pass


def get_user_preferences():
    """Get user preferences for snowflake generation"""
    print("Snowflake Pattern Generator")
    print("=" * 30)
    
    preferences = {}
    
    try:
        branches = input("Enter number of branches (default 8): ").strip()
        preferences['branches'] = int(branches) if branches else 8
        
        length = input("Enter branch length (default 30): ").strip()
        preferences['branch_length'] = int(length) if length else 30
        
        bg_color = input("Enter background color (default grey): ").strip()
        preferences['bg_color'] = bg_color if bg_color else "grey"
        
        custom_colors = input("Use custom colors? (y/n, default n): ").strip().lower()
        if custom_colors in ['y', 'yes']:
            colors_input = input("Enter colors separated by commas (e.g., red,blue,green): ").strip()
            preferences['colors'] = [color.strip() for color in colors_input.split(',') if color.strip()]
        else:
            preferences['colors'] = None
            
        return preferences
        
    except ValueError:
        print("Invalid input. Using defaults.")
        return {}


def main():
    """Main function to run the snowflake generator"""
    try:
        preferences = get_user_preferences()
        
        # Validate inputs
        if preferences.get('branches', 8) <= 0:
            raise ValueError("Number of branches must be positive")
        if preferences.get('branch_length', 30) <= 0:
            raise ValueError("Branch length must be positive")
            
        # Create and generate snowflake
        generator = SnowflakeGenerator(**preferences)
        generator.generate()
        
    except ValueError as e:
        print(f"Invalid input: {e}")
        print("Using default values...")
        generator = SnowflakeGenerator()
        generator.generate()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()