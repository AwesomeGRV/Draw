"""
Advanced Fractal Generator Suite
Generates complex fractals including Mandelbrot sets, Julia sets, Sierpinski triangles, and more
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import colorsys
import random
import math
import time
from dataclasses import dataclass
from typing import Tuple, Optional, Callable
import json


@dataclass
class FractalConfig:
    """Configuration for fractal generation"""
    width: int = 800
    height: int = 600
    max_iterations: int = 100
    zoom: float = 1.0
    center_x: float = 0.0
    center_y: float = 0.0
    color_scheme: str = "rainbow"
    julia_c: complex = complex(-0.7, 0.27015)
    escape_radius: float = 2.0


class FractalGenerator:
    """Base class for fractal generators"""
    
    def __init__(self, config: FractalConfig):
        self.config = config
        self.image_data = None
        
    def generate(self) -> np.ndarray:
        """Generate fractal image data"""
        raise NotImplementedError
        
    def get_color(self, iterations: int, max_iterations: int) -> Tuple[int, int, int]:
        """Get RGB color based on iteration count"""
        if iterations == max_iterations:
            return (0, 0, 0)  # Black for points in the set
            
        # Normalize iterations to [0, 1]
        normalized = iterations / max_iterations
        
        if self.config.color_scheme == "rainbow":
            # Rainbow color scheme
            hue = normalized
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        elif self.config.color_scheme == "fire":
            # Fire color scheme (black -> red -> yellow -> white)
            if normalized < 0.25:
                rgb = (0, 0, 0)
            elif normalized < 0.5:
                rgb = (4 * (normalized - 0.25), 0, 0)
            elif normalized < 0.75:
                rgb = (1, 4 * (normalized - 0.5), 0)
            else:
                rgb = (1, 1, 4 * (normalized - 0.75))
        elif self.config.color_scheme == "ocean":
            # Ocean color scheme (black -> blue -> cyan -> white)
            rgb = (0, normalized * 0.5, normalized)
        elif self.config.color_scheme == "grayscale":
            # Grayscale
            rgb = (normalized, normalized, normalized)
        else:
            rgb = (normalized, normalized, normalized)
            
        return tuple(int(c * 255) for c in rgb)


class MandelbrotGenerator(FractalGenerator):
    """Mandelbrot set generator"""
    
    def generate(self) -> np.ndarray:
        """Generate Mandelbrot set"""
        width, height = self.config.width, self.config.height
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate bounds
        x_min = self.config.center_x - 2.0 / self.config.zoom
        x_max = self.config.center_x + 2.0 / self.config.zoom
        y_min = self.config.center_y - 1.5 / self.config.zoom
        y_max = self.config.center_y + 1.5 / self.config.zoom
        
        for y in range(height):
            for x in range(width):
                # Convert pixel to complex coordinates
                real = x_min + (x / width) * (x_max - x_min)
                imag = y_min + (y / height) * (y_max - y_min)
                c = complex(real, imag)
                
                # Mandelbrot iteration
                z = 0
                iterations = 0
                
                while abs(z) <= self.config.escape_radius and iterations < self.config.max_iterations:
                    z = z * z + c
                    iterations += 1
                
                # Set pixel color
                color = self.get_color(iterations, self.config.max_iterations)
                image[y, x] = color
                
        self.image_data = image
        return image


class JuliaGenerator(FractalGenerator):
    """Julia set generator"""
    
    def generate(self) -> np.ndarray:
        """Generate Julia set"""
        width, height = self.config.width, self.config.height
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate bounds
        x_min = self.config.center_x - 2.0 / self.config.zoom
        x_max = self.config.center_x + 2.0 / self.config.zoom
        y_min = self.config.center_y - 1.5 / self.config.zoom
        y_max = self.config.center_y + 1.5 / self.config.zoom
        
        for y in range(height):
            for x in range(width):
                # Convert pixel to complex coordinates
                real = x_min + (x / width) * (x_max - x_min)
                imag = y_min + (y / height) * (y_max - y_min)
                z = complex(real, imag)
                
                # Julia iteration
                iterations = 0
                
                while abs(z) <= self.config.escape_radius and iterations < self.config.max_iterations:
                    z = z * z + self.config.julia_c
                    iterations += 1
                
                # Set pixel color
                color = self.get_color(iterations, self.config.max_iterations)
                image[y, x] = color
                
        self.image_data = image
        return image


class SierpinskiGenerator(FractalGenerator):
    """Sierpinski triangle generator"""
    
    def __init__(self, config: FractalConfig, iterations: int = 7):
        super().__init__(config)
        self.triangle_iterations = iterations
        
    def generate(self) -> np.ndarray:
        """Generate Sierpinski triangle"""
        width, height = self.config.width, self.config.height
        image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
        
        # Define triangle vertices
        vertices = [
            (width // 2, 50),  # Top
            (50, height - 50),  # Bottom left
            (width - 50, height - 50)  # Bottom right
        ]
        
        def draw_triangle(p1, p2, p3, depth):
            """Recursively draw Sierpinski triangle"""
            if depth == 0:
                # Draw filled triangle
                points = [p1, p2, p3]
                for y in range(min(p[1] for p in points), max(p[1] for p in points) + 1):
                    for x in range(min(p[0] for p in points), max(p[0] for p in points) + 1):
                        if self._point_in_triangle(x, y, p1, p2, p3):
                            if 0 <= y < height and 0 <= x < width:
                                image[y, x] = (0, 0, 0)  # Black triangle
            else:
                # Calculate midpoints
                mid1 = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
                mid2 = ((p2[0] + p3[0]) // 2, (p2[1] + p3[1]) // 2)
                mid3 = ((p3[0] + p1[0]) // 2, (p3[1] + p1[1]) // 2)
                
                # Recursively draw three smaller triangles
                draw_triangle(p1, mid1, mid3, depth - 1)
                draw_triangle(mid1, p2, mid2, depth - 1)
                draw_triangle(mid3, mid2, p3, depth - 1)
        
        draw_triangle(vertices[0], vertices[1], vertices[2], self.triangle_iterations)
        self.image_data = image
        return image
    
    def _point_in_triangle(self, x, y, p1, p2, p3):
        """Check if point is inside triangle using barycentric coordinates"""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign((x, y), p1, p2)
        d2 = sign((x, y), p2, p3)
        d3 = sign((x, y), p3, p1)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)


class DragonCurveGenerator(FractalGenerator):
    """Dragon curve fractal generator"""
    
    def __init__(self, config: FractalConfig, iterations: int = 15):
        super().__init__(config)
        self.curve_iterations = iterations
        
    def generate(self) -> np.ndarray:
        """Generate dragon curve"""
        width, height = self.config.width, self.config.height
        image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
        
        # Generate dragon curve sequence
        sequence = self._generate_dragon_sequence(self.curve_iterations)
        
        # Starting position and direction
        x, y = width // 2, height // 2
        angle = 0
        step_size = max(2, min(width, height) // (2 ** (self.curve_iterations // 2)))
        
        # Draw the curve
        points = [(x, y)]
        for turn in sequence:
            x += int(step_size * math.cos(angle))
            y += int(step_size * math.sin(angle))
            
            # Keep within bounds
            x = max(0, min(width - 1, x))
            y = max(0, min(height - 1, y))
            
            points.append((x, y))
            
            # Turn direction
            if turn == 'R':
                angle -= math.pi / 2
            else:
                angle += math.pi / 2
        
        # Draw lines connecting points
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self._draw_line(image, x1, y1, x2, y2, (255, 0, 0))  # Red color
        
        self.image_data = image
        return image
    
    def _generate_dragon_sequence(self, iterations: int) -> str:
        """Generate dragon curve turn sequence"""
        sequence = "R"
        for _ in range(iterations):
            new_sequence = sequence + "R"
            for turn in reversed(sequence):
                new_sequence += "L" if turn == "R" else "R"
            sequence = new_sequence
        return sequence
    
    def _draw_line(self, image, x1, y1, x2, y2, color):
        """Draw a line using Bresenham's algorithm"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        x_inc = 1 if x1 < x2 else -1
        y_inc = 1 if y1 < y2 else -1
        error = dx - dy
        
        for _ in range(max(dx, dy) + 1):
            if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                image[y, x] = color
            
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx


