"""
Machine Learning Pattern Recognition Module
Demonstrates various ML algorithms for pattern recognition and classification
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.datasets import make_classification, make_blobs, make_circles, make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans, DBSCAN
import pandas as pd
import seaborn as sns
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional
import pickle
import json


@dataclass
class MLConfig:
    """Configuration for ML experiments"""
    test_size: float = 0.3
    random_state: int = 42
    n_samples: int = 300
    n_features: int = 2
    n_clusters: int = 3
    noise: float = 0.1


class DataGenerator:
    """Generates synthetic datasets for ML demonstrations"""
    
    @staticmethod
    def generate_classification(n_samples=300, n_features=2, n_classes=2, noise=0.1):
        """Generate classification dataset"""
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_classes=n_classes,
            n_redundant=0,
            n_informative=n_features,
            n_clusters_per_class=1,
            random_state=42,
            noise=noise
        )
        return X, y
    
    @staticmethod
    def generate_blobs(n_samples=300, n_features=2, centers=3, cluster_std=1.0):
        """Generate blob dataset"""
        X, y = make_blobs(
            n_samples=n_samples,
            n_features=n_features,
            centers=centers,
            cluster_std=cluster_std,
            random_state=42
        )
        return X, y
    
    @staticmethod
    def generate_circles(n_samples=300, noise=0.1):
        """Generate concentric circles dataset"""
        X, y = make_circles(
            n_samples=n_samples,
            noise=noise,
            factor=0.5,
            random_state=42
        )
        return X, y
    
    @staticmethod
    def generate_moons(n_samples=300, noise=0.1):
        """Generate two moons dataset"""
        X, y = make_moons(
            n_samples=n_samples,
            noise=noise,
            random_state=42
        )
        return X, y
    
    @staticmethod
    def generate_spiral(n_samples=300, noise=0.1):
        """Generate spiral dataset"""
        n = n_samples // 2
        theta = np.linspace(0, 4 * np.pi, n)
        
        # First spiral
        r1 = theta + np.random.normal(0, noise, n)
        x1 = r1 * np.cos(theta)
        y1 = r1 * np.sin(theta)
        
        # Second spiral
        r2 = theta + np.random.normal(0, noise, n)
        x2 = r2 * np.cos(theta + np.pi)
        y2 = r2 * np.sin(theta + np.pi)
        
        X = np.vstack([np.column_stack([x1, y1]), np.column_stack([x2, y2])])
        y = np.hstack([np.zeros(n), np.ones(n)])
        
        return X, y


class MLModel:
    """Base class for ML models"""
    
    def __init__(self, name: str):
        self.name = name
        self.model = None
        self.accuracy = 0.0
        self.predictions = None
        self.probabilities = None
    
    def train(self, X_train, y_train):
        """Train the model"""
        raise NotImplementedError
    
    def predict(self, X_test):
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        return self.model.predict(X_test)
    
    def predict_proba(self, X_test):
        """Get prediction probabilities"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X_test)
        return None


class KNNModel(MLModel):
    """K-Nearest Neighbors classifier"""
    
    def __init__(self, n_neighbors=5):
        super().__init__(f"KNN (k={n_neighbors})")
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class SVMModel(MLModel):
    """Support Vector Machine classifier"""
    
    def __init__(self, kernel='rbf', C=1.0):
        super().__init__(f"SVM ({kernel})")
        self.model = SVC(kernel=kernel, C=C, probability=True)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class DecisionTreeModel(MLModel):
    """Decision Tree classifier"""
    
    def __init__(self, max_depth=None):
        super().__init__("Decision Tree")
        self.model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class RandomForestModel(MLModel):
    """Random Forest classifier"""
    
    def __init__(self, n_estimators=100):
        super().__init__(f"Random Forest ({n_estimators} trees)")
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class NaiveBayesModel(MLModel):
    """Gaussian Naive Bayes classifier"""
    
    def __init__(self):
        super().__init__("Naive Bayes")
        self.model = GaussianNB()
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class LogisticRegressionModel(MLModel):
    """Logistic Regression classifier"""
    
    def __init__(self):
        super().__init__("Logistic Regression")
        self.model = LogisticRegression(random_state=42)
    
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)


