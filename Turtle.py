"""
Geometric Pattern Generator using Turtle Graphics
Creates beautiful circular patterns with customizable parameters
"""

import turtle
import sys


def create_geometric_pattern(iterations=100, patterns=5, angle_multiplier=9, turn_angle=180):
    """
    Creates a geometric pattern using turtle graphics
    
    Args:
        iterations (int): Number of iterations for each pattern
        patterns (int): Number of pattern cycles
        angle_multiplier (int): Multiplier for circle angle calculation
        turn_angle (int): Angle to turn after each circle
    """
    try:
        screen = turtle.Screen()
        screen.title("Geometric Pattern Generator")
        screen.bgcolor("black")
        
        t = turtle.Turtle()
        t.speed(0)  # Fastest speed
        t.color("cyan")
        t.width(2)
        
        for pattern in range(patterns):
            angle = angle_multiplier * pattern
            for i in range(iterations):
                # Create four circles with turns
                for _ in range(4):
                    t.circle(i, angle)
                    t.right(turn_angle)
        
        # Hide turtle and display completion message
        t.hideturtle()
        
        # Add text to the screen
        t.penup()
        t.goto(0, -screen.window_height() // 2 + 50)
        t.color("white")
        t.write("Pattern Complete! Click to close.", align="center", font=("Arial", 16, "bold"))
        
        # Wait for click to close
        screen.exitonclick()
        
    except turtle.Terminator:
        print("Graphics window was closed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            turtle.bye()
        except:
            pass


def main():
    """Main function to run the geometric pattern generator"""
    print("Geometric Pattern Generator")
    print("=" * 30)
    
    try:
        # Get user input with defaults
        iterations = input("Enter number of iterations (default 100): ").strip()
        iterations = int(iterations) if iterations else 100
        
        patterns = input("Enter number of patterns (default 5): ").strip()
        patterns = int(patterns) if patterns else 5
        
        angle_multiplier = input("Enter angle multiplier (default 9): ").strip()
        angle_multiplier = int(angle_multiplier) if angle_multiplier else 9
        
        turn_angle = input("Enter turn angle (default 180): ").strip()
        turn_angle = int(turn_angle) if turn_angle else 180
        
        # Validate inputs
        if iterations <= 0 or patterns <= 0:
            raise ValueError("Iterations and patterns must be positive integers")
        
        create_geometric_pattern(iterations, patterns, angle_multiplier, turn_angle)
        
    except ValueError as e:
        print(f"Invalid input: {e}")
        print("Using default values...")
        create_geometric_pattern()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()