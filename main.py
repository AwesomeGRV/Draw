"""
Main Launcher for Draw Programs
A collection of educational Python programs demonstrating various concepts
"""

import sys
import os
from typing import Dict, Callable


class ProgramLauncher:
    """Main launcher for all programs in the draw collection"""
    
    def __init__(self):
        """Initialize the program launcher"""
        self.programs: Dict[str, Dict] = {
            '1': {
                'name': 'Geometric Pattern Generator',
                'description': 'Creates beautiful circular patterns using turtle graphics',
                'module': 'Turtle',
                'function': 'main'
            },
            '2': {
                'name': 'Multiplication Table Generator',
                'description': 'Generates customizable multiplication tables',
                'module': 'mathstables',
                'function': 'main'
            },
            '3': {
                'name': 'Snowflake Pattern Generator',
                'description': 'Creates snowflake patterns with customizable parameters',
                'module': 'snow',
                'function': 'main'
            },
            '4': {
                'name': 'Text Evolution Simulator',
                'description': 'Demonstrates evolutionary algorithms through text generation',
                'module': 'text',
                'function': 'main'
            },
            '5': {
                'name': 'Run All Programs',
                'description': 'Execute all programs in sequence',
                'module': None,
                'function': 'run_all'
            }
        }
        
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 60)
        print("           DRAW PROGRAMS COLLECTION")
        print("=" * 60)
        print("Choose a program to run:")
        print()
        
        for key, program in self.programs.items():
            print(f"{key}. {program['name']}")
            print(f"   {program['description']}")
            print()
        
        print("0. Exit")
        print("=" * 60)
        
    def run_program(self, choice: str):
        """
        Run the selected program
        
        Args:
            choice (str): User's menu choice
        """
        if choice == '0':
            print("Goodbye!")
            return False
            
        if choice not in self.programs:
            print("Invalid choice. Please try again.")
            return True
            
        program = self.programs[choice]
        
        if choice == '5':
            # Run all programs
            self.run_all_programs()
        else:
            # Run individual program
            self.run_single_program(program)
            
        return True
        
    def run_single_program(self, program: Dict):
        """
        Run a single program
        
        Args:
            program (Dict): Program information dictionary
        """
        print(f"\nStarting {program['name']}...")
        print("-" * 40)
        
        try:
            # Import the module
            module = __import__(program['module'])
            
            # Get the main function
            main_function = getattr(module, program['function'])
            
            # Run the program
            main_function()
            
        except ImportError as e:
            print(f"Error: Could not import module '{program['module']}': {e}")
        except AttributeError as e:
            print(f"Error: Function '{program['function']}' not found in module: {e}")
        except KeyboardInterrupt:
            print(f"\n{program['name']} interrupted by user.")
        except Exception as e:
            print(f"Error running {program['name']}: {e}")
            
        print("\nPress Enter to continue...")
        input()
        
    def run_all_programs(self):
        """Run all programs in sequence"""
        print("\nRunning all programs...")
        print("=" * 40)
        
        # Skip the 'Run All Programs' option
        programs_to_run = [p for k, p in self.programs.items() if k != '5']
        
        for i, program in enumerate(programs_to_run, 1):
            print(f"\nProgram {i}/{len(programs_to_run)}: {program['name']}")
            print("-" * 40)
            
            try:
                module = __import__(program['module'])
                main_function = getattr(module, program['function'])
                main_function()
                
            except KeyboardInterrupt:
                print(f"\n{program['name']} interrupted by user.")
                break
            except Exception as e:
                print(f"Error running {program['name']}: {e}")
                
            if i < len(programs_to_run):
                print(f"\nCompleted {program['name']}. Press Enter to continue to next program...")
                input()
            else:
                print(f"\nCompleted all programs!")
                
        print("\nPress Enter to return to menu...")
        input()
        
    def run(self):
        """Run the main launcher loop"""
        print("Welcome to the Draw Programs Collection!")
        print("This collection contains various educational Python programs.")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (0-5): ").strip()
                
                if not self.run_program(choice):
                    break
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Press Enter to continue...")
                input()


def check_dependencies():
    """Check if all required modules are available"""
    required_modules = ['turtle', 'random', 'string', 'time', 'sys']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    if missing_modules:
        print("Warning: The following required modules are missing:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nSome programs may not work correctly.")
        print("Press Enter to continue anyway...")
        input()
        
    return len(missing_modules) == 0


def main():
    """Main function"""
    print("Checking dependencies...")
    check_dependencies()
    
    launcher = ProgramLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