class KMeansClustering:
    """K-Means clustering algorithm"""
    
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.labels = None
        self.centroids = None
    
    def fit(self, X):
        """Fit the clustering model"""
        self.labels = self.model.fit_predict(X)
        self.centroids = self.model.cluster_centers_
        return self.labels


class DBSCANClustering:
    """DBSCAN clustering algorithm"""
    
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels = None
    
    def fit(self, X):
        """Fit the clustering model"""
        self.labels = self.model.fit_predict(X)
        return self.labels


class MLPatternGUI:
    """GUI for ML pattern recognition"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Machine Learning Pattern Recognition")
        self.root.geometry("1400x900")
        
        self.config = MLConfig()
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.current_models = []
        self.current_clustering = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Export Model", command=self.export_model)
        file_menu.add_command(label="Import Model", command=self.import_model)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Data generation section
        data_frame = ttk.LabelFrame(control_frame, text="Data Generation", padding="5")
        data_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(data_frame, text="Dataset Type:").grid(row=0, column=0, sticky=tk.W)
        self.dataset_type = ttk.Combobox(data_frame, values=[
            "Classification", "Blobs", "Circles", "Moons", "Spiral"
        ])
        self.dataset_type.set("Classification")
        self.dataset_type.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Label(data_frame, text="Samples:").grid(row=1, column=0, sticky=tk.W)
        self.n_samples = ttk.Entry(data_frame, width=10)
        self.n_samples.insert(0, "300")
        self.n_samples.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(data_frame, text="Noise:").grid(row=2, column=0, sticky=tk.W)
        self.noise = ttk.Entry(data_frame, width=10)
        self.noise.insert(0, "0.1")
        self.noise.grid(row=2, column=1, sticky=tk.W)
        
        ttk.Button(data_frame, text="Generate Data", command=self.generate_data).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Model selection section
        model_frame = ttk.LabelFrame(control_frame, text="Model Selection", padding="5")
        model_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.model_vars = {}
        models = ["KNN", "SVM", "Decision Tree", "Random Forest", "Naive Bayes", "Logistic Regression"]
        
        for i, model in enumerate(models):
            var = tk.BooleanVar()
            self.model_vars[model] = var
            ttk.Checkbutton(model_frame, text=model, variable=var).grid(row=i, column=0, sticky=tk.W)
        
        # Model parameters
        param_frame = ttk.LabelFrame(control_frame, text="Model Parameters", padding="5")
        param_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(param_frame, text="KNN Neighbors:").grid(row=0, column=0, sticky=tk.W)
        self.knn_neighbors = ttk.Entry(param_frame, width=10)
        self.knn_neighbors.insert(0, "5")
        self.knn_neighbors.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(param_frame, text="SVM Kernel:").grid(row=1, column=0, sticky=tk.W)
        self.svm_kernel = ttk.Combobox(param_frame, values=["linear", "rbf", "poly"], width=8)
        self.svm_kernel.set("rbf")
        self.svm_kernel.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(param_frame, text="RF Trees:").grid(row=2, column=0, sticky=tk.W)
        self.rf_trees = ttk.Entry(param_frame, width=10)
        self.rf_trees.insert(0, "100")
        self.rf_trees.grid(row=2, column=1, sticky=tk.W)
        
        # Clustering section
        cluster_frame = ttk.LabelFrame(control_frame, text="Clustering", padding="5")
        cluster_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.cluster_type = ttk.Combobox(cluster_frame, values=["K-Means", "DBSCAN"])
        self.cluster_type.set("K-Means")
        self.cluster_type.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(cluster_frame, text="Clusters:").grid(row=1, column=0, sticky=tk.W)
        self.n_clusters = ttk.Entry(cluster_frame, width=10)
        self.n_clusters.insert(0, "3")
        self.n_clusters.grid(row=1, column=1, sticky=tk.W)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="Train Models", command=self.train_models).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Run Clustering", command=self.run_clustering).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Compare Models", command=self.compare_models).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=1, column=0, columnspan=3, pady=5)
        
        # Right panel - Visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate data and train models")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
    
    def generate_data(self):
        """Generate synthetic dataset"""
        try:
            dataset_type = self.dataset_type.get()
            n_samples = int(self.n_samples.get())
            noise = float(self.noise.get())
            
            self.status_var.set(f"Generating {dataset_type} dataset...")
            self.root.update()
            
            if dataset_type == "Classification":
                self.X, self.y = DataGenerator.generate_classification(n_samples=n_samples, noise=noise)
            elif dataset_type == "Blobs":
                self.X, self.y = DataGenerator.generate_blobs(n_samples=n_samples, noise=noise)
            elif dataset_type == "Circles":
                self.X, self.y = DataGenerator.generate_circles(n_samples=n_samples, noise=noise)
            elif dataset_type == "Moons":
                self.X, self.y = DataGenerator.generate_moons(n_samples=n_samples, noise=noise)
            elif dataset_type == "Spiral":
                self.X, self.y = DataGenerator.generate_spiral(n_samples=n_samples, noise=noise)
            
            # Split data
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=self.config.test_size, random_state=self.config.random_state
            )
            
            # Scale features
            scaler = StandardScaler()
            self.X_train = scaler.fit_transform(self.X_train)
            self.X_test = scaler.transform(self.X_test)
            
            self.visualize_data()
            self.status_var.set(f"Generated {dataset_type} dataset: {n_samples} samples")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate data: {str(e)}")
    
    def visualize_data(self):
        """Visualize the generated data"""
        if self.X is None:
            return
        
        self.figure.clear()
        
        # Create subplots
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)
        
        # Plot training data
        scatter1 = ax1.scatter(self.X_train[:, 0], self.X_train[:, 1], c=self.y_train, cmap='viridis', alpha=0.7)
        ax1.set_title("Training Data")
        ax1.set_xlabel("Feature 1")
        ax1.set_ylabel("Feature 2")
        plt.colorbar(scatter1, ax=ax1)
        
        # Plot test data
        scatter2 = ax2.scatter(self.X_test[:, 0], self.X_test[:, 1], c=self.y_test, cmap='viridis', alpha=0.7)
        ax2.set_title("Test Data")
        ax2.set_xlabel("Feature 1")
        ax2.set_ylabel("Feature 2")
        plt.colorbar(scatter2, ax=ax2)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def train_models(self):
        """Train selected ML models"""
        if self.X_train is None:
            messagebox.showwarning("Warning", "Please generate data first")
            return
        
        self.current_models = []
        selected_models = [name for name, var in self.model_vars.items() if var.get()]
        
        if not selected_models:
            messagebox.showwarning("Warning", "Please select at least one model")
            return
        
        try:
            self.status_var.set("Training models...")
            self.root.update()
            
            for model_name in selected_models:
                if model_name == "KNN":
                    k = int(self.knn_neighbors.get())
                    model = KNNModel(n_neighbors=k)
                elif model_name == "SVM":
                    kernel = self.svm_kernel.get()
                    model = SVMModel(kernel=kernel)
                elif model_name == "Decision Tree":
                    model = DecisionTreeModel()
                elif model_name == "Random Forest":
                    n_trees = int(self.rf_trees.get())
                    model = RandomForestModel(n_estimators=n_trees)
                elif model_name == "Naive Bayes":
                    model = NaiveBayesModel()
                elif model_name == "Logistic Regression":
                    model = LogisticRegressionModel()
                else:
                    continue
                
                # Train model
                model.train(self.X_train, self.y_train)
                
                # Make predictions
                predictions = model.predict(self.X_test)
                model.predictions = predictions
                model.accuracy = accuracy_score(self.y_test, predictions)
                
                # Get probabilities if available
                model.probabilities = model.predict_proba(self.X_test)
                
                self.current_models.append(model)
            
            self.visualize_results()
            self.status_var.set(f"Trained {len(self.current_models)} models")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to train models: {str(e)}")
    
    def run_clustering(self):
        """Run clustering algorithm"""
        if self.X is None:
            messagebox.showwarning("Warning", "Please generate data first")
            return
        
        try:
            cluster_type = self.cluster_type.get()
            n_clusters = int(self.n_clusters.get())
            
            self.status_var.set(f"Running {cluster_type} clustering...")
            self.root.update()
            
            if cluster_type == "K-Means":
                clustering = KMeansClustering(n_clusters=n_clusters)
            else:  # DBSCAN
                clustering = DBSCANClustering(eps=0.5, min_samples=5)
            
            clustering.fit(self.X)
            self.current_clustering = clustering
            
            self.visualize_clustering()
            self.status_var.set(f"Completed {cluster_type} clustering")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run clustering: {str(e)}")
    
    def visualize_results(self):
        """Visualize model results"""
        if not self.current_models:
            return
        
        n_models = len(self.current_models)
        cols = 3
        rows = (n_models + cols - 1) // cols
        
        self.figure.clear()
        
        for i, model in enumerate(self.current_models):
            ax = self.figure.add_subplot(rows, cols, i + 1)
            
            # Plot decision boundary
            self.plot_decision_boundary(ax, model, self.X_test, self.y_test)
            
            ax.set_title(f"{model.name}\nAccuracy: {model.accuracy:.3f}")
            ax.set_xlabel("Feature 1")
            ax.set_ylabel("Feature 2")
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_decision_boundary(self, ax, model, X, y):
        """Plot decision boundary for a model"""
        # Create mesh grid
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                             np.arange(y_min, y_max, 0.1))
        
        # Predict on mesh grid
        mesh_points = np.c_[xx.ravel(), yy.ravel()]
        Z = model.predict(mesh_points)
        Z = Z.reshape(xx.shape)
        
        # Plot decision boundary
        ax.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
        
        # Plot test points
        scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolors='black')
        
        # Plot misclassified points
        misclassified = y != model.predictions
        if np.any(misclassified):
            ax.scatter(X[misclassified, 0], X[misclassified, 1], 
                      c='red', marker='x', s=100, linewidths=2, label='Misclassified')
            ax.legend()
    
    def visualize_clustering(self):
        """Visualize clustering results"""
        if self.current_clustering is None:
            return
        
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        
        # Plot clusters
        unique_labels = np.unique(self.current_clustering.labels)
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_labels)))
        
        for label, color in zip(unique_labels, colors):
            if label == -1:  # Noise points for DBSCAN
                label_name = "Noise"
                marker = 'x'
            else:
                label_name = f"Cluster {label}"
                marker = 'o'
            
            mask = self.current_clustering.labels == label
            ax.scatter(self.X[mask, 0], self.X[mask, 1], 
                      c=[color], label=label_name, marker=marker, alpha=0.7)
        
        # Plot centroids for K-Means
        if hasattr(self.current_clustering, 'centroids') and self.current_clustering.centroids is not None:
            ax.scatter(self.current_clustering.centroids[:, 0], 
                      self.current_clustering.centroids[:, 1],
                      c='red', marker='*', s=200, linewidths=2, label='Centroids')
        
        ax.set_title(f"{self.cluster_type.get()} Clustering Results")
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        ax.legend()
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def compare_models(self):
        """Compare model performance"""
        if not self.current_models:
            messagebox.showwarning("Warning", "Please train models first")
            return
        
        # Create comparison window
        compare_window = tk.Toplevel(self.root)
        compare_window.title("Model Comparison")
        compare_window.geometry("600x400")
        
        # Create text widget
        text_frame = ttk.Frame(compare_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Generate comparison report
        report = "Model Comparison Report\n" + "="*50 + "\n\n"
        
        # Sort models by accuracy
        sorted_models = sorted(self.current_models, key=lambda m: m.accuracy, reverse=True)
        
        for model in sorted_models:
            report += f"{model.name}:\n"
            report += f"  Accuracy: {model.accuracy:.4f}\n"
            
            # Add classification report
            class_report = classification_report(self.y_test, model.predictions)
            report += f"  Classification Report:\n{class_report}\n"
            report += "-"*50 + "\n"
        
        # Create confusion matrix visualization
        if len(sorted_models) > 0:
            best_model = sorted_models[0]
            self.plot_confusion_matrix(best_model)
        
        text_widget.insert(tk.END, report)
        text_widget.config(state=tk.DISABLED)
    
    def plot_confusion_matrix(self, model):
        """Plot confusion matrix for the best model"""
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        cm = confusion_matrix(self.y_test, model.predictions)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title(f"Confusion Matrix - {model.name}")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def load_data(self):
        """Load data from CSV file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = pd.read_csv(filename)
                
                # Assume last column is target
                self.X = data.iloc[:, :-1].values
                self.y = data.iloc[:, -1].values
                
                # Split and scale data
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                    self.X, self.y, test_size=self.config.test_size, random_state=self.config.random_state
                )
                
                scaler = StandardScaler()
                self.X_train = scaler.fit_transform(self.X_train)
                self.X_test = scaler.transform(self.X_test)
                
                self.visualize_data()
                self.status_var.set(f"Loaded data from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_results(self):
        """Save results to file"""
        if not self.current_models:
            messagebox.showwarning("Warning", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                results = {
                    "models": [
                        {
                            "name": model.name,
                            "accuracy": model.accuracy,
                            "predictions": model.predictions.tolist() if model.predictions is not None else None
                        }
                        for model in self.current_models
                    ]
                }
                
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2)
                
                self.status_var.set(f"Results saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {str(e)}")
    
    def export_model(self):
        """Export trained model"""
        if not self.current_models:
            messagebox.showwarning("Warning", "No models to export")
            return
        
        # Select model to export
        model_names = [model.name for model in self.current_models]
        
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Model to Export")
        selection_window.geometry("300x200")
        
        ttk.Label(selection_window, text="Select Model:").pack(pady=10)
        
        model_var = tk.StringVar(value=model_names[0])
        model_combo = ttk.Combobox(selection_window, textvariable=model_var, values=model_names, state="readonly")
        model_combo.pack(pady=10)
        
        def export_selected():
            selected_name = model_var.get()
            model = next(m for m in self.current_models if m.name == selected_name)
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pkl",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            
            if filename:
                try:
                    with open(filename, 'wb') as f:
                        pickle.dump(model.model, f)
                    self.status_var.set(f"Model exported to {filename}")
                    selection_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export model: {str(e)}")
        
        ttk.Button(selection_window, text="Export", command=export_selected).pack(pady=20)
    
    def import_model(self):
        """Import trained model"""
        filename = filedialog.askopenfilename(
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'rb') as f:
                    model_data = pickle.load(f)
                
                # Create a wrapper model
                wrapper = MLModel("Imported Model")
                wrapper.model = model_data
                
                if self.X_test is not None:
                    predictions = wrapper.predict(self.X_test)
                    wrapper.predictions = predictions
                    wrapper.accuracy = accuracy_score(self.y_test, predictions)
                    wrapper.probabilities = wrapper.predict_proba(self.X_test)
                
                self.current_models.append(wrapper)
                self.status_var.set(f"Model imported from {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import model: {str(e)}")
    
    def clear_all(self):
        """Clear all data and models"""
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.current_models = []
        self.current_clustering = None
        
        self.figure.clear()
        self.canvas.draw()
        
        self.status_var.set("All data and models cleared")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to run the ML pattern recognition"""
    print("Machine Learning Pattern Recognition Suite")
    print("=" * 50)
    print("Starting interactive ML environment...")
    
    app = MLPatternGUI()
    app.run()


if __name__ == "__main__":
    main()
