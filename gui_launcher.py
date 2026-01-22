"""
Advanced Graphics & Algorithms Suite - GUI Launcher
A modern graphical interface for launching all programs with buttons
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import importlib.util
from typing import Dict, List


class ProgramLauncherGUI:
    """GUI launcher for all programs in the suite"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Graphics & Algorithms Suite")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.setup_styles()
        
        # Program definitions
        self.programs = {
            'fractals': {
                'name': 'Advanced Fractal Generator',
                'description': 'Generate complex fractals (Mandelbrot, Julia, Sierpinski, Dragon curves)',
                'category': 'Graphics',
                'file': 'fractals.py',
                'icon': '🌀',
                'requirements': ['numpy', 'matplotlib', 'tkinter']
            },
            'data_viz': {
                'name': 'Data Visualization Suite',
                'description': 'Interactive charts, graphs, and data analysis tools',
                'category': 'Data Science',
                'file': 'data_viz.py',
                'icon': '📊',
                'requirements': ['numpy', 'matplotlib', 'pandas', 'seaborn', 'tkinter']
            },
            'ml_patterns': {
                'name': 'ML Pattern Recognition',
                'description': 'Machine learning algorithms for classification and clustering',
                'category': 'Machine Learning',
                'file': 'ml_patterns.py',
                'icon': '🤖',
                'requirements': ['numpy', 'matplotlib', 'scikit-learn', 'tkinter']
            },
            'animations': {
                'name': 'Animation System',
                'description': 'Interactive animations with physics simulations',
                'category': 'Graphics',
                'file': 'animations.py',
                'icon': '🎮',
                'requirements': ['pygame', 'numpy']
            },
            'config_manager': {
                'name': 'Configuration Manager',
                'description': 'Manage application settings and user preferences',
                'category': 'Utilities',
                'file': 'config_manager.py',
                'icon': '⚙️',
                'requirements': ['tkinter']
            },
            'turtle': {
                'name': 'Geometric Pattern Generator',
                'description': 'Creates beautiful circular patterns using turtle graphics',
                'category': 'Graphics',
                'file': 'Turtle.py',
                'icon': '🐢',
                'requirements': ['turtle']
            },
            'snow': {
                'name': 'Snowflake Pattern Generator',
                'description': 'Creates snowflake patterns with customizable parameters',
                'category': 'Graphics',
                'file': 'snow.py',
                'icon': '❄️',
                'requirements': ['turtle', 'random']
            },
            'text': {
                'name': 'Text Evolution Simulator',
                'description': 'Demonstrates evolutionary algorithms through text generation',
                'category': 'Algorithms',
                'file': 'text.py',
                'icon': '🧬',
                'requirements': ['random', 'string', 'time']
            },
            'grv_styles': {
                'name': 'GRV Text Styles',
                'description': 'Display GRV in 10 different artistic styles',
                'category': 'Fun',
                'file': 'grv_styles.py',
                'icon': '🎨',
                'requirements': []
            },
            'mathstables': {
                'name': 'Multiplication Table Generator',
                'description': 'Generates customizable multiplication tables',
                'category': 'Education',
                'file': 'mathstables.py',
                'icon': '🔢',
                'requirements': []
            }
        }
        
        self.setup_ui()
        self.check_dependencies()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Category.TLabel', 
                     background='#f0f0f0', 
                     font=('Arial', 12, 'bold'))
        style.configure('Title.TLabel', 
                     background='#f0f0f0', 
                     font=('Arial', 16, 'bold'))
        style.configure('Program.TButton', 
                     font=('Arial', 10),
                     padding=10)
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, 
                           text="Advanced Graphics & Algorithms Suite",
                           font=('Arial', 20, 'bold'),
                           bg='#f0f0f0',
                           fg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                             text="Click any program to launch it",
                             font=('Arial', 12),
                             bg='#f0f0f0',
                             fg='#7f8c8d')
        subtitle_label.pack(pady=5)
        
        # Main content area with scrollbar
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create program buttons by category
        self.create_category_buttons(scrollable_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to launch programs")
        status_bar = tk.Label(self.root, 
                           textvariable=self.status_var,
                           bd=1, 
                           relief=tk.SUNKEN, 
                           anchor=tk.W,
                           bg='#34495e', 
                           fg='white',
                           font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel for scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def create_category_buttons(self, parent):
        """Create program buttons organized by category"""
        categories = {}
        
        # Group programs by category
        for key, program in self.programs.items():
            category = program['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((key, program))
        
        # Create frames for each category
        row = 0
        for category, programs in categories.items():
            # Category header
            category_frame = tk.Frame(parent, bg='#f0f0f0')
            category_frame.pack(fill=tk.X, pady=15)
            
            category_label = tk.Label(category_frame,
                                text=f"{category}",
                                font=('Arial', 14, 'bold'),
                                bg='#f0f0f0',
                                fg='#2c3e50',
                                anchor='w')
            category_label.pack(fill=tk.X, pady=(0, 10))
            
            # Separator line
            separator = tk.Frame(category_frame, height=2, bg='#bdc3c7')
            separator.pack(fill=tk.X, pady=(0, 10))
            
            # Program buttons grid
            buttons_frame = tk.Frame(category_frame, bg='#f0f0f0')
            buttons_frame.pack(fill=tk.X)
            
            # Create buttons in a grid layout (3 columns)
            for i, (key, program) in enumerate(programs):
                col = i % 3
                if col == 0:
                    row_frame = tk.Frame(buttons_frame, bg='#f0f0f0')
                    row_frame.pack(fill=tk.X, pady=5)
                
                self.create_program_button(row_frame, key, program)
            
            row += 1
    
    def create_program_button(self, parent, key, program):
        """Create a button for a single program"""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)
        
        # Button with program info
        button = tk.Button(button_frame,
                        text=f"{program['icon']}\n{program['name']}",
                        font=('Arial', 11, 'bold'),
                        bg='#3498db',
                        fg='white',
                        activebackground='#2980b9',
                        activeforeground='white',
                        relief=tk.RAISED,
                        bd=2,
                        padx=15,
                        pady=20,
                        wraplength=200,
                        justify=tk.CENTER,
                        cursor='hand2',
                        command=lambda k=key: self.launch_program(k))
        button.pack(fill=tk.X, expand=True)
        
        # Description label
        desc_label = tk.Label(button_frame,
                           text=program['description'],
                           font=('Arial', 8),
                           bg='#f0f0f0',
                           fg='#7f8c8d',
                           wraplength=200,
                           justify=tk.CENTER)
        desc_label.pack(fill=tk.X, pady=(5, 0))
        
        # Store reference for status updates
        button.program_key = key
        
    def check_dependencies(self):
        """Check dependencies for all programs"""
        missing_count = 0
        total_count = 0
        
        for key, program in self.programs.items():
            total_count += 1
            if not self.check_program_dependencies(program['requirements']):
                missing_count += 1
        
        if missing_count > 0:
            self.status_var.set(f"Warning: {missing_count} programs have missing dependencies")
        else:
            self.status_var.set("All dependencies satisfied - Ready to launch programs")
    
    def check_program_dependencies(self, requirements: List[str]) -> bool:
        """Check if specific program dependencies are available"""
        for module in requirements:
            try:
                if module == 'tkinter':
                    import tkinter
                elif module == 'turtle':
                    import turtle
                else:
                    importlib.import_module(module)
            except ImportError:
                return False
        return True
    
    def launch_program(self, program_key: str):
        """Launch the selected program"""
        program = self.programs[program_key]
        
        # Check dependencies first
        if not self.check_program_dependencies(program['requirements']):
            missing_deps = []
            for module in program['requirements']:
                try:
                    if module == 'tkinter':
                        import tkinter
                    elif module == 'turtle':
                        import turtle
                    else:
                        importlib.import_module(module)
                except ImportError:
                    missing_deps.append(module)
            
            messagebox.showerror(
                "Missing Dependencies",
                f"Cannot launch {program['name']}.\n\n"
                f"Missing required modules: {', '.join(missing_deps)}\n\n"
                f"Install using: pip install {' '.join(missing_deps)}"
            )
            return
        
        try:
            self.status_var.set(f"Launching {program['name']}...")
            self.root.update()
            
            # Launch the program in a new process
            subprocess.Popen([sys.executable, program['file']], 
                           cwd=os.getcwd(),
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            self.status_var.set(f"Launched {program['name']} successfully")
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch {program['name']}:\n{str(e)}"
            )
            self.status_var.set(f"Error launching {program['name']}")
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Install Dependencies", command=self.install_dependencies)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Check Dependencies", command=self.check_all_dependencies)
    
    def install_dependencies(self):
        """Install all required dependencies"""
        try:
            self.status_var.set("Installing dependencies...")
            self.root.update()
            
            # Run pip install
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Dependencies installed successfully!")
                self.status_var.set("Dependencies installed - Ready to launch programs")
            else:
                messagebox.showerror("Error", f"Failed to install dependencies:\n{result.stderr}")
                self.status_var.set("Dependency installation failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies:\n{str(e)}")
            self.status_var.set("Dependency installation failed")
    
    def check_all_dependencies(self):
        """Show detailed dependency status"""
        status_window = tk.Toplevel(self.root)
        status_window.title("Dependency Status")
        status_window.geometry("600x400")
        status_window.configure(bg='#f0f0f0')
        
        # Title
        title_label = tk.Label(status_window,
                           text="Program Dependency Status",
                           font=('Arial', 14, 'bold'),
                           bg='#f0f0f0',
                           fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Status text
        text_frame = tk.Frame(status_window, bg='#f0f0f0')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        status_text = tk.Text(text_frame, wrap=tk.WORD, height=15)
        scrollbar = tk.Scrollbar(text_frame, command=status_text.yview)
        status_text.configure(yscrollcommand=scrollbar.set)
        
        # Check each program
        for key, program in self.programs.items():
            status_text.insert(tk.END, f"{program['icon']} {program['name']}\n", 'title')
            status_text.insert(tk.END, f"  Category: {program['category']}\n")
            status_text.insert(tk.END, f"  File: {program['file']}\n")
            
            if self.check_program_dependencies(program['requirements']):
                status_text.insert(tk.END, "  Status: ✓ All dependencies satisfied\n", 'success')
            else:
                status_text.insert(tk.END, "  Status: ✗ Missing dependencies\n", 'error')
                status_text.insert(tk.END, f"  Required: {', '.join(program['requirements'])}\n", 'warning')
            
            status_text.insert(tk.END, "\n")
        
        # Configure text tags
        status_text.tag_config('title', font=('Arial', 11, 'bold'), foreground='#2c3e50')
        status_text.tag_config('success', foreground='#27ae60')
        status_text.tag_config('error', foreground='#e74c3c')
        status_text.tag_config('warning', foreground='#f39c12')
        
        status_text.config(state=tk.DISABLED)
        
        # Pack text and scrollbar
        status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Close button
        close_button = tk.Button(status_window,
                             text="Close",
                             command=status_window.destroy,
                             bg='#3498db',
                             fg='white',
                             font=('Arial', 10))
        close_button.pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Advanced Graphics & Algorithms Suite v3.0

A comprehensive collection of educational and advanced Python programs demonstrating graphics, machine learning, data visualization, animations, and algorithms.

Features:
• Advanced fractal generation
• Machine learning pattern recognition
• Interactive data visualization
• Physics-based animations
• Configuration management
• Classic educational programs

Created for educational purposes and learning Python programming concepts."""
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the GUI application"""
        self.create_menu_bar()
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()


def main():
    """Main function to run the GUI launcher"""
    print("Starting Advanced Graphics & Algorithms Suite GUI Launcher...")
    
    try:
        app = ProgramLauncherGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nGUI launcher interrupted by user.")
    except Exception as e:
        print(f"Error starting GUI launcher: {e}")
        # Fallback to CLI launcher
        try:
            import main as cli_main
            cli_main.main()
        except ImportError:
            print("CLI launcher not available. Exiting.")


if __name__ == "__main__":
    main()