class FractalGUI:
    """GUI for fractal generation and exploration"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Fractal Generator")
        self.root.geometry("1200x800")
        
        self.config = FractalConfig()
        self.current_generator = None
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Fractal type selection
        ttk.Label(control_frame, text="Fractal Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fractal_type = ttk.Combobox(control_frame, values=["Mandelbrot", "Julia", "Sierpinski", "Dragon Curve"])
        self.fractal_type.set("Mandelbrot")
        self.fractal_type.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Parameters
        ttk.Label(control_frame, text="Max Iterations:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_iterations = ttk.Scale(control_frame, from_=50, to=500, orient=tk.HORIZONTAL)
        self.max_iterations.set(100)
        self.max_iterations.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(control_frame, text="Zoom:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.zoom = ttk.Scale(control_frame, from_=0.5, to=10, orient=tk.HORIZONTAL)
        self.zoom.set(1.0)
        self.zoom.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Color scheme
        ttk.Label(control_frame, text="Color Scheme:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.color_scheme = ttk.Combobox(control_frame, values=["rainbow", "fire", "ocean", "grayscale"])
        self.color_scheme.set("rainbow")
        self.color_scheme.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Julia set parameters (shown only for Julia)
        self.julia_frame = ttk.Frame(control_frame)
        self.julia_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.julia_frame, text="Julia C (real):").grid(row=0, column=0, sticky=tk.W)
        self.julia_real = ttk.Entry(self.julia_frame, width=10)
        self.julia_real.insert(0, "-0.7")
        self.julia_real.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.julia_frame, text="Julia C (imag):").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.julia_imag = ttk.Entry(self.julia_frame, width=10)
        self.julia_imag.insert(0, "0.27015")
        self.julia_imag.grid(row=0, column=3, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate", command=self.generate_fractal).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save Config", command=self.save_config).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Load Config", command=self.load_config).grid(row=0, column=3, padx=5)
        
        # Image display
        image_frame = ttk.LabelFrame(main_frame, text="Fractal Display", padding="10")
        image_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, image_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate fractals")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.fractal_type.bind("<<ComboboxSelected>>", self.on_fractal_type_change)
        
    def on_fractal_type_change(self, event=None):
        """Handle fractal type change"""
        if self.fractal_type.get() == "Julia":
            self.julia_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        else:
            self.julia_frame.grid_forget()
    
    def generate_fractal(self):
        """Generate the selected fractal"""
        try:
            self.status_var.set("Generating fractal...")
            self.root.update()
            
            # Update config
            self.config.max_iterations = int(self.max_iterations.get())
            self.config.zoom = self.zoom.get()
            self.config.color_scheme = self.color_scheme.get()
            
            fractal_type = self.fractal_type.get()
            
            if fractal_type == "Mandelbrot":
                self.current_generator = MandelbrotGenerator(self.config)
            elif fractal_type == "Julia":
                try:
                    real = float(self.julia_real.get())
                    imag = float(self.julia_imag.get())
                    self.config.julia_c = complex(real, imag)
                except ValueError:
                    messagebox.showerror("Error", "Invalid Julia set parameters")
                    return
                self.current_generator = JuliaGenerator(self.config)
            elif fractal_type == "Sierpinski":
                self.current_generator = SierpinskiGenerator(self.config, iterations=7)
            elif fractal_type == "Dragon Curve":
                self.current_generator = DragonCurveGenerator(self.config, iterations=15)
            
            # Generate fractal
            start_time = time.time()
            image_data = self.current_generator.generate()
            generation_time = time.time() - start_time
            
            # Display image
            self.display_image(image_data)
            
            self.status_var.set(f"Fractal generated in {generation_time:.2f} seconds")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate fractal: {str(e)}")
            self.status_var.set("Error generating fractal")
    
    def display_image(self, image_data):
        """Display image data on canvas"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(image_data)
        ax.axis('off')
        self.canvas.draw()
        self.current_image = image_data
    
    def save_image(self):
        """Save current fractal image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No fractal image to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                from PIL import Image
                img = Image.fromarray(self.current_image)
                img.save(filename)
                self.status_var.set(f"Image saved to {filename}")
            except ImportError:
                messagebox.showerror("Error", "PIL library required for saving images")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def save_config(self):
        """Save current configuration"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                config_dict = {
                    "max_iterations": self.config.max_iterations,
                    "zoom": self.config.zoom,
                    "color_scheme": self.config.color_scheme,
                    "julia_c": {"real": self.config.julia_c.real, "imag": self.config.julia_c.imag}
                }
                
                with open(filename, 'w') as f:
                    json.dump(config_dict, f, indent=2)
                
                self.status_var.set(f"Configuration saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config_dict = json.load(f)
                
                self.config.max_iterations = config_dict.get("max_iterations", 100)
                self.config.zoom = config_dict.get("zoom", 1.0)
                self.config.color_scheme = config_dict.get("color_scheme", "rainbow")
                
                if "julia_c" in config_dict:
                    julia_c = config_dict["julia_c"]
                    self.config.julia_c = complex(julia_c["real"], julia_c["imag"])
                    self.julia_real.delete(0, tk.END)
                    self.julia_real.insert(0, str(julia_c["real"]))
                    self.julia_imag.delete(0, tk.END)
                    self.julia_imag.insert(0, str(julia_c["imag"]))
                
                # Update UI
                self.max_iterations.set(self.config.max_iterations)
                self.zoom.set(self.config.zoom)
                self.color_scheme.set(self.config.color_scheme)
                
                self.status_var.set(f"Configuration loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main function to run the fractal generator"""
    print("Advanced Fractal Generator Suite")
    print("=" * 40)
    print("Choose interface:")
    print("1. GUI Interface (Recommended)")
    print("2. Command Line Interface")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        gui = FractalGUI()
        gui.run()
    elif choice == "2":
        # Simple CLI interface
        config = FractalConfig()
        print("Generating Mandelbrot set with default settings...")
        
        generator = MandelbrotGenerator(config)
        image_data = generator.generate()
        
        print("Fractal generated successfully!")
        print("Use GUI interface to view and save the fractal.")
    else:
        print("Invalid choice. Starting GUI...")
        gui = FractalGUI()
        gui.run()


if __name__ == "__main__":
    main()
