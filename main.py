"""
Advanced Graphics & Algorithms Suite - Main Launcher
A comprehensive collection of educational and advanced programs demonstrating
graphics, machine learning, data visualization, animations, and algorithms
"""

import sys
import os
from typing import Dict, Callable
import importlib.util


class ProgramLauncher:
    """Main launcher for all programs in the Advanced Graphics Suite"""
    
    def __init__(self):
        """Initialize the program launcher"""
        self.programs: Dict[str, Dict] = {
            '1': {
                'name': 'Advanced Fractal Generator',
                'description': 'Generate complex fractals (Mandelbrot, Julia, Sierpinski, Dragon curves)',
                'module': 'fractals',
                'function': 'main',
                'category': 'Graphics',
                'requirements': ['numpy', 'matplotlib', 'tkinter']
            },
            '2': {
                'name': 'Data Visualization Suite',
                'description': 'Interactive charts, graphs, and data analysis tools',
                'module': 'data_viz',
                'function': 'main',
                'category': 'Data Science',
                'requirements': ['numpy', 'matplotlib', 'pandas', 'seaborn', 'tkinter']
            },
            '3': {
                'name': 'ML Pattern Recognition',
                'description': 'Machine learning algorithms for classification and clustering',
                'module': 'ml_patterns',
                'function': 'main',
                'category': 'Machine Learning',
                'requirements': ['numpy', 'matplotlib', 'scikit-learn', 'tkinter']
            },
            '4': {
                'name': 'Animation System',
                'description': 'Interactive animations with physics simulations',
                'module': 'animations',
                'function': 'main',
                'category': 'Graphics',
                'requirements': ['pygame', 'numpy']
            },
            '5': {
                'name': 'Configuration Manager',
                'description': 'Manage application settings and user preferences',
                'module': 'config_manager',
                'function': 'main',
                'category': 'Utilities',
                'requirements': ['tkinter']
            },
            '6': {
                'name': 'Geometric Pattern Generator',
                'description': 'Creates beautiful circular patterns using turtle graphics',
                'module': 'Turtle',
                'function': 'main',
                'category': 'Graphics',
                'requirements': ['turtle']
            },
            '7': {
                'name': 'Snowflake Pattern Generator',
                'description': 'Creates snowflake patterns with customizable parameters',
                'module': 'snow',
                'function': 'main',
                'category': 'Graphics',
                'requirements': ['turtle', 'random']
            },
            '8': {
                'name': 'Text Evolution Simulator',
                'description': 'Demonstrates evolutionary algorithms through text generation',
                'module': 'text',
                'function': 'main',
                'category': 'Algorithms',
                'requirements': ['random', 'string', 'time']
            },
            '9': {
                'name': 'Multiplication Table Generator',
                'description': 'Generates customizable multiplication tables',
                'module': 'mathstables',
                'function': 'main',
                'category': 'Education',
                'requirements': []
            },
            '10': {
                'name': 'Run All Programs',
                'description': 'Execute all programs in sequence',
                'module': None,
                'function': 'run_all',
                'category': 'Utilities',
                'requirements': []
            }
        }
        
    def display_menu(self):
        """Display the main menu with categories"""
        print("\n" + "=" * 70)
        print("    ADVANCED GRAPHICS & ALGORITHMS SUITE")
        print("=" * 70)
        print("Choose a program to run:")
        print()
        
        # Group programs by category
        categories = {}
        for key, program in self.programs.items():
            if key == '10':  # Skip "Run All" for now
                continue
            category = program['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((key, program))
        
        # Display programs by category
        for category, programs in categories.items():
            print(f"\n{category.upper()}:")
            print("-" * 40)
            for key, program in programs:
                print(f"{key}. {program['name']}")
                print(f"   {program['description']}")
                print()
        
        print("=" * 70)
        print("10. Run All Programs (Sequential)")
        print("0. Exit")
        print("=" * 70)
        
    def run_program(self, choice: str):
        """
        Run the selected program with dependency checking
        
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
        
        if choice == '10':
            # Run all programs
            self.run_all_programs()
        else:
            # Check dependencies first
            if not self.check_dependencies(program['requirements']):
                print(f"Cannot run {program['name']} due to missing dependencies.")
                return True
            
            # Run individual program
            self.run_single_program(program)
            
        return True
        
    def check_dependencies(self, requirements: list) -> bool:
        """
        Check if required modules are available
        
        Args:
            requirements (list): List of required module names
            
        Returns:
            bool: True if all dependencies are available
        """
        missing_modules = []
        
        for module in requirements:
            try:
                if module == 'tkinter':
                    import tkinter
                elif module == 'turtle':
                    import turtle
                else:
                    importlib.import_module(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"Missing required modules: {', '.join(missing_modules)}")
            print("Please install missing dependencies using:")
            print(f"pip install {' '.join(missing_modules)}")
            return False
        
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
        print("Welcome to the Advanced Graphics & Algorithms Suite!")
        print("This collection contains various educational and advanced programs.")
        print("Including fractals, machine learning, data visualization, animations, and more.")
        print()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (0-10): ").strip()
                
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
    print("Checking system dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Warning: Python 3.8 or higher is recommended for best compatibility.")
    
    # Check for optional advanced modules
    advanced_modules = {
        'numpy': 'Required for fractals, ML, and animations',
        'matplotlib': 'Required for data visualization and fractals',
        'pandas': 'Required for data analysis',
        'seaborn': 'Required for advanced data visualization',
        'scikit-learn': 'Required for machine learning features',
        'pygame': 'Required for animation system',
        'PIL': 'Required for image processing',
        'scipy': 'Required for advanced algorithms'
    }
    
    missing_advanced = []
    available_advanced = []
    
    for module, description in advanced_modules.items():
        try:
            if module == 'PIL':
                import PIL
            else:
                importlib.import_module(module)
            available_advanced.append(f"✓ {module} - {description}")
        except ImportError:
            missing_advanced.append(f"✗ {module} - {description}")
    
    print("\nAdvanced Features Status:")
    print("=" * 50)
    
    if available_advanced:
        print("Available advanced features:")
        for feature in available_advanced:
            print(f"  {feature}")
    
    if missing_advanced:
        print("\nMissing advanced features:")
        for feature in missing_advanced:
            print(f"  {feature}")
        
        print(f"\nTo install missing features, run:")
        print("pip install -r requirements.txt")
    
    # Check basic modules
    basic_modules = ['turtle', 'tkinter', 'random', 'string', 'time', 'sys']
    missing_basic = []
    
    for module in basic_modules:
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'turtle':
                import turtle
            else:
                importlib.import_module(module)
        except ImportError:
            missing_basic.append(module)
    
    if missing_basic:
        print(f"\nWarning: Missing basic modules: {', '.join(missing_basic)}")
        print("Some basic programs may not work correctly.")
    else:
        print("\n✓ All basic modules are available")
    
    print("=" * 50)
    return len(missing_basic) == 0


def main():
    """Main function"""
    print("Checking dependencies...")
    check_dependencies()
    
    print("\nChoose launcher type:")
    print("1. GUI Launcher (Recommended)")
    print("2. CLI Launcher")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        try:
            import gui_launcher
            gui_launcher.main()
        except ImportError:
            print("GUI launcher not available. Falling back to CLI launcher...")
            launcher = ProgramLauncher()
            launcher.run()
        except Exception as e:
            print(f"Error starting GUI launcher: {e}")
            print("Falling back to CLI launcher...")
            launcher = ProgramLauncher()
            launcher.run()
    else:
        launcher = ProgramLauncher()
        launcher.run()


if __name__ == "__main__":
    main()
