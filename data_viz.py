"""
Advanced Data Visualization Module
Creates interactive charts, graphs, and data analysis tools
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.signal import savgol_filter
import json
import csv
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import random
import math


@dataclass
class DataPoint:
    """Represents a single data point"""
    x: float
    y: float
    label: Optional[str] = None
    category: Optional[str] = None


class DataGenerator:
    """Generates sample data for visualization"""
    
    @staticmethod
    def generate_linear_data(n_points=100, slope=2, intercept=1, noise=0.5):
        """Generate linear data with noise"""
        x = np.linspace(0, 10, n_points)
        y = slope * x + intercept + np.random.normal(0, noise, n_points)
        return x, y
    
    @staticmethod
    def generate_polynomial_data(n_points=100, degree=3, noise=0.5):
        """Generate polynomial data"""
        x = np.linspace(-5, 5, n_points)
        y = sum(np.random.uniform(-2, 2) * (x ** i) for i in range(degree + 1))
        y += np.random.normal(0, noise, n_points)
        return x, y
    
    @staticmethod
    def generate_sine_data(n_points=100, frequency=1, amplitude=1, noise=0.2):
        """Generate sine wave data with noise"""
        x = np.linspace(0, 4 * np.pi, n_points)
        y = amplitude * np.sin(frequency * x) + np.random.normal(0, noise, n_points)
        return x, y
    
    @staticmethod
    def generate_cluster_data(n_clusters=3, points_per_cluster=50):
        """Generate clustered data"""
        data = []
        for i in range(n_clusters):
            center_x = np.random.uniform(-5, 5)
            center_y = np.random.uniform(-5, 5)
            cluster_data = []
            
            for _ in range(points_per_cluster):
                x = center_x + np.random.normal(0, 1)
                y = center_y + np.random.normal(0, 1)
                cluster_data.append(DataPoint(x, y, category=f"Cluster {i+1}"))
            
            data.extend(cluster_data)
        
        return data
    
    @staticmethod
    def generate_time_series_data(n_points=365, trend=0.1, seasonality=True):
        """Generate time series data with trend and seasonality"""
        dates = pd.date_range(start='2023-01-01', periods=n_points, freq='D')
        
        # Base trend
        trend_component = trend * np.arange(n_points)
        
        # Seasonal component
        seasonal_component = 0
        if seasonality:
            seasonal_component = 10 * np.sin(2 * np.pi * np.arange(n_points) / 365.25)
        
        # Random noise
        noise = np.random.normal(0, 2, n_points)
        
        # Combine components
        values = 100 + trend_component + seasonal_component + noise
        
        return dates, values


class ChartType:
    """Enumeration of available chart types"""
    LINE = "Line Chart"
    SCATTER = "Scatter Plot"
    BAR = "Bar Chart"
    HISTOGRAM = "Histogram"
    BOX_PLOT = "Box Plot"
    HEATMAP = "Heatmap"
    PIE_CHART = "Pie Chart"
    VIOLIN = "Violin Plot"
    CONTOUR = "Contour Plot"
    3D_SURFACE = "3D Surface"


class DataVisualizer:
    """Main data visualization class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Data Visualization Suite")
        self.root.geometry("1400x900")
        
        self.current_data = None
        self.current_figure = None
        self.chart_history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load CSV Data", command=self.load_csv_data)
        file_menu.add_command(label="Generate Sample Data", command=self.show_data_generator)
        file_menu.add_separator()
        file_menu.add_command(label="Save Chart", command=self.save_chart)
        file_menu.add_command(label="Export Data", command=self.export_data)
        
        # Data menu
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data", menu=data_menu)
        data_menu.add_command(label="Data Statistics", command=self.show_statistics)
        data_menu.add_command(label="Data Cleaning", command=self.show_data_cleaning)
        data_menu.add_command(label="Transform Data", command=self.show_data_transform)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Chart type selection
        ttk.Label(control_frame, text="Chart Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.chart_type = ttk.Combobox(control_frame, values=[
            ChartType.LINE, ChartType.SCATTER, ChartType.BAR, ChartType.HISTOGRAM,
            ChartType.BOX_PLOT, ChartType.HEATMAP, ChartType.PIE_CHART,
            ChartType.VIOLIN, ChartType.CONTOUR, ChartType._3D_SURFACE
        ])
        self.chart_type.set(ChartType.LINE)
        self.chart_type.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Data source
        ttk.Label(control_frame, text="Data Source:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.data_source = ttk.Label(control_frame, text="No data loaded")
        self.data_source.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Chart options
        options_frame = ttk.LabelFrame(control_frame, text="Chart Options", padding="5")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(options_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.chart_title = ttk.Entry(options_frame, width=20)
        self.chart_title.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(options_frame, text="X Label:").grid(row=1, column=0, sticky=tk.W)
        self.x_label = ttk.Entry(options_frame, width=20)
        self.x_label.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(options_frame, text="Y Label:").grid(row=2, column=0, sticky=tk.W)
        self.y_label = ttk.Entry(options_frame, width=20)
        self.y_label.grid(row=2, column=1, sticky=(tk.W, tk.E))
        
        # Color scheme
        ttk.Label(options_frame, text="Color Scheme:").grid(row=3, column=0, sticky=tk.W)
        self.color_scheme = ttk.Combobox(options_frame, values=["viridis", "plasma", "inferno", "magma", "cool", "hot", "rainbow"])
        self.color_scheme.set("viridis")
        self.color_scheme.grid(row=3, column=1, sticky=(tk.W, tk.E))
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(control_frame, text="Advanced Options", padding="5")
        advanced_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.show_grid = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="Show Grid", variable=self.show_grid).grid(row=0, column=0, sticky=tk.W)
        
        self.show_legend = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="Show Legend", variable=self.show_legend).grid(row=1, column=0, sticky=tk.W)
        
        self.smooth_data = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="Smooth Data", variable=self.smooth_data).grid(row=2, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate Chart", command=self.generate_chart).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear Chart", command=self.clear_chart).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Reset View", command=self.reset_view).grid(row=0, column=2, padx=5)
        
        # Right panel - Chart display
        chart_frame = ttk.LabelFrame(main_frame, text="Chart Display", padding="10")
        chart_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, chart_frame)
        toolbar.update()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to visualize data")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
    
    def show_data_generator(self):
        """Show data generator dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Generate Sample Data")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Data Type:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        data_type = ttk.Combobox(dialog, values=["Linear", "Polynomial", "Sine Wave", "Clusters", "Time Series"])
        data_type.set("Linear")
        data_type.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(dialog, text="Number of Points:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        n_points = ttk.Entry(dialog)
        n_points.insert(0, "100")
        n_points.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        def generate():
            try:
                n = int(n_points.get())
                dtype = data_type.get()
                
                if dtype == "Linear":
                    x, y = DataGenerator.generate_linear_data(n)
                    self.current_data = pd.DataFrame({'x': x, 'y': y})
                elif dtype == "Polynomial":
                    x, y = DataGenerator.generate_polynomial_data(n)
                    self.current_data = pd.DataFrame({'x': x, 'y': y})
                elif dtype == "Sine Wave":
                    x, y = DataGenerator.generate_sine_data(n)
                    self.current_data = pd.DataFrame({'x': x, 'y': y})
                elif dtype == "Clusters":
                    data_points = DataGenerator.generate_cluster_data()
                    self.current_data = pd.DataFrame([
                        {'x': point.x, 'y': point.y, 'category': point.category}
                        for point in data_points
                    ])
                elif dtype == "Time Series":
                    dates, values = DataGenerator.generate_time_series_data(n)
                    self.current_data = pd.DataFrame({'date': dates, 'value': values})
                
                self.data_source.config(text=f"Generated {dtype} data ({n} points)")
                self.status_var.set(f"Generated {dtype} data with {n} points")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate data: {str(e)}")
        
        ttk.Button(dialog, text="Generate", command=generate).grid(row=2, column=0, columnspan=2, pady=20)
    
    def load_csv_data(self):
        """Load data from CSV file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.current_data = pd.read_csv(filename)
                self.data_source.config(text=f"Loaded: {filename}")
                self.status_var.set(f"Loaded {len(self.current_data)} rows from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
    
    def generate_chart(self):
        """Generate the selected chart"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data available. Please load or generate data first.")
            return
        
        try:
            self.status_var.set("Generating chart...")
            self.root.update()
            
            chart_type = self.chart_type.get()
            title = self.chart_title.get() or f"{chart_type} Visualization"
            x_label = self.x_label.get() or "X Axis"
            y_label = self.y_label.get() or "Y Axis"
            
            # Clear previous chart
            self.figure.clear()
            
            # Create subplot
            ax = self.figure.add_subplot(111)
            
            # Apply color scheme
            colors = plt.cm.get_cmap(self.color_scheme.get())
            
            if chart_type == ChartType.LINE:
                self.create_line_chart(ax, title, x_label, y_label, colors)
            elif chart_type == ChartType.SCATTER:
                self.create_scatter_plot(ax, title, x_label, y_label, colors)
            elif chart_type == ChartType.BAR:
                self.create_bar_chart(ax, title, x_label, y_label, colors)
            elif chart_type == ChartType.HISTOGRAM:
                self.create_histogram(ax, title, x_label, colors)
            elif chart_type == ChartType.BOX_PLOT:
                self.create_box_plot(ax, title, colors)
            elif chart_type == ChartType.HEATMAP:
                self.create_heatmap(ax, title, colors)
            elif chart_type == ChartType.PIE_CHART:
                self.create_pie_chart(ax, title, colors)
            elif chart_type == ChartType.VIOLIN:
                self.create_violin_plot(ax, title, colors)
            elif chart_type == ChartType.CONTOUR:
                self.create_contour_plot(ax, title, x_label, y_label, colors)
            elif chart_type == ChartType._3D_SURFACE:
                self.create_3d_surface(ax, title, x_label, y_label, colors)
            
            # Apply common settings
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(self.show_grid.get())
            
            if self.show_legend.get() and hasattr(ax, 'legend_') and ax.legend_:
                ax.legend()
            
            # Adjust layout and redraw
            self.figure.tight_layout()
            self.canvas.draw()
            
            self.status_var.set(f"Generated {chart_type}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")
            self.status_var.set("Error generating chart")
    
    def create_line_chart(self, ax, title, x_label, y_label, colors):
        """Create line chart"""
        if len(self.current_data.columns) >= 2:
            x_col = self.current_data.columns[0]
            y_col = self.current_data.columns[1]
            
            x_data = self.current_data[x_col]
            y_data = self.current_data[y_col]
            
            if self.smooth_data.get():
                # Apply smoothing
                window_length = min(11, len(y_data) if len(y_data) % 2 == 1 else len(y_data) - 1)
                if window_length >= 3:
                    y_data = savgol_filter(y_data, window_length, 3)
            
            ax.plot(x_data, y_data, color=colors(0.7), linewidth=2)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
    
    def create_scatter_plot(self, ax, title, x_label, y_label, colors):
        """Create scatter plot"""
        if len(self.current_data.columns) >= 2:
            x_col = self.current_data.columns[0]
            y_col = self.current_data.columns[1]
            
            x_data = self.current_data[x_col]
            y_data = self.current_data[y_col]
            
            # Use category column if available
            if 'category' in self.current_data.columns:
                categories = self.current_data['category'].unique()
                for i, cat in enumerate(categories):
                    mask = self.current_data['category'] == cat
                    ax.scatter(x_data[mask], y_data[mask], 
                             c=[colors(i / len(categories))], label=cat, alpha=0.7)
            else:
                ax.scatter(x_data, y_data, c=colors(0.7), alpha=0.7)
            
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
    
    def create_bar_chart(self, ax, title, x_label, y_label, colors):
        """Create bar chart"""
        if len(self.current_data.columns) >= 2:
            x_col = self.current_data.columns[0]
            y_col = self.current_data.columns[1]
            
            # Group data if too many categories
            if len(self.current_data[x_col].unique()) > 20:
                data_grouped = self.current_data.groupby(x_col)[y_col].mean().head(20)
            else:
                data_grouped = self.current_data.groupby(x_col)[y_col].mean()
            
            bars = ax.bar(range(len(data_grouped)), data_grouped.values, color=colors(0.7))
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_xticks(range(len(data_grouped)))
            ax.set_xticklabels(data_grouped.index, rotation=45, ha='right')
    
    def create_histogram(self, ax, title, x_label, colors):
        """Create histogram"""
        if len(self.current_data.columns) >= 1:
            data_col = self.current_data.columns[1] if len(self.current_data.columns) > 1 else self.current_data.columns[0]
            data = self.current_data[data_col]
            
            ax.hist(data, bins=30, color=colors(0.7), alpha=0.7, edgecolor='black')
            ax.set_xlabel(x_label)
            ax.set_ylabel('Frequency')
    
    def create_box_plot(self, ax, title, colors):
        """Create box plot"""
        numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            ax.boxplot([self.current_data[col].dropna() for col in numeric_cols], 
                      labels=numeric_cols)
            ax.set_title(title)
    
    def create_heatmap(self, ax, title, colors):
        """Create heatmap"""
        numeric_data = self.current_data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            correlation = numeric_data.corr()
            im = ax.imshow(correlation, cmap=colors, aspect='auto')
            ax.set_xticks(range(len(correlation.columns)))
            ax.set_yticks(range(len(correlation.columns)))
            ax.set_xticklabels(correlation.columns, rotation=45, ha='right')
            ax.set_yticklabels(correlation.columns)
            
            # Add colorbar
            self.figure.colorbar(im, ax=ax)
    
    def create_pie_chart(self, ax, title, colors):
        """Create pie chart"""
        # Use first categorical column or create bins from numeric data
        categorical_cols = self.current_data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            data = self.current_data[categorical_cols[0]].value_counts()
        else:
            # Create bins from first numeric column
            numeric_col = self.current_data.select_dtypes(include=[np.number]).columns[0]
            data = pd.cut(self.current_data[numeric_col], bins=5).value_counts()
        
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%', colors=[colors(i/len(data)) for i in range(len(data))])
        ax.set_title(title)
    
    def create_violin_plot(self, ax, title, colors):
        """Create violin plot"""
        numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            data_to_plot = [self.current_data[col].dropna() for col in numeric_cols]
            parts = ax.violinplot(data_to_plot, positions=range(1, len(numeric_cols) + 1))
            
            # Color the violin plots
            for pc in parts['bodies']:
                pc.set_facecolor(colors(0.7))
                pc.set_alpha(0.7)
            
            ax.set_xticks(range(1, len(numeric_cols) + 1))
            ax.set_xticklabels(numeric_cols)
            ax.set_title(title)
    
    def create_contour_plot(self, ax, title, x_label, y_label, colors):
        """Create contour plot"""
        if len(self.current_data.columns) >= 2:
            x_col = self.current_data.columns[0]
            y_col = self.current_data.columns[1]
            
            x_data = self.current_data[x_col]
            y_data = self.current_data[y_col]
            
            # Create grid
            xi = np.linspace(x_data.min(), x_data.max(), 100)
            yi = np.linspace(y_data.min(), y_data.max(), 100)
            Xi, Yi = np.meshgrid(xi, yi)
            
            # Interpolate data
            from scipy.interpolate import griddata
            Zi = griddata((x_data, y_data), y_data, (Xi, Yi), method='linear')
            
            contour = ax.contourf(Xi, Yi, Zi, levels=20, cmap=colors)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            self.figure.colorbar(contour, ax=ax)
    
    def create_3d_surface(self, ax, title, x_label, y_label, colors):
        """Create 3D surface plot"""
        from mpl_toolkits.mplot3d import Axes3D
        
        # Remove current 2D axis and create 3D axis
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        
        if len(self.current_data.columns) >= 2:
            x_col = self.current_data.columns[0]
            y_col = self.current_data.columns[1]
            
            x_data = self.current_data[x_col]
            y_data = self.current_data[y_col]
            
            # Create grid
            xi = np.linspace(x_data.min(), x_data.max(), 50)
            yi = np.linspace(y_data.min(), y_data.max(), 50)
            Xi, Yi = np.meshgrid(xi, yi)
            
            # Interpolate data
            from scipy.interpolate import griddata
            Zi = griddata((x_data, y_data), y_data, (Xi, Yi), method='linear')
            
            surf = ax.plot_surface(Xi, Yi, Zi, cmap=colors, alpha=0.8)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_zlabel('Value')
            self.figure.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    def clear_chart(self):
        """Clear the current chart"""
        self.figure.clear()
        self.canvas.draw()
        self.status_var.set("Chart cleared")
    
    def reset_view(self):
        """Reset the chart view"""
        self.canvas.draw()
        self.status_var.set("View reset")
    
    def save_chart(self):
        """Save the current chart"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if filename:
            try:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                self.status_var.set(f"Chart saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save chart: {str(e)}")
    
    def export_data(self):
        """Export current data"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        
        if filename:
            try:
                if filename.endswith('.xlsx'):
                    self.current_data.to_excel(filename, index=False)
                else:
                    self.current_data.to_csv(filename, index=False)
                self.status_var.set(f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def show_statistics(self):
        """Show data statistics"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data available")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Data Statistics")
        stats_window.geometry("600x400")
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(stats_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate statistics
        stats_text = "Data Statistics\n" + "="*50 + "\n\n"
        stats_text += f"Dataset Shape: {self.current_data.shape}\n"
        stats_text += f"Memory Usage: {self.current_data.memory_usage(deep=True).sum() / 1024:.2f} KB\n\n"
        
        # Column statistics
        stats_text += "Column Information:\n" + "-"*30 + "\n"
        for col in self.current_data.columns:
            stats_text += f"\n{col}:\n"
            stats_text += f"  Type: {self.current_data[col].dtype}\n"
            stats_text += f"  Non-null: {self.current_data[col].count()}/{len(self.current_data)}\n"
            
            if self.current_data[col].dtype in ['int64', 'float64']:
                stats_text += f"  Mean: {self.current_data[col].mean():.2f}\n"
                stats_text += f"  Std: {self.current_data[col].std():.2f}\n"
                stats_text += f"  Min: {self.current_data[col].min():.2f}\n"
                stats_text += f"  Max: {self.current_data[col].max():.2f}\n"
                stats_text += f"  Median: {self.current_data[col].median():.2f}\n"
        
        # Correlation matrix for numeric columns
        numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            stats_text += "\n\nCorrelation Matrix:\n" + "-"*30 + "\n"
            corr_matrix = self.current_data[numeric_cols].corr()
            stats_text += corr_matrix.to_string()
        
        text_widget.insert(tk.END, stats_text)
        text_widget.config(state=tk.DISABLED)
    
    def show_data_cleaning(self):
        """Show data cleaning options"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data available")
            return
        
        cleaning_window = tk.Toplevel(self.root)
        cleaning_window.title("Data Cleaning")
        cleaning_window.geometry("400x300")
        
        ttk.Label(cleaning_window, text="Data Cleaning Options", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Show current data info
        info_text = f"Current shape: {self.current_data.shape}\n"
        info_text += f"Missing values: {self.current_data.isnull().sum().sum()}\n"
        info_text += f"Duplicate rows: {self.current_data.duplicated().sum()}"
        
        ttk.Label(cleaning_window, text=info_text).pack(pady=10)
        
        def remove_duplicates():
            self.current_data = self.current_data.drop_duplicates()
            self.data_source.config(text=f"Data cleaned (duplicates removed)")
            cleaning_window.destroy()
        
        def fill_missing():
            for col in self.current_data.columns:
                if self.current_data[col].dtype in ['int64', 'float64']:
                    self.current_data[col].fillna(self.current_data[col].mean(), inplace=True)
                else:
                    self.current_data[col].fillna(self.current_data[col].mode()[0], inplace=True)
            self.data_source.config(text="Data cleaned (missing values filled)")
            cleaning_window.destroy()
        
        def drop_missing():
            self.current_data = self.current_data.dropna()
            self.data_source.config(text="Data cleaned (missing rows dropped)")
            cleaning_window.destroy()
        
        button_frame = ttk.Frame(cleaning_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Remove Duplicates", command=remove_duplicates).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Fill Missing", command=fill_missing).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Drop Missing", command=drop_missing).grid(row=0, column=2, padx=5)
    
    def show_data_transform(self):
        """Show data transformation options"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No data available")
            return
        
        transform_window = tk.Toplevel(self.root)
        transform_window.title("Data Transformation")
        transform_window.geometry("400x250")
        
        ttk.Label(transform_window, text="Select Transformation:", font=("Arial", 10, "bold")).pack(pady=10)
        
        def normalize_data():
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                min_val = self.current_data[col].min()
                max_val = self.current_data[col].max()
                if max_val != min_val:
                    self.current_data[col] = (self.current_data[col] - min_val) / (max_val - min_val)
            self.data_source.config(text="Data normalized (0-1 scale)")
            transform_window.destroy()
        
        def standardize_data():
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                mean_val = self.current_data[col].mean()
                std_val = self.current_data[col].std()
                if std_val != 0:
                    self.current_data[col] = (self.current_data[col] - mean_val) / std_val
            self.data_source.config(text="Data standardized (z-score)")
            transform_window.destroy()
        
        def log_transform():
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if (self.current_data[col] > 0).all():
                    self.current_data[col] = np.log(self.current_data[col])
            self.data_source.config(text="Log transformation applied")
            transform_window.destroy()
        
        button_frame = ttk.Frame(transform_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Normalize (0-1)", command=normalize_data).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Standardize", command=standardize_data).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Log Transform", command=log_transform).grid(row=0, column=2, padx=5)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to run the data visualizer"""
    print("Advanced Data Visualization Suite")
    print("=" * 40)
    print("Starting interactive visualization environment...")
    
    visualizer = DataVisualizer()
    visualizer.run()


if __name__ == "__main__":
    main()
