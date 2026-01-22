"""
Enhanced GUI Launcher with Modern Design
Beautiful, feature-rich graphical interface for launching programs
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import importlib.util
from typing import Dict, List
import threading
import time
from datetime import datetime
import json
import webbrowser
import math


class EnhancedGUILauncher:
    """Enhanced GUI launcher with modern design and animations"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Graphics & Algorithms Suite")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Configure modern style
        self.setup_modern_style()
        
        # Animation variables
        self.animations_running = True
        self.particle_positions = []
        self.init_particles()
        
        # Program definitions with enhanced data
        self.programs = {
            'fractals': {
                'name': 'Advanced Fractal Generator',
                'description': 'Generate complex fractals with real-time rendering',
                'category': 'Graphics',
                'file': 'fractals.py',
                'icon': '🌀',
                'color': '#FF6B6B',
                'gradient': '#FF8E8E',
                'requirements': ['numpy', 'matplotlib', 'tkinter'],
                'difficulty': 'Advanced',
                'features': ['Real-time rendering', 'Multiple fractal types', 'Export capabilities'],
                'rating': 4.8,
                'users': '2.5k'
            },
            'data_viz': {
                'name': 'Data Visualization Suite',
                'description': 'Interactive charts and advanced data analysis',
                'category': 'Data Science',
                'file': 'data_viz.py',
                'icon': '📊',
                'color': '#4ECDC4',
                'gradient': '#6EE7E0',
                'requirements': ['numpy', 'matplotlib', 'pandas', 'seaborn', 'tkinter'],
                'difficulty': 'Intermediate',
                'features': ['10+ chart types', 'Real-time analysis', 'Data cleaning tools'],
                'rating': 4.6,
                'users': '1.8k'
            },
            'ml_patterns': {
                'name': 'ML Pattern Recognition',
                'description': 'Machine learning algorithms with visualization',
                'category': 'Machine Learning',
                'file': 'ml_patterns.py',
                'icon': '🤖',
                'color': '#45B7D1',
                'gradient': '#6AC5DB',
                'requirements': ['numpy', 'matplotlib', 'scikit-learn', 'tkinter'],
                'difficulty': 'Advanced',
                'features': ['6+ algorithms', 'Model comparison', 'Interactive visualization'],
                'rating': 4.7,
                'users': '1.2k'
            },
            'animations': {
                'name': 'Animation System',
                'description': 'Physics-based animations and particle effects',
                'category': 'Graphics',
                'file': 'animations.py',
                'icon': '🎮',
                'color': '#96CEB4',
                'gradient': '#B4E6CE',
                'requirements': ['pygame', 'numpy'],
                'difficulty': 'Intermediate',
                'features': ['Physics simulation', 'Particle systems', 'Real-time controls'],
                'rating': 4.5,
                'users': '980'
            },
            'image_processor': {
                'name': 'Image Processing Suite',
                'description': 'Professional image manipulation and analysis',
                'category': 'Graphics',
                'file': 'image_processor.py',
                'icon': '🖼️',
                'color': '#FECA57',
                'gradient': '#FFD97D',
                'requirements': ['PIL', 'numpy', 'matplotlib', 'opencv-python'],
                'difficulty': 'Intermediate',
                'features': ['Advanced filters', 'Batch processing', 'Analysis tools'],
                'rating': 4.4,
                'users': '750'
            },
            'network_analyzer': {
                'name': 'Network Traffic Analyzer',
                'description': 'Real-time network monitoring and analysis',
                'category': 'System Tools',
                'file': 'network_analyzer.py',
                'icon': '🌐',
                'color': '#A55EEA',
                'gradient': '#C47FED',
                'requirements': ['psutil', 'matplotlib', 'numpy'],
                'difficulty': 'Advanced',
                'features': ['Real-time monitoring', 'Traffic analysis', 'Connection tracking'],
                'rating': 4.3,
                'users': '620'
            },
            'web_launcher': {
                'name': 'Web-Based Launcher',
                'description': 'Modern web interface for program management',
                'category': 'Utilities',
                'file': 'web_launcher.py',
                'icon': '🌍',
                'color': '#00D2D3',
                'gradient': '#33E5E5',
                'requirements': ['flask', 'numpy', 'matplotlib'],
                'difficulty': 'Intermediate',
                'features': ['Web interface', 'Remote access', 'Modern UI'],
                'rating': 4.9,
                'users': '1.5k'
            },
            'config_manager': {
                'name': 'Configuration Manager',
                'description': 'Manage application settings and preferences',
                'category': 'Utilities',
                'file': 'config_manager.py',
                'icon': '⚙️',
                'color': '#FFEAA7',
                'gradient': '#FFF3CD',
                'requirements': ['tkinter'],
                'difficulty': 'Beginner',
                'features': ['Settings persistence', 'User profiles', 'Import/Export'],
                'rating': 4.2,
                'users': '890'
            },
            'turtle': {
                'name': 'Geometric Pattern Generator',
                'description': 'Beautiful circular patterns with turtle graphics',
                'category': 'Graphics',
                'file': 'Turtle.py',
                'icon': '🐢',
                'color': '#DDA0DD',
                'gradient': '#E8C4E8',
                'requirements': ['turtle'],
                'difficulty': 'Beginner',
                'features': ['Customizable patterns', 'Interactive controls', 'Export options'],
                'rating': 4.1,
                'users': '1.1k'
            },
            'snow': {
                'name': 'Snowflake Pattern Generator',
                'description': 'Creates intricate snowflake patterns',
                'category': 'Graphics',
                'file': 'snow.py',
                'icon': '❄️',
                'color': '#87CEEB',
                'gradient': '#B4E0F3',
                'requirements': ['turtle', 'random'],
                'difficulty': 'Beginner',
                'features': ['Random patterns', 'Color variations', 'Custom parameters'],
                'rating': 4.0,
                'users': '950'
            },
            'text': {
                'name': 'Text Evolution Simulator',
                'description': 'Evolutionary algorithms for text generation',
                'category': 'Algorithms',
                'file': 'text.py',
                'icon': '🧬',
                'color': '#98D8C8',
                'gradient': '#B8E8D8',
                'requirements': ['random', 'string', 'time'],
                'difficulty': 'Intermediate',
                'features': ['Evolution visualization', 'Performance metrics', 'Configurable parameters'],
                'rating': 3.9,
                'users': '720'
            },
            'mathstables': {
                'name': 'Multiplication Table Generator',
                'description': 'Customizable multiplication tables with export',
                'category': 'Education',
                'file': 'mathstables.py',
                'icon': '🔢',
                'color': '#F7DC6F',
                'gradient': '#FAE692',
                'requirements': [],
                'difficulty': 'Beginner',
                'features': ['Customizable size', 'File export', 'Formatted output'],
                'rating': 3.8,
                'users': '580'
            }
        }
        
        # Status tracking
        self.program_status = {}
        for key in self.programs:
            self.program_status[key] = {
                'status': 'ready',
                'last_run': None,
                'dependencies_ok': self.check_program_dependencies(self.programs[key]['requirements'])
            }
        
        self.setup_ui()
        self.start_animations()
        
    def setup_modern_style(self):
        """Setup modern styling with custom colors and fonts"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel',
                     background='#1a1a2e',
                     foreground='#ffffff',
                     font=('Segoe UI', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                     background='#1a1a2e',
                     foreground='#b8b8d1',
                     font=('Segoe UI', 12))
        
        style.configure('Category.TLabel',
                     background='#1a1a2e',
                     foreground='#ffffff',
                     font=('Segoe UI', 16, 'bold'))
        
        style.configure('Modern.TButton',
                     font=('Segoe UI', 10, 'bold'),
                     padding=15,
                     relief=tk.FLAT)
        
    def init_particles(self):
        """Initialize background particles for animation"""
        for _ in range(50):
            self.particle_positions.append({
                'x': math.random() * 1200,
                'y': math.random() * 800,
                'vx': (math.random() - 0.5) * 0.5,
                'vy': (math.random() - 0.5) * 0.5,
                'size': math.random() * 3 + 1,
                'opacity': math.random() * 0.5 + 0.2
            })
    
    def setup_ui(self):
        """Setup the enhanced user interface"""
        # Create main canvas for animations
        self.main_canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable frame
        self.scroll_frame = tk.Frame(self.main_canvas, bg='#1a1a2e')
        self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        # Header with animation
        self.create_header()
        
        # Stats bar
        self.create_stats_bar()
        
        # Search and filter
        self.create_search_bar()
        
        # Program cards container
        self.cards_container = tk.Frame(self.scroll_frame, bg='#1a1a2e')
        self.cards_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create program cards
        self.create_program_cards()
        
        # Footer
        self.create_footer()
        
        # Configure scrolling
        self.scroll_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<MouseWheel>", self.on_mousewheel)
        
    def create_header(self):
        """Create animated header"""
        header_frame = tk.Frame(self.scroll_frame, bg='#1a1a2e')
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Title with gradient effect
        title_label = tk.Label(header_frame,
                           text="Advanced Graphics & Algorithms Suite",
                           font=('Segoe UI', 28, 'bold'),
                           bg='#1a1a2e',
                           fg='#ffffff')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                             text="Professional tools for graphics, machine learning, and data analysis",
                             font=('Segoe UI', 12),
                             bg='#1a1a2e',
                             fg='#b8b8d1')
        subtitle_label.pack(pady=5)
        
        # Animated underline
        self.underline_canvas = tk.Canvas(header_frame, bg='#1a1a2e', height=3, highlightthickness=0)
        self.underline_canvas.pack(fill=tk.X, pady=10)
        
    def create_stats_bar(self):
        """Create statistics bar"""
        stats_frame = tk.Frame(self.scroll_frame, bg='#16213e', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Calculate stats
        total_programs = len(self.programs)
        ready_programs = sum(1 for status in self.program_status.values() if status['dependencies_ok'])
        categories = len(set(p['category'] for p in self.programs.values()))
        
        # Create stat items
        stats = [
            ("Total Programs", total_programs, "#4ECDC4"),
            ("Ready to Run", ready_programs, "#45B7D1"),
            ("Categories", categories, "#96CEB4"),
            ("Last Update", datetime.now().strftime("%H:%M"), "#FECA57")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg='#16213e')
            stat_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=15)
            
            tk.Label(stat_frame, text=str(value),
                    font=('Segoe UI', 20, 'bold'),
                    bg='#16213e',
                    fg=color).pack()
            
            tk.Label(stat_frame, text=label,
                    font=('Segoe UI', 10),
                    bg='#16213e',
                    fg='#b8b8d1').pack()
    
    def create_search_bar(self):
        """Create search and filter bar"""
        search_frame = tk.Frame(self.scroll_frame, bg='#1a1a2e')
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_programs)
        
        search_entry = tk.Entry(search_frame,
                              textvariable=self.search_var,
                              font=('Segoe UI', 12),
                              bg='#16213e',
                              fg='#ffffff',
                              insertbackground='#ffffff',
                              relief=tk.FLAT)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        search_entry.insert(0, "🔍 Search programs...")
        
        # Category filter
        self.category_var = tk.StringVar(value="All Categories")
        categories = ["All Categories"] + list(set(p['category'] for p in self.programs.values()))
        
        category_menu = ttk.Combobox(search_frame,
                                    textvariable=self.category_var,
                                    values=categories,
                                    state="readonly",
                                    font=('Segoe UI', 10))
        category_menu.pack(side=tk.LEFT, padx=10)
        category_menu.bind('<<ComboboxSelected>>', self.filter_programs)
        
        # Sort options
        self.sort_var = tk.StringVar(value="Sort by Name")
        sort_options = ["Sort by Name", "Sort by Rating", "Sort by Difficulty", "Sort by Category"]
        
        sort_menu = ttk.Combobox(search_frame,
                               textvariable=self.sort_var,
                               values=sort_options,
                               state="readonly",
                               font=('Segoe UI', 10))
        sort_menu.pack(side=tk.LEFT, padx=10)
        sort_menu.bind('<<ComboboxSelected>>', self.filter_programs)
    
    def create_program_cards(self):
        """Create modern program cards"""
        # Clear existing cards
        for widget in self.cards_container.winfo_children():
            widget.destroy()
        
        # Get filtered and sorted programs
        programs = self.get_filtered_programs()
        
        # Create cards in grid layout
        rows = (len(programs) + 2) // 3  # 3 columns
        
        for i, (key, program) in enumerate(programs):
            row = i // 3
            col = i % 3
            
            card_frame = tk.Frame(self.cards_container, bg='#16213e', relief=tk.RAISED, bd=1)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            self.create_program_card(card_frame, key, program)
        
        # Configure grid weights
        for i in range(3):
            self.cards_container.columnconfigure(i, weight=1)
    
    def create_program_card(self, parent, key, program):
        """Create individual program card"""
        # Card header with gradient
        header_frame = tk.Frame(parent, bg=program['color'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Icon and title
        title_frame = tk.Frame(header_frame, bg=program['color'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        icon_label = tk.Label(title_frame,
                            text=program['icon'],
                            font=('Segoe UI', 24),
                            bg=program['color'],
                            fg='#ffffff')
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame,
                             text=program['name'],
                             font=('Segoe UI', 12, 'bold'),
                             bg=program['color'],
                             fg='#ffffff')
        title_label.pack(side=tk.LEFT)
        
        # Rating and users
        rating_frame = tk.Frame(title_frame, bg=program['color'])
        rating_frame.pack(side=tk.RIGHT)
        
        rating_text = f"⭐ {program['rating']} • {program['users']}"
        tk.Label(rating_frame,
                text=rating_text,
                font=('Segoe UI', 8),
                bg=program['color'],
                fg='#ffffff').pack()
        
        # Card content
        content_frame = tk.Frame(parent, bg='#16213e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Description
        desc_label = tk.Label(content_frame,
                            text=program['description'],
                            font=('Segoe UI', 10),
                            bg='#16213e',
                            fg='#b8b8d1',
                            wraplength=250,
                            justify=tk.LEFT)
        desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Features
        features_frame = tk.Frame(content_frame, bg='#16213e')
        features_frame.pack(fill=tk.X, pady=(0, 10))
        
        for feature in program['features'][:2]:  # Show first 2 features
            feature_label = tk.Label(features_frame,
                                  text=f"• {feature}",
                                  font=('Segoe UI', 8),
                                  bg='#16213e',
                                  fg='#4ECDC4')
            feature_label.pack(anchor=tk.W)
        
        # Difficulty badge
        difficulty_colors = {
            'Beginner': '#27ae60',
            'Intermediate': '#f39c12',
            'Advanced': '#e74c3c'
        }
        
        diff_color = difficulty_colors.get(program['difficulty'], '#95a5a6')
        difficulty_label = tk.Label(content_frame,
                                   text=program['difficulty'],
                                   font=('Segoe UI', 8, 'bold'),
                                   bg=diff_color,
                                   fg='#ffffff',
                                   padx=8,
                                   pady=2)
        difficulty_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Status indicator
        status = self.program_status[key]['status']
        status_colors = {
            'ready': '#27ae60',
            'running': '#3498db',
            'stopped': '#e74c3c'
        }
        
        status_color = status_colors.get(status, '#95a5a6')
        status_label = tk.Label(content_frame,
                              text=f"● {status.upper()}",
                              font=('Segoe UI', 8, 'bold'),
                              bg='#16213e',
                              fg=status_color)
        status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Launch button
        launch_btn = tk.Button(content_frame,
                             text="LAUNCH",
                             font=('Segoe UI', 10, 'bold'),
                             bg=program['color'],
                             fg='#ffffff',
                             activebackground=program['gradient'],
                             relief=tk.FLAT,
                             bd=0,
                             padx=20,
                             pady=8,
                             cursor='hand2',
                             command=lambda k=key: self.launch_program(k))
        launch_btn.pack(fill=tk.X, pady=10)
        
        # Hover effects
        launch_btn.bind('<Enter>', lambda e: self.on_button_enter(e, launch_btn, program['gradient']))
        launch_btn.bind('<Leave>', lambda e: self.on_button_leave(e, launch_btn, program['color']))
    
    def create_footer(self):
        """Create footer with controls"""
        footer_frame = tk.Frame(self.scroll_frame, bg='#16213e', relief=tk.RAISED, bd=1)
        footer_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Control buttons
        controls = [
            ("🔧 Check Dependencies", self.check_all_dependencies),
            ("📦 Install All", self.install_all_dependencies),
            ("🔄 Refresh Status", self.refresh_status),
            ("🌐 Web Interface", self.launch_web_interface),
            ("⚙️ Settings", self.open_settings)
        ]
        
        for text, command in controls:
            btn = tk.Button(footer_frame,
                          text=text,
                          font=('Segoe UI', 10),
                          bg='#1a1a2e',
                          fg='#ffffff',
                          activebackground='#0f3460',
                          relief=tk.FLAT,
                          bd=0,
                          padx=15,
                          pady=8,
                          cursor='hand2',
                          command=command)
            btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to launch programs")
        
        status_label = tk.Label(footer_frame,
                               textvariable=self.status_var,
                               font=('Segoe UI', 10),
                               bg='#16213e',
                               fg='#b8b8d1')
        status_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def on_button_enter(self, event, button, color):
        """Button hover enter effect"""
        button.config(bg=color)
    
    def on_button_leave(self, event, button, color):
        """Button hover leave effect"""
        button.config(bg=color)
    
    def start_animations(self):
        """Start background animations"""
        self.animate_particles()
        self.animate_underline()
    
    def animate_particles(self):
        """Animate background particles"""
        if self.animations_running:
            # Clear previous particles
            self.main_canvas.delete("particle")
            
            # Update and draw particles
            for particle in self.particle_positions:
                # Update position
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                
                # Wrap around screen
                if particle['x'] < 0:
                    particle['x'] = 1200
                elif particle['x'] > 1200:
                    particle['x'] = 0
                
                if particle['y'] < 0:
                    particle['y'] = 800
                elif particle['y'] > 800:
                    particle['y'] = 0
                
                # Draw particle
                self.main_canvas.create_oval(
                    particle['x'] - particle['size'],
                    particle['y'] - particle['size'],
                    particle['x'] + particle['size'],
                    particle['y'] + particle['size'],
                    fill='#4ECDC4',
                    outline='',
                    tags='particle'
                )
            
            # Schedule next frame
            self.root.after(50, self.animate_particles)
    
    def animate_underline(self):
        """Animate header underline"""
        if self.animations_running:
            self.underline_canvas.delete("underline")
            
            # Get canvas width
            self.underline_canvas.update()
            width = self.underline_canvas.winfo_width()
            
            # Animated gradient line
            for i in range(0, width, 5):
                color_intensity = int(128 + 127 * math.sin(time.time() * 2 + i * 0.01))
                color = f'#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}'
                
                self.underline_canvas.create_line(
                    i, 0, i + 5, 3,
                    fill=color,
                    width=2,
                    tags='underline'
                )
            
            # Schedule next frame
            self.root.after(100, self.animate_underline)
    
    def get_filtered_programs(self):
        """Get filtered and sorted programs"""
        programs = list(self.programs.items())
        
        # Filter by search
        search_term = self.search_var.get().lower()
        if search_term and search_term != "🔍 search programs...":
            programs = [(k, p) for k, p in programs if 
                       search_term in p['name'].lower() or 
                       search_term in p['description'].lower()]
        
        # Filter by category
        category = self.category_var.get()
        if category != "All Categories":
            programs = [(k, p) for k, p in programs if p['category'] == category]
        
        # Sort
        sort_option = self.sort_var.get()
        if sort_option == "Sort by Name":
            programs.sort(key=lambda x: x[1]['name'])
        elif sort_option == "Sort by Rating":
            programs.sort(key=lambda x: x[1]['rating'], reverse=True)
        elif sort_option == "Sort by Difficulty":
            difficulty_order = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2}
            programs.sort(key=lambda x: difficulty_order.get(x[1]['difficulty'], 3))
        elif sort_option == "Sort by Category":
            programs.sort(key=lambda x: x[1]['category'])
        
        return programs
    
    def filter_programs(self, *args):
        """Filter and refresh program cards"""
        self.create_program_cards()
    
    def on_frame_configure(self, event):
        """Handle frame configure event"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def check_program_dependencies(self, requirements: List[str]) -> bool:
        """Check if program dependencies are available"""
        for module in requirements:
            try:
                if module == 'tkinter':
                    import tkinter
                elif module == 'turtle':
                    import turtle
                else:
                    importlib.util.find_spec(module)
                    if module == 'opencv-python':
                        import cv2
                    else:
                        importlib.import_module(module)
            except ImportError:
                return False
        return True
    
    def launch_program(self, program_key: str):
        """Launch selected program"""
        program = self.programs[program_key]
        
        # Check dependencies
        if not self.check_program_dependencies(program['requirements']):
            missing_deps = []
            for module in program['requirements']:
                try:
                    if module == 'tkinter':
                        import tkinter
                    elif module == 'turtle':
                        import turtle
                    else:
                        importlib.util.find_spec(module)
                        if module == 'opencv-python':
                            import cv2
                        else:
                            importlib.import_module(module)
                except ImportError:
                    missing_deps.append(module)
            
            messagebox.showerror(
                "Missing Dependencies",
                f"Cannot launch {program['name']}.\n\n"
                f"Missing: {', '.join(missing_deps)}\n\n"
                f"Install using: pip install {' '.join(missing_deps)}"
            )
            return
        
        try:
            self.status_var.set(f"Launching {program['name']}...")
            self.root.update()
            
            # Launch program
            subprocess.Popen([sys.executable, program['file']],
                           cwd=os.getcwd(),
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            self.program_status[program_key]['status'] = 'running'
            self.program_status[program_key]['last_run'] = datetime.now().isoformat()
            
            self.status_var.set(f"Launched {program['name']} successfully!")
            
            # Update card after delay
            self.root.after(1000, self.create_program_cards)
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {program['name']}:\n{str(e)}")
            self.status_var.set(f"Error launching {program['name']}")
    
    def check_all_dependencies(self):
        """Check all program dependencies"""
        missing_count = 0
        total_count = len(self.programs)
        
        for key, program in self.programs.items():
            if not self.check_program_dependencies(program['requirements']):
                missing_count += 1
                self.program_status[key]['dependencies_ok'] = False
            else:
                self.program_status[key]['dependencies_ok'] = True
        
        if missing_count == 0:
            messagebox.showinfo("Dependencies", "All dependencies are satisfied!")
            self.status_var.set("All dependencies OK")
        else:
            messagebox.showwarning("Dependencies", f"{missing_count} programs have missing dependencies")
            self.status_var.set(f"{missing_count} programs need dependencies")
        
        self.create_program_cards()
    
    def install_all_dependencies(self):
        """Install all dependencies"""
        try:
            self.status_var.set("Installing dependencies...")
            self.root.update()
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Dependencies installed successfully!")
                self.status_var.set("Dependencies installed")
                self.check_all_dependencies()
            else:
                messagebox.showerror("Error", f"Installation failed:\n{result.stderr}")
                self.status_var.set("Installation failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies:\n{str(e)}")
            self.status_var.set("Installation error")
    
    def refresh_status(self):
        """Refresh program status"""
        for key in self.programs:
            self.program_status[key]['status'] = 'ready'
        
        self.create_program_cards()
        self.status_var.set("Status refreshed")
    
    def launch_web_interface(self):
        """Launch web interface"""
        try:
            subprocess.Popen([sys.executable, "web_launcher.py"],
                           cwd=os.getcwd(),
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            self.status_var.set("Web interface launched")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch web interface:\n{str(e)}")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#1a1a2e')
        
        tk.Label(settings_window,
                text="Settings",
                font=('Segoe UI', 16, 'bold'),
                bg='#1a1a2e',
                fg='#ffffff').pack(pady=20)
        
        tk.Label(settings_window,
                text="Settings panel coming soon!",
                font=('Segoe UI', 12),
                bg='#1a1a2e',
                fg='#b8b8d1').pack(pady=20)
        
        tk.Button(settings_window,
                text="Close",
                font=('Segoe UI', 10),
                bg='#4ECDC4',
                fg='#ffffff',
                relief=tk.FLAT,
                bd=0,
                padx=20,
                pady=8,
                command=settings_window.destroy).pack(pady=20)
    
    def run(self):
        """Run the enhanced GUI"""
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()


def main():
    """Main function to run the enhanced GUI launcher"""
    print("Starting Enhanced GUI Launcher...")
    print("Modern interface with animations and advanced features")
    
    try:
        app = EnhancedGUILauncher()
        app.run()
    except KeyboardInterrupt:
        print("\nEnhanced GUI launcher interrupted by user.")
    except Exception as e:
        print(f"Error starting enhanced GUI: {e}")
        # Fallback to basic GUI
        try:
            import gui_launcher
            gui_launcher.main()
        except ImportError:
            print("Basic GUI also not available. Exiting.")


if __name__ == "__main__":
    main()
