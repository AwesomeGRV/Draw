"""
Configuration Manager
Handles application settings, user preferences, and data persistence
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


@dataclass
class AppConfig:
    """Application configuration"""
    # Window settings
    window_width: int = 1200
    window_height: int = 800
    window_maximized: bool = False
    
    # Theme settings
    theme: str = "default"
    font_size: int = 12
    font_family: str = "Arial"
    
    # Graphics settings
    default_color_scheme: str = "rainbow"
    default_iterations: int = 100
    default_zoom: float = 1.0
    
    # Data settings
    auto_save: bool = True
    auto_save_interval: int = 300  # seconds
    default_data_path: str = "./data"
    
    # ML settings
    default_test_size: float = 0.3
    default_random_state: int = 42
    
    # Animation settings
    default_fps: int = 60
    particle_count: int = 100
    
    # Recent files
    recent_files: List[str] = None
    
    def __post_init__(self):
        if self.recent_files is None:
            self.recent_files = []


@dataclass
class UserProfile:
    """User profile and preferences"""
    username: str = "User"
    email: str = ""
    skill_level: str = "beginner"  # beginner, intermediate, advanced
    preferred_modules: List[str] = None
    custom_settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.preferred_modules is None:
            self.preferred_modules = []
        if self.custom_settings is None:
            self.custom_settings = {}


class ConfigManager:
    """Manages application configuration and user data"""
    
    def __init__(self, app_name: str = "AdvancedGraphicsSuite"):
        self.app_name = app_name
        self.config_dir = Path.home() / f".{app_name.lower()}"
        self.config_file = self.config_dir / "config.json"
        self.profile_file = self.config_dir / "profile.json"
        self.data_dir = self.config_dir / "data"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        self.profile = self.load_profile()
    
    def load_config(self) -> AppConfig:
        """Load application configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                return AppConfig(**data)
            except Exception as e:
                print(f"Error loading config: {e}")
                return AppConfig()
        return AppConfig()
    
    def save_config(self):
        """Save application configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_profile(self) -> UserProfile:
        """Load user profile"""
        if self.profile_file.exists():
            try:
                with open(self.profile_file, 'r') as f:
                    data = json.load(f)
                return UserProfile(**data)
            except Exception as e:
                print(f"Error loading profile: {e}")
                return UserProfile()
        return UserProfile()
    
    def save_profile(self):
        """Save user profile"""
        try:
            with open(self.profile_file, 'w') as f:
                json.dump(asdict(self.profile), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def add_recent_file(self, filepath: str):
        """Add file to recent files list"""
        if filepath in self.config.recent_files:
            self.config.recent_files.remove(filepath)
        
        self.config.recent_files.insert(0, filepath)
        
        # Keep only last 10 files
        self.config.recent_files = self.config.recent_files[:10]
        
        self.save_config()
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files"""
        return [f for f in self.config.recent_files if os.path.exists(f)]
    
    def save_data(self, data: Any, filename: str, format: str = "pickle") -> bool:
        """Save data to file"""
        filepath = self.data_dir / filename
        
        try:
            if format == "pickle":
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
            elif format == "json":
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.add_recent_file(str(filepath))
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self, filename: str, format: str = "pickle") -> Optional[Any]:
        """Load data from file"""
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            if format == "pickle":
                with open(filepath, 'rb') as f:
                    return pickle.load(f)
            elif format == "json":
                with open(filepath, 'r') as f:
                    return json.load(f)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def export_config(self, filepath: str) -> bool:
        """Export configuration to external file"""
        try:
            export_data = {
                "config": asdict(self.config),
                "profile": asdict(self.profile)
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, filepath: str) -> bool:
        """Import configuration from external file"""
        try:
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            if "config" in import_data:
                self.config = AppConfig(**import_data["config"])
            
            if "profile" in import_data:
                self.profile = UserProfile(**import_data["profile"])
            
            self.save_config()
            self.save_profile()
            
            return True
            
        except Exception as e:
            print(f"Error importing config: {e}")
            return False


