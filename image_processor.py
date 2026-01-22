"""
Advanced Image Processing Suite
Professional image manipulation and analysis tools
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import json
from datetime import datetime
from typing import Tuple, List, Optional
import threading


class ImageProcessor:
    """Advanced image processing application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Image Processing Suite")
        self.root.geometry("1400x900")
        
        self.original_image = None
        self.processed_image = None
        self.image_history = []
        self.current_filter = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # File operations
        file_frame = ttk.LabelFrame(control_frame, text="File Operations", padding="5")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Open Image", command=self.open_image).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Save Image", command=self.save_image).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Save As", command=self.save_as_image).pack(fill=tk.X, pady=2)
        
        # Basic adjustments
        adjust_frame = ttk.LabelFrame(control_frame, text="Basic Adjustments", padding="5")
        adjust_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Brightness
        ttk.Label(adjust_frame, text="Brightness:").pack(anchor=tk.W)
        self.brightness_var = tk.DoubleVar(value=1.0)
        brightness_scale = ttk.Scale(adjust_frame, from_=0.1, to=3.0, variable=self.brightness_var,
                                   orient=tk.HORIZONTAL, command=self.apply_brightness)
        brightness_scale.pack(fill=tk.X, pady=2)
        
        # Contrast
        ttk.Label(adjust_frame, text="Contrast:").pack(anchor=tk.W)
        self.contrast_var = tk.DoubleVar(value=1.0)
        contrast_scale = ttk.Scale(adjust_frame, from_=0.1, to=3.0, variable=self.contrast_var,
                                 orient=tk.HORIZONTAL, command=self.apply_contrast)
        contrast_scale.pack(fill=tk.X, pady=2)
        
        # Saturation
        ttk.Label(adjust_frame, text="Saturation:").pack(anchor=tk.W)
        self.saturation_var = tk.DoubleVar(value=1.0)
        saturation_scale = ttk.Scale(adjust_frame, from_=0.0, to=2.0, variable=self.saturation_var,
                                   orient=tk.HORIZONTAL, command=self.apply_saturation)
        saturation_scale.pack(fill=tk.X, pady=2)
        
        # Filters
        filter_frame = ttk.LabelFrame(control_frame, text="Filters", padding="5")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filters = [
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Edge Detect", self.apply_edge_detect),
            ("Emboss", self.apply_emboss),
            ("Contour", self.apply_contour),
            ("Vintage", self.apply_vintage)
        ]
        
        for filter_name, filter_func in filters:
            ttk.Button(filter_frame, text=filter_name, command=filter_func).pack(fill=tk.X, pady=2)
        
        # Advanced operations
        advanced_frame = ttk.LabelFrame(control_frame, text="Advanced Operations", padding="5")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(advanced_frame, text="Histogram Equalization", command=self.histogram_equalization).pack(fill=tk.X, pady=2)
        ttk.Button(advanced_frame, text="Noise Reduction", command=self.noise_reduction).pack(fill=tk.X, pady=2)
        ttk.Button(advanced_frame, text="Resize", command=self.resize_image).pack(fill=tk.X, pady=2)
        ttk.Button(advanced_frame, text="Rotate", command=self.rotate_image).pack(fill=tk.X, pady=2)
        ttk.Button(advanced_frame, text="Crop", command=self.crop_image).pack(fill=tk.X, pady=2)
        
        # Analysis tools
        analysis_frame = ttk.LabelFrame(control_frame, text="Analysis Tools", padding="5")
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(analysis_frame, text="Show Histogram", command=self.show_histogram).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Edge Detection Analysis", command=self.edge_analysis).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Color Analysis", command=self.color_analysis).pack(fill=tk.X, pady=2)
        
        # History controls
        history_frame = ttk.LabelFrame(control_frame, text="History", padding="5")
        history_frame.pack(fill=tk.X)
        
        ttk.Button(history_frame, text="Undo", command=self.undo).pack(fill=tk.X, pady=2)
        ttk.Button(history_frame, text="Redo", command=self.redo).pack(fill=tk.X, pady=2)
        ttk.Button(history_frame, text="Reset", command=self.reset_image).pack(fill=tk.X, pady=2)
        
        # Right panel - Image display
        image_frame = ttk.LabelFrame(main_frame, text="Image Display", padding="10")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(image_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to process images")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def open_image(self):
        """Open an image file"""
        file_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                self.image_history = []
                self.display_image()
                self.status_var.set(f"Opened: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def save_image(self):
        """Save the processed image"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        # Save with original filename if available
        if hasattr(self, 'current_file_path'):
            try:
                self.processed_image.save(self.current_file_path)
                self.status_var.set(f"Saved: {os.path.basename(self.current_file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
        else:
            self.save_as_image()
    
    def save_as_image(self):
        """Save image with new filename"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.current_file_path = file_path
                self.status_var.set(f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def display_image(self):
        """Display image on canvas"""
        if self.processed_image is None:
            return
        
        # Resize image to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.display_image)
            return
        
        # Calculate scaling
        img_width, img_height = self.processed_image.size
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        display_image = self.processed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.photo = ImageTk.PhotoImage(display_image)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
    
    def save_to_history(self):
        """Save current state to history"""
        if self.processed_image is not None:
            self.image_history.append(self.processed_image.copy())
            # Limit history size
            if len(self.image_history) > 20:
                self.image_history.pop(0)
    
    def apply_brightness(self, value):
        """Apply brightness adjustment"""
        if self.original_image is None:
            return
        
        self.save_to_history()
        enhancer = ImageEnhance.Brightness(self.original_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image()
    
    def apply_contrast(self, value):
        """Apply contrast adjustment"""
        if self.original_image is None:
            return
        
        self.save_to_history()
        enhancer = ImageEnhance.Contrast(self.original_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image()
    
    def apply_saturation(self, value):
        """Apply saturation adjustment"""
        if self.original_image is None:
            return
        
        self.save_to_history()
        enhancer = ImageEnhance.Color(self.original_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image()
    
    def apply_blur(self):
        """Apply blur filter"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        self.processed_image = self.processed_image.filter(ImageFilter.BLUR)
        self.display_image()
        self.status_var.set("Applied blur filter")
    
    def apply_sharpen(self):
        """Apply sharpen filter"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        self.processed_image = self.processed_image.filter(ImageFilter.SHARPEN)
        self.display_image()
        self.status_var.set("Applied sharpen filter")
    
    def apply_edge_detect(self):
        """Apply edge detection filter"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        self.processed_image = self.processed_image.filter(ImageFilter.FIND_EDGES)
        self.display_image()
        self.status_var.set("Applied edge detection")
    
    def apply_emboss(self):
        """Apply emboss filter"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        self.processed_image = self.processed_image.filter(ImageFilter.EMBOSS)
        self.display_image()
        self.status_var.set("Applied emboss filter")
    
    def apply_contour(self):
        """Apply contour filter"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        self.processed_image = self.processed_image.filter(ImageFilter.CONTOUR)
        self.display_image()
        self.status_var.set("Applied contour filter")
    
    def apply_vintage(self):
        """Apply vintage effect"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        
        # Convert to numpy array
        img_array = np.array(self.processed_image)
        
        # Apply vintage effect
        vintage_img = img_array.copy()
        
        # Reduce blue channel, increase red channel
        vintage_img[:, :, 0] = np.minimum(255, vintage_img[:, :, 0] * 1.2)  # Red
        vintage_img[:, :, 2] = vintage_img[:, :, 2] * 0.8  # Blue
        
        # Add sepia tone
        vintage_img = cv2.transform(vintage_img, np.array([[0.393, 0.769, 0.189],
                                                           [0.349, 0.686, 0.168],
                                                           [0.272, 0.534, 0.131]]))
        
        self.processed_image = Image.fromarray(np.uint8(vintage_img))
        self.display_image()
        self.status_var.set("Applied vintage effect")
    
    def histogram_equalization(self):
        """Apply histogram equalization"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        
        # Convert to numpy array
        img_array = np.array(self.processed_image)
        
        if len(img_array.shape) == 3:  # Color image
            # Convert to YUV and equalize Y channel
            yuv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
            yuv_img[:, :, 0] = cv2.equalizeHist(yuv_img[:, :, 0])
            img_array = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2RGB)
        else:  # Grayscale
            img_array = cv2.equalizeHist(img_array)
        
        self.processed_image = Image.fromarray(img_array)
        self.display_image()
        self.status_var.set("Applied histogram equalization")
    
    def noise_reduction(self):
        """Apply noise reduction"""
        if self.processed_image is None:
            return
        
        self.save_to_history()
        
        # Convert to numpy array
        img_array = np.array(self.processed_image)
        
        # Apply bilateral filter for noise reduction
        if len(img_array.shape) == 3:
            denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
        else:
            denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
        
        self.processed_image = Image.fromarray(denoised)
        self.display_image()
        self.status_var.set("Applied noise reduction")
    
    def resize_image(self):
        """Resize image"""
        if self.processed_image is None:
            return
        
        # Create resize dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Resize Image")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="New Width:").grid(row=0, column=0, padx=10, pady=10)
        width_entry = ttk.Entry(dialog)
        width_entry.insert(0, str(self.processed_image.width))
        width_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="New Height:").grid(row=1, column=0, padx=10, pady=10)
        height_entry = ttk.Entry(dialog)
        height_entry.insert(0, str(self.processed_image.height))
        height_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def apply_resize():
            try:
                new_width = int(width_entry.get())
                new_height = int(height_entry.get())
                
                self.save_to_history()
                self.processed_image = self.processed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.display_image()
                self.status_var.set(f"Resized to {new_width}x{new_height}")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid dimensions")
        
        ttk.Button(dialog, text="Apply", command=apply_resize).grid(row=2, column=0, columnspan=2, pady=20)
    
    def rotate_image(self):
        """Rotate image"""
        if self.processed_image is None:
            return
        
        # Create rotation dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Rotate Image")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Angle (degrees):").grid(row=0, column=0, padx=10, pady=10)
        angle_entry = ttk.Entry(dialog)
        angle_entry.insert(0, "90")
        angle_entry.grid(row=0, column=1, padx=10, pady=10)
        
        def apply_rotation():
            try:
                angle = float(angle_entry.get())
                
                self.save_to_history()
                self.processed_image = self.processed_image.rotate(angle, expand=True)
                self.display_image()
                self.status_var.set(f"Rotated by {angle} degrees")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid angle")
        
        ttk.Button(dialog, text="Apply", command=apply_rotation).grid(row=1, column=0, columnspan=2, pady=20)
    
    def crop_image(self):
        """Crop image (rectangular selection)"""
        if self.processed_image is None:
            return
        
        self.status_var.set("Click and drag on image to select crop area")
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.finish_crop)
    
    def start_crop(self, event):
        """Start crop selection"""
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        self.crop_rect = self.canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y, 
            self.crop_start_x, self.crop_start_y,
            outline="red", width=2
        )
    
    def update_crop(self, event):
        """Update crop selection"""
        self.canvas.coords(self.crop_rect, 
                          self.crop_start_x, self.crop_start_y,
                          event.x, event.y)
    
    def finish_crop(self, event):
        """Finish crop selection"""
        # Get crop coordinates
        coords = self.canvas.coords(self.crop_rect)
        
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            
            # Convert to image coordinates
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_width, img_height = self.processed_image.size
            
            scale_x = img_width / canvas_width
            scale_y = img_height / canvas_height
            
            img_x1 = int(x1 * scale_x)
            img_y1 = int(y1 * scale_y)
            img_x2 = int(x2 * scale_x)
            img_y2 = int(y2 * scale_y)
            
            # Crop image
            self.save_to_history()
            self.processed_image = self.processed_image.crop((img_x1, img_y1, img_x2, img_y2))
            self.display_image()
            self.status_var.set("Image cropped")
        
        # Clean up
        self.canvas.delete(self.crop_rect)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
    
    def show_histogram(self):
        """Show image histogram"""
        if self.processed_image is None:
            return
        
        # Create histogram window
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Image Histogram")
        hist_window.geometry("800x600")
        
        # Create matplotlib figure
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        
        # Convert image to numpy array
        img_array = np.array(self.processed_image)
        
        if len(img_array.shape) == 3:  # Color image
            # RGB histograms
            colors = ['red', 'green', 'blue']
            for i, color in enumerate(colors):
                axes[0, 0].hist(img_array[:, :, i].flatten(), bins=256, color=color, alpha=0.7)
            axes[0, 0].set_title('RGB Histogram')
            axes[0, 0].set_xlabel('Pixel Value')
            axes[0, 0].set_ylabel('Frequency')
            
            # Individual channel histograms
            for i, (color, channel) in enumerate(zip(colors, ['Red', 'Green', 'Blue'])):
                if i < 3:
                    row, col = (i + 1) // 2, (i + 1) % 2
                    axes[row, col].hist(img_array[:, :, i].flatten(), bins=256, color=color, alpha=0.7)
                    axes[row, col].set_title(f'{channel} Channel')
                    axes[row, col].set_xlabel('Pixel Value')
                    axes[row, col].set_ylabel('Frequency')
        else:  # Grayscale
            axes[0, 0].hist(img_array.flatten(), bins=256, color='gray', alpha=0.7)
            axes[0, 0].set_title('Grayscale Histogram')
            axes[0, 0].set_xlabel('Pixel Value')
            axes[0, 0].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def edge_analysis(self):
        """Perform edge detection analysis"""
        if self.processed_image is None:
            return
        
        # Create analysis window
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Edge Detection Analysis")
        analysis_window.geometry("1000x800")
        
        # Convert to numpy array
        img_array = np.array(self.processed_image)
        
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply different edge detection methods
        edges_canny = cv2.Canny(gray, 100, 200)
        edges_sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=3)
        edges_laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        
        # Create matplotlib figure
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Original
        axes[0, 0].imshow(gray, cmap='gray')
        axes[0, 0].set_title('Original (Grayscale)')
        axes[0, 0].axis('off')
        
        # Canny
        axes[0, 1].imshow(edges_canny, cmap='gray')
        axes[0, 1].set_title('Canny Edge Detection')
        axes[0, 1].axis('off')
        
        # Sobel
        axes[1, 0].imshow(np.abs(edges_sobel), cmap='gray')
        axes[1, 0].set_title('Sobel Edge Detection')
        axes[1, 0].axis('off')
        
        # Laplacian
        axes[1, 1].imshow(np.abs(edges_laplacian), cmap='gray')
        axes[1, 1].set_title('Laplacian Edge Detection')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, analysis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def color_analysis(self):
        """Perform color analysis"""
        if self.processed_image is None:
            return
        
        # Create analysis window
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Color Analysis")
        analysis_window.geometry("800x600")
        
        # Convert to numpy array
        img_array = np.array(self.processed_image)
        
        if len(img_array.shape) == 3:  # Color image
            # Calculate color statistics
            mean_colors = np.mean(img_array, axis=(0, 1))
            std_colors = np.std(img_array, axis=(0, 1))
            
            # Create text widget for results
            text_widget = tk.Text(analysis_window, wrap=tk.WORD, height=20)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Display results
            results = "Color Analysis Results\n" + "="*50 + "\n\n"
            results += f"Image Size: {self.processed_image.size}\n"
            results += f"Image Mode: {self.processed_image.mode}\n\n"
            
            results += "Color Statistics:\n"
            colors = ['Red', 'Green', 'Blue']
            for i, color in enumerate(colors):
                results += f"{color}:\n"
                results += f"  Mean: {mean_colors[i]:.2f}\n"
                results += f"  Std Dev: {std_colors[i]:.2f}\n"
                results += f"  Min: {np.min(img_array[:, :, i]):.2f}\n"
                results += f"  Max: {np.max(img_array[:, :, i]):.2f}\n\n"
            
            # Dominant colors (simplified)
            pixels = img_array.reshape(-1, 3)
            unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
            top_indices = np.argsort(counts)[-5:][::-1]
            
            results += "Top 5 Dominant Colors:\n"
            for idx in top_indices:
                color = unique_colors[idx]
                hex_color = '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
                results += f"  {hex_color} - {counts[idx]} pixels ({counts[idx]/len(pixels)*100:.1f}%)\n"
            
            text_widget.insert(tk.END, results)
            text_widget.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Info", "Color analysis is only available for color images")
    
    def undo(self):
        """Undo last operation"""
        if self.image_history:
            self.processed_image = self.image_history.pop()
            self.display_image()
            self.status_var.set("Undo successful")
        else:
            self.status_var.set("Nothing to undo")
    
    def redo(self):
        """Redo operation (simplified - just reset to original)"""
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.display_image()
            self.status_var.set("Reset to original")
        else:
            self.status_var.set("No original image")
    
    def reset_image(self):
        """Reset to original image"""
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.image_history = []
            
            # Reset sliders
            self.brightness_var.set(1.0)
            self.contrast_var.set(1.0)
            self.saturation_var.set(1.0)
            
            self.display_image()
            self.status_var.set("Reset to original")
        else:
            self.status_var.set("No original image")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main function to run the image processor"""
    print("Advanced Image Processing Suite")
    print("=" * 40)
    print("Starting professional image processing application...")
    
    app = ImageProcessor()
    app.run()


if __name__ == "__main__":
    main()