class SettingsGUI:
    """GUI for managing application settings"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.root = tk.Tk()
        self.root.title("Settings")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the settings UI"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self.setup_general_tab(general_frame)
        
        # Graphics settings tab
        graphics_frame = ttk.Frame(notebook)
        notebook.add(graphics_frame, text="Graphics")
        self.setup_graphics_tab(graphics_frame)
        
        # ML settings tab
        ml_frame = ttk.Frame(notebook)
        notebook.add(ml_frame, text="Machine Learning")
        self.setup_ml_tab(ml_frame)
        
        # User profile tab
        profile_frame = ttk.Frame(notebook)
        notebook.add(profile_frame, text="Profile")
        self.setup_profile_tab(profile_frame)
        
        # Data management tab
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="Data")
        self.setup_data_tab(data_frame)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Settings", command=self.export_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Import Settings", command=self.import_settings).pack(side=tk.LEFT, padx=5)
    
    def setup_general_tab(self, parent):
        """Setup general settings tab"""
        # Window settings
        window_frame = ttk.LabelFrame(parent, text="Window Settings", padding="10")
        window_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(window_frame, text="Window Width:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.window_width = ttk.Entry(window_frame, width=20)
        self.window_width.insert(0, str(self.config_manager.config.window_width))
        self.window_width.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(window_frame, text="Window Height:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.window_height = ttk.Entry(window_frame, width=20)
        self.window_height.insert(0, str(self.config_manager.config.window_height))
        self.window_height.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        self.window_maximized = tk.BooleanVar(value=self.config_manager.config.window_maximized)
        ttk.Checkbutton(window_frame, text="Start Maximized", variable=self.window_maximized).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Theme settings
        theme_frame = ttk.LabelFrame(parent, text="Theme Settings", padding="10")
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.theme = ttk.Combobox(theme_frame, values=["default", "dark", "light", "blue"], width=18)
        self.theme.set(self.config_manager.config.theme)
        self.theme.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(theme_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.font_size = ttk.Entry(theme_frame, width=20)
        self.font_size.insert(0, str(self.config_manager.config.font_size))
        self.font_size.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(theme_frame, text="Font Family:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.font_family = ttk.Combobox(theme_frame, values=["Arial", "Helvetica", "Times New Roman", "Courier New"], width=18)
        self.font_family.set(self.config_manager.config.font_family)
        self.font_family.grid(row=2, column=1, sticky=tk.W, pady=2)
    
    def setup_graphics_tab(self, parent):
        """Setup graphics settings tab"""
        graphics_frame = ttk.LabelFrame(parent, text="Graphics Settings", padding="10")
        graphics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(graphics_frame, text="Default Color Scheme:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.color_scheme = ttk.Combobox(graphics_frame, values=["rainbow", "fire", "ocean", "grayscale"], width=18)
        self.color_scheme.set(self.config_manager.config.default_color_scheme)
        self.color_scheme.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(graphics_frame, text="Default Iterations:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.iterations = ttk.Entry(graphics_frame, width=20)
        self.iterations.insert(0, str(self.config_manager.config.default_iterations))
        self.iterations.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(graphics_frame, text="Default Zoom:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.zoom = ttk.Entry(graphics_frame, width=20)
        self.zoom.insert(0, str(self.config_manager.config.default_zoom))
        self.zoom.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Animation settings
        animation_frame = ttk.LabelFrame(parent, text="Animation Settings", padding="10")
        animation_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(animation_frame, text="Default FPS:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.fps = ttk.Entry(animation_frame, width=20)
        self.fps.insert(0, str(self.config_manager.config.default_fps))
        self.fps.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(animation_frame, text="Particle Count:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.particle_count = ttk.Entry(animation_frame, width=20)
        self.particle_count.insert(0, str(self.config_manager.config.particle_count))
        self.particle_count.grid(row=1, column=1, sticky=tk.W, pady=2)
    
    def setup_ml_tab(self, parent):
        """Setup machine learning settings tab"""
        ml_frame = ttk.LabelFrame(parent, text="Machine Learning Settings", padding="10")
        ml_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(ml_frame, text="Default Test Size:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.test_size = ttk.Entry(ml_frame, width=20)
        self.test_size.insert(0, str(self.config_manager.config.default_test_size))
        self.test_size.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(ml_frame, text="Default Random State:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.random_state = ttk.Entry(ml_frame, width=20)
        self.random_state.insert(0, str(self.config_manager.config.default_random_state))
        self.random_state.grid(row=1, column=1, sticky=tk.W, pady=2)
    
    def setup_profile_tab(self, parent):
        """Setup user profile tab"""
        profile_frame = ttk.LabelFrame(parent, text="User Profile", padding="10")
        profile_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(profile_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.username = ttk.Entry(profile_frame, width=30)
        self.username.insert(0, self.config_manager.profile.username)
        self.username.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(profile_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email = ttk.Entry(profile_frame, width=30)
        self.email.insert(0, self.config_manager.profile.email)
        self.email.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(profile_frame, text="Skill Level:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.skill_level = ttk.Combobox(profile_frame, values=["beginner", "intermediate", "advanced"], width=28)
        self.skill_level.set(self.config_manager.profile.skill_level)
        self.skill_level.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(profile_frame, text="Preferred Modules:").grid(row=3, column=0, sticky=tk.NW, pady=2)
        self.modules_frame = ttk.Frame(profile_frame)
        self.modules_frame.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        self.module_vars = {}
        modules = ["fractals", "data_viz", "ml_patterns", "animations", "turtle", "snow", "text"]
        
        for i, module in enumerate(modules):
            var = tk.BooleanVar(value=module in self.config_manager.profile.preferred_modules)
            self.module_vars[module] = var
            ttk.Checkbutton(self.modules_frame, text=module.replace("_", " ").title(), 
                           variable=var).grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)
    
    def setup_data_tab(self, parent):
        """Setup data management tab"""
        data_frame = ttk.LabelFrame(parent, text="Data Management", padding="10")
        data_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_save = tk.BooleanVar(value=self.config_manager.config.auto_save)
        ttk.Checkbutton(data_frame, text="Auto-save", variable=self.auto_save).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(data_frame, text="Auto-save Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.auto_save_interval = ttk.Entry(data_frame, width=20)
        self.auto_save_interval.insert(0, str(self.config_manager.config.auto_save_interval))
        self.auto_save_interval.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(data_frame, text="Default Data Path:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.data_path = ttk.Entry(data_frame, width=30)
        self.data_path.insert(0, self.config_manager.config.default_data_path)
        self.data_path.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Recent files
        recent_frame = ttk.LabelFrame(parent, text="Recent Files", padding="10")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Listbox for recent files
        self.recent_listbox = tk.Listbox(recent_frame, height=8)
        self.recent_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Populate recent files
        for filepath in self.config_manager.get_recent_files():
            self.recent_listbox.insert(tk.END, os.path.basename(filepath))
        
        # Buttons for recent files
        recent_button_frame = ttk.Frame(recent_frame)
        recent_button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(recent_button_frame, text="Open", command=self.open_recent_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(recent_button_frame, text="Remove", command=self.remove_recent_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(recent_button_frame, text="Clear All", command=self.clear_recent_files).pack(side=tk.LEFT, padx=5)
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Update config
            self.config_manager.config.window_width = int(self.window_width.get())
            self.config_manager.config.window_height = int(self.window_height.get())
            self.config_manager.config.window_maximized = self.window_maximized.get()
            self.config_manager.config.theme = self.theme.get()
            self.config_manager.config.font_size = int(self.font_size.get())
            self.config_manager.config.font_family = self.font_family.get()
            self.config_manager.config.default_color_scheme = self.color_scheme.get()
            self.config_manager.config.default_iterations = int(self.iterations.get())
            self.config_manager.config.default_zoom = float(self.zoom.get())
            self.config_manager.config.default_fps = int(self.fps.get())
            self.config_manager.config.particle_count = int(self.particle_count.get())
            self.config_manager.config.default_test_size = float(self.test_size.get())
            self.config_manager.config.default_random_state = int(self.random_state.get())
            self.config_manager.config.auto_save = self.auto_save.get()
            self.config_manager.config.auto_save_interval = int(self.auto_save_interval.get())
            self.config_manager.config.default_data_path = self.data_path.get()
            
            # Update profile
            self.config_manager.profile.username = self.username.get()
            self.config_manager.profile.email = self.email.get()
            self.config_manager.profile.skill_level = self.skill_level.get()
            self.config_manager.profile.preferred_modules = [
                module for module, var in self.module_vars.items() if var.get()
            ]
            
            # Save
            self.config_manager.save_config()
            self.config_manager.save_profile()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_defaults(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.config_manager.config = AppConfig()
            self.config_manager.profile = UserProfile()
            self.config_manager.save_config()
            self.config_manager.save_profile()
            
            # Reload UI
            self.root.destroy()
            settings_gui = SettingsGUI(self.config_manager)
            settings_gui.run()
    
    def export_settings(self):
        """Export settings to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.config_manager.export_config(filename):
                messagebox.showinfo("Success", "Settings exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export settings")
    
    def import_settings(self):
        """Import settings from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.config_manager.import_config(filename):
                messagebox.showinfo("Success", "Settings imported successfully!")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Failed to import settings")
    
    def open_recent_file(self):
        """Open selected recent file"""
        selection = self.recent_listbox.curselection()
        if selection:
            recent_files = self.config_manager.get_recent_files()
            if selection[0] < len(recent_files):
                messagebox.showinfo("File Info", f"Selected: {recent_files[selection[0]]}")
    
    def remove_recent_file(self):
        """Remove selected recent file"""
        selection = self.recent_listbox.curselection()
        if selection:
            recent_files = self.config_manager.get_recent_files()
            if selection[0] < len(recent_files):
                filename = recent_files[selection[0]]
                self.config_manager.config.recent_files.remove(filename)
                self.config_manager.save_config()
                
                # Update listbox
                self.recent_listbox.delete(selection[0])
    
    def clear_recent_files(self):
        """Clear all recent files"""
        if messagebox.askyesno("Confirm", "Clear all recent files?"):
            self.config_manager.config.recent_files = []
            self.config_manager.save_config()
            self.recent_listbox.delete(0, tk.END)
    
    def run(self):
        """Run the settings GUI"""
        self.root.mainloop()


def main():
    """Main function to run the configuration manager"""
    print("Configuration Manager")
    print("=" * 30)
    
    # Create config manager
    config_manager = ConfigManager()
    
    # Show current configuration
    print("Current Configuration:")
    print(f"  Window: {config_manager.config.window_width}x{config_manager.config.window_height}")
    print(f"  Theme: {config_manager.config.theme}")
    print(f"  User: {config_manager.profile.username}")
    print(f"  Skill Level: {config_manager.profile.skill_level}")
    print()
    
    # Launch settings GUI
    settings_gui = SettingsGUI(config_manager)
    settings_gui.run()


if __name__ == "__main__":
    main()
