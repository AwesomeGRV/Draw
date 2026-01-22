"""
Folder Organizer Tool
Automatically organize files in folders based on file types, dates, and custom rules
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
import mimetypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import Dict, List, Tuple, Optional
import threading


class FolderOrganizer:
    """Advanced folder organization tool with multiple organizing strategies"""
    
    def __init__(self):
        self.settings_file = "folder_organizer_settings.json"
        self.log_file = "folder_organizer_log.txt"
        
        # Default organization rules
        self.default_rules = {
            'by_type': {
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs'],
                'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
                'Ebooks': ['.epub', '.mobi', '.azw', '.azw3'],
                'Fonts': ['.ttf', '.otf', '.woff', '.woff2'],
                'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
                'Presentations': ['.ppt', '.pptx', '.odp'],
                'PDFs': ['.pdf'],
                'Text': ['.txt', '.md', '.rst'],
                'Others': []
            },
            'by_date': {
                'Today': 0,
                'Yesterday': 1,
                'This Week': 7,
                'Last Week': 14,
                'This Month': 30,
                'Last Month': 60,
                'This Year': 365,
                'Older': 99999
            },
            'by_size': {
                'Small (< 1MB)': 0,
                'Medium (1-10MB)': 1,
                'Large (10-100MB)': 10,
                'Very Large (> 100MB)': 100
            }
        }
        
        self.load_settings()
        self.operation_log = []
        
    def load_settings(self):
        """Load organizer settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.custom_rules = settings.get('custom_rules', {})
                    self.default_folder = settings.get('default_folder', os.path.expanduser("~/Downloads"))
                    self.create_subfolders = settings.get('create_subfolders', True)
                    self.duplicate_action = settings.get('duplicate_action', 'skip')
            else:
                self.custom_rules = {}
                self.default_folder = os.path.expanduser("~/Downloads")
                self.create_subfolders = True
                self.duplicate_action = 'skip'
        except Exception:
            self.custom_rules = {}
            self.default_folder = os.path.expanduser("~/Downloads")
            self.create_subfolders = True
            self.duplicate_action = 'skip'
    
    def save_settings(self):
        """Save organizer settings"""
        try:
            settings = {
                'custom_rules': self.custom_rules,
                'default_folder': self.default_folder,
                'create_subfolders': self.create_subfolders,
                'duplicate_action': self.duplicate_action,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            self.log_message(f"Could not save settings: {e}")
    
    def log_message(self, message: str):
        """Log operation message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.operation_log.append(log_entry)
        
        # Also write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception:
            pass
    
    def get_file_category(self, file_path: str, rules: Dict) -> str:
        """Determine file category based on rules"""
        file_ext = Path(file_path).suffix.lower()
        
        for category, extensions in rules.items():
            if isinstance(extensions, list):
                if file_ext in extensions:
                    return category
            elif isinstance(extensions, dict):
                # For size/date rules
                continue
        
        return 'Others'
    
    def get_date_category(self, file_path: str, rules: Dict) -> str:
        """Determine file category based on modification date"""
        try:
            file_mtime = os.path.getmtime(file_path)
            file_date = datetime.fromtimestamp(file_mtime)
            days_old = (datetime.now() - file_date).days
            
            for category, days in rules.items():
                if days_old <= days:
                    return category
            
            return 'Older'
        except Exception:
            return 'Unknown'
    
    def get_size_category(self, file_path: str, rules: Dict) -> str:
        """Determine file category based on file size"""
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
            
            for category, size_mb in rules.items():
                if file_size_mb <= size_mb:
                    return category
            
            return 'Very Large (> 100MB)'
        except Exception:
            return 'Unknown'
    
    def organize_by_type(self, source_folder: str, target_folder: str, rules: Dict = None) -> Dict:
        """Organize files by type"""
        if rules is None:
            rules = self.default_rules['by_type']
        
        results = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'categories': {}
        }
        
        self.log_message(f"Starting organization by type in: {source_folder}")
        
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    category = self.get_file_category(file_path, rules)
                    target_dir = os.path.join(target_folder, category)
                    
                    # Create target directory if needed
                    if self.create_subfolders and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        self.log_message(f"Created directory: {target_dir}")
                    
                    # Move file
                    target_path = os.path.join(target_dir, file)
                    
                    if os.path.exists(target_path):
                        # Handle duplicates
                        if self.duplicate_action == 'skip':
                            self.log_message(f"Skipped duplicate: {file}")
                            results['skipped'] += 1
                            continue
                        elif self.duplicate_action == 'rename':
                            counter = 1
                            while os.path.exists(target_path):
                                name, ext = os.path.splitext(file)
                                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                                counter += 1
                        elif self.duplicate_action == 'replace':
                            os.remove(target_path)
                    
                    shutil.move(file_path, target_path)
                    self.log_message(f"Moved: {file} -> {category}/{file}")
                    results['moved'] += 1
                    
                    # Update category stats
                    if category not in results['categories']:
                        results['categories'][category] = 0
                    results['categories'][category] += 1
                    
                except Exception as e:
                    self.log_message(f"Error processing {file}: {e}")
                    results['errors'] += 1
        
        self.log_message(f"Organization complete. Moved: {results['moved']}, Skipped: {results['skipped']}, Errors: {results['errors']}")
        return results
    
    def organize_by_date(self, source_folder: str, target_folder: str) -> Dict:
        """Organize files by modification date"""
        results = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'categories': {}
        }
        
        self.log_message(f"Starting organization by date in: {source_folder}")
        
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    category = self.get_date_category(file_path, self.default_rules['by_date'])
                    target_dir = os.path.join(target_folder, category)
                    
                    # Create target directory if needed
                    if self.create_subfolders and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        self.log_message(f"Created directory: {target_dir}")
                    
                    # Move file
                    target_path = os.path.join(target_dir, file)
                    
                    if os.path.exists(target_path):
                        if self.duplicate_action == 'skip':
                            results['skipped'] += 1
                            continue
                        elif self.duplicate_action == 'rename':
                            counter = 1
                            while os.path.exists(target_path):
                                name, ext = os.path.splitext(file)
                                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                                counter += 1
                        elif self.duplicate_action == 'replace':
                            os.remove(target_path)
                    
                    shutil.move(file_path, target_path)
                    self.log_message(f"Moved: {file} -> {category}/{file}")
                    results['moved'] += 1
                    
                    # Update category stats
                    if category not in results['categories']:
                        results['categories'][category] = 0
                    results['categories'][category] += 1
                    
                except Exception as e:
                    self.log_message(f"Error processing {file}: {e}")
                    results['errors'] += 1
        
        self.log_message(f"Date organization complete. Moved: {results['moved']}, Skipped: {results['skipped']}, Errors: {results['errors']}")
        return results
    
    def organize_by_size(self, source_folder: str, target_folder: str) -> Dict:
        """Organize files by size"""
        results = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'categories': {}
        }
        
        self.log_message(f"Starting organization by size in: {source_folder}")
        
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    category = self.get_size_category(file_path, self.default_rules['by_size'])
                    target_dir = os.path.join(target_folder, category)
                    
                    # Create target directory if needed
                    if self.create_subfolders and not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                        self.log_message(f"Created directory: {target_dir}")
                    
                    # Move file
                    target_path = os.path.join(target_dir, file)
                    
                    if os.path.exists(target_path):
                        if self.duplicate_action == 'skip':
                            results['skipped'] += 1
                            continue
                        elif self.duplicate_action == 'rename':
                            counter = 1
                            while os.path.exists(target_path):
                                name, ext = os.path.splitext(file)
                                target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                                counter += 1
                        elif self.duplicate_action == 'replace':
                            os.remove(target_path)
                    
                    shutil.move(file_path, target_path)
                    self.log_message(f"Moved: {file} -> {category}/{file}")
                    results['moved'] += 1
                    
                    # Update category stats
                    if category not in results['categories']:
                        results['categories'][category] = 0
                    results['categories'][category] += 1
                    
                except Exception as e:
                    self.log_message(f"Error processing {file}: {e}")
                    results['errors'] += 1
        
        self.log_message(f"Size organization complete. Moved: {results['moved']}, Skipped: {results['skipped']}, Errors: {results['errors']}")
        return results
    
    def analyze_folder(self, folder_path: str) -> Dict:
        """Analyze folder contents and return statistics"""
        analysis = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'size_distribution': {},
            'date_distribution': {},
            'largest_files': []
        }
        
        self.log_message(f"Analyzing folder: {folder_path}")
        
        file_sizes = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    # File size
                    file_size = os.path.getsize(file_path)
                    analysis['total_files'] += 1
                    analysis['total_size'] += file_size
                    file_sizes.append((file_path, file_size))
                    
                    # File type
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext not in analysis['file_types']:
                        analysis['file_types'][file_ext] = {'count': 0, 'size': 0}
                    analysis['file_types'][file_ext]['count'] += 1
                    analysis['file_types'][file_ext]['size'] += file_size
                    
                    # Size distribution
                    size_mb = file_size / (1024 * 1024)
                    if size_mb < 1:
                        size_cat = 'Small (< 1MB)'
                    elif size_mb < 10:
                        size_cat = 'Medium (1-10MB)'
                    elif size_mb < 100:
                        size_cat = 'Large (10-100MB)'
                    else:
                        size_cat = 'Very Large (> 100MB)'
                    
                    if size_cat not in analysis['size_distribution']:
                        analysis['size_distribution'][size_cat] = 0
                    analysis['size_distribution'][size_cat] += 1
                    
                    # Date distribution
                    file_mtime = os.path.getmtime(file_path)
                    file_date = datetime.fromtimestamp(file_mtime)
                    days_old = (datetime.now() - file_date).days
                    
                    if days_old <= 1:
                        date_cat = 'Today'
                    elif days_old <= 7:
                        date_cat = 'This Week'
                    elif days_old <= 30:
                        date_cat = 'This Month'
                    elif days_old <= 365:
                        date_cat = 'This Year'
                    else:
                        date_cat = 'Older'
                    
                    if date_cat not in analysis['date_distribution']:
                        analysis['date_distribution'][date_cat] = 0
                    analysis['date_distribution'][date_cat] += 1
                    
                except Exception as e:
                    self.log_message(f"Error analyzing {file}: {e}")
        
        # Get largest files
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        analysis['largest_files'] = file_sizes[:10]
        
        self.log_message(f"Analysis complete: {analysis['total_files']} files, {analysis['total_size'] / (1024*1024):.1f} MB total")
        return analysis
    
    def run_gui(self):
        """Run the GUI version of the folder organizer"""
        root = tk.Tk()
        root.title("Folder Organizer")
        root.geometry("900x700")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source folder selection
        source_frame = ttk.LabelFrame(main_frame, text="Source Folder", padding="5")
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.source_folder_var = tk.StringVar(value=self.default_folder)
        ttk.Entry(source_frame, textvariable=self.source_folder_var, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(source_frame, text="Browse", command=self.browse_source).pack(side=tk.LEFT)
        
        # Target folder selection
        target_frame = ttk.LabelFrame(main_frame, text="Target Folder", padding="5")
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.target_folder_var = tk.StringVar(value=os.path.join(self.default_folder, "Organized"))
        ttk.Entry(target_frame, textvariable=self.target_folder_var, width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(target_frame, text="Browse", command=self.browse_target).pack(side=tk.LEFT)
        
        # Organization method
        method_frame = ttk.LabelFrame(main_frame, text="Organization Method", padding="5")
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.method_var = tk.StringVar(value="by_type")
        methods = [
            ("By File Type", "by_type"),
            ("By Date", "by_date"),
            ("By Size", "by_size")
        ]
        
        for text, value in methods:
            ttk.Radiobutton(method_frame, text=text, variable=self.method_var, value=value).pack(side=tk.LEFT, padx=10)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.create_subfolders_var = tk.BooleanVar(value=self.create_subfolders)
        ttk.Checkbutton(options_frame, text="Create subfolders", variable=self.create_subfolders_var).pack(side=tk.LEFT, padx=10)
        
        # Duplicate handling
        ttk.Label(options_frame, text="Handle duplicates:").pack(side=tk.LEFT, padx=(20, 5))
        self.duplicate_var = tk.StringVar(value=self.duplicate_action)
        duplicate_combo = ttk.Combobox(options_frame, textvariable=self.duplicate_var, 
                                     values=["skip", "rename", "replace"], state="readonly", width=10)
        duplicate_combo.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="Analyze Folder", command=self.analyze_folder_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Organize Files", command=self.organize_files_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Log", command=self.view_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.progress_var).pack(pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        root.mainloop()
    
    def browse_source(self):
        """Browse for source folder"""
        folder = filedialog.askdirectory(initialdir=self.source_folder_var.get())
        if folder:
            self.source_folder_var.set(folder)
    
    def browse_target(self):
        """Browse for target folder"""
        folder = filedialog.askdirectory(initialdir=self.target_folder_var.get())
        if folder:
            self.target_folder_var.set(folder)
    
    def analyze_folder_gui(self):
        """Analyze folder in GUI"""
        source_folder = self.source_folder_var.get()
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Error", "Source folder does not exist!")
            return
        
        self.progress_var.set("Analyzing folder...")
        self.results_text.delete(1.0, tk.END)
        
        def analyze():
            try:
                analysis = self.analyze_folder(source_folder)
                
                # Display results
                self.results_text.insert(tk.END, f"📊 FOLDER ANALYSIS RESULTS\n")
                self.results_text.insert(tk.END, f"=" * 50 + "\n\n")
                self.results_text.insert(tk.END, f"📁 Folder: {source_folder}\n")
                self.results_text.insert(tk.END, f"📄 Total Files: {analysis['total_files']:,}\n")
                self.results_text.insert(tk.END, f"💾 Total Size: {analysis['total_size'] / (1024*1024):.1f} MB\n\n")
                
                # File types
                self.results_text.insert(tk.END, f"📋 FILE TYPES:\n")
                self.results_text.insert(tk.END, f"-" * 30 + "\n")
                for ext, data in sorted(analysis['file_types'].items(), key=lambda x: x[1]['count'], reverse=True):
                    self.results_text.insert(tk.END, f"{ext or 'No extension'}: {data['count']} files ({data['size'] / (1024*1024):.1f} MB)\n")
                
                # Size distribution
                self.results_text.insert(tk.END, f"\n📏 SIZE DISTRIBUTION:\n")
                self.results_text.insert(tk.END, f"-" * 30 + "\n")
                for size_cat, count in analysis['size_distribution'].items():
                    self.results_text.insert(tk.END, f"{size_cat}: {count} files\n")
                
                # Date distribution
                self.results_text.insert(tk.END, f"\n📅 DATE DISTRIBUTION:\n")
                self.results_text.insert(tk.END, f"-" * 30 + "\n")
                for date_cat, count in analysis['date_distribution'].items():
                    self.results_text.insert(tk.END, f"{date_cat}: {count} files\n")
                
                # Largest files
                if analysis['largest_files']:
                    self.results_text.insert(tk.END, f"\n🔝 LARGEST FILES:\n")
                    self.results_text.insert(tk.END, f"-" * 30 + "\n")
                    for file_path, size in analysis['largest_files'][:5]:
                        file_name = os.path.basename(file_path)
                        size_mb = size / (1024 * 1024)
                        self.results_text.insert(tk.END, f"{file_name}: {size_mb:.1f} MB\n")
                
                self.progress_var.set("Analysis complete!")
                
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Error during analysis: {e}")
                self.progress_var.set("Analysis failed!")
        
        # Run in thread to avoid GUI freezing
        threading.Thread(target=analyze, daemon=True).start()
    
    def organize_files_gui(self):
        """Organize files in GUI"""
        source_folder = self.source_folder_var.get()
        target_folder = self.target_folder_var.get()
        method = self.method_var.get()
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Error", "Source folder does not exist!")
            return
        
        if source_folder == target_folder:
            messagebox.showerror("Error", "Source and target folders cannot be the same!")
            return
        
        # Update settings
        self.create_subfolders = self.create_subfolders_var.get()
        self.duplicate_action = self.duplicate_var.get()
        self.save_settings()
        
        self.progress_var.set("Organizing files...")
        self.results_text.delete(1.0, tk.END)
        
        def organize():
            try:
                if method == "by_type":
                    results = self.organize_by_type(source_folder, target_folder)
                elif method == "by_date":
                    results = self.organize_by_date(source_folder, target_folder)
                elif method == "by_size":
                    results = self.organize_by_size(source_folder, target_folder)
                else:
                    raise ValueError("Invalid organization method")
                
                # Display results
                self.results_text.insert(tk.END, f"🗂️ ORGANIZATION RESULTS\n")
                self.results_text.insert(tk.END, f"=" * 50 + "\n\n")
                self.results_text.insert(tk.END, f"📁 Source: {source_folder}\n")
                self.results_text.insert(tk.END, f"📁 Target: {target_folder}\n")
                self.results_text.insert(tk.END, f"🔧 Method: {method.replace('_', ' ').title()}\n\n")
                self.results_text.insert(tk.END, f"📊 SUMMARY:\n")
                self.results_text.insert(tk.END, f"  ✅ Files moved: {results['moved']}\n")
                self.results_text.insert(tk.END, f"  ⏭️ Files skipped: {results['skipped']}\n")
                self.results_text.insert(tk.END, f"  ❌ Errors: {results['errors']}\n\n")
                
                if results['categories']:
                    self.results_text.insert(tk.END, f"📋 CATEGORIES:\n")
                    self.results_text.insert(tk.END, f"-" * 30 + "\n")
                    for category, count in results['categories'].items():
                        self.results_text.insert(tk.END, f"  {category}: {count} files\n")
                
                self.progress_var.set("Organization complete!")
                messagebox.showinfo("Success", f"Organization complete! Moved {results['moved']} files.")
                
            except Exception as e:
                self.results_text.insert(tk.END, f"❌ Error during organization: {e}")
                self.progress_var.set("Organization failed!")
                messagebox.showerror("Error", f"Organization failed: {e}")
        
        # Run in thread to avoid GUI freezing
        threading.Thread(target=organize, daemon=True).start()
    
    def view_log(self):
        """View operation log"""
        log_window = tk.Toplevel()
        log_window.title("Operation Log")
        log_window.geometry("600x400")
        
        log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load log content
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    log_text.insert(tk.END, log_content)
            else:
                log_text.insert(tk.END, "No log file found.")
        except Exception as e:
            log_text.insert(tk.END, f"Error reading log file: {e}")
        
        log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear operation log"""
        if messagebox.askyesno("Confirm", "Clear all operation logs?"):
            self.operation_log = []
            try:
                if os.path.exists(self.log_file):
                    os.remove(self.log_file)
                messagebox.showinfo("Success", "Log cleared!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear log: {e}")
    
    def run_cli(self):
        """Run the CLI version of the folder organizer"""
        print("🗂️ FOLDER ORGANIZER")
        print("=" * 40)
        
        while True:
            print("\nChoose an option:")
            print("1. 📊 Analyze folder")
            print("2. 🗂️ Organize by type")
            print("3. 📅 Organize by date")
            print("4. 📏 Organize by size")
            print("5. ⚙️ Settings")
            print("6. 📋 View log")
            print("7. 🚪 Exit")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                self.analyze_cli()
            elif choice == '2':
                self.organize_cli('by_type')
            elif choice == '3':
                self.organize_cli('by_date')
            elif choice == '4':
                self.organize_cli('by_size')
            elif choice == '5':
                self.settings_cli()
            elif choice == '6':
                self.view_log_cli()
            elif choice == '7':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid choice!")
    
    def analyze_cli(self):
        """Analyze folder in CLI"""
        folder = input("Enter folder path to analyze: ").strip()
        
        if not os.path.exists(folder):
            print("❌ Folder does not exist!")
            return
        
        print("\n📊 Analyzing folder...")
        analysis = self.analyze_folder(folder)
        
        print(f"\n📁 Folder: {folder}")
        print(f"📄 Total Files: {analysis['total_files']:,}")
        print(f"💾 Total Size: {analysis['total_size'] / (1024*1024):.1f} MB")
        
        print("\n📋 Top File Types:")
        for ext, data in sorted(analysis['file_types'].items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
            print(f"  {ext or 'No extension'}: {data['count']} files")
        
        input("\nPress Enter to continue...")
    
    def organize_cli(self, method: str):
        """Organize files in CLI"""
        source = input("Enter source folder: ").strip()
        target = input("Enter target folder: ").strip()
        
        if not os.path.exists(source):
            print("❌ Source folder does not exist!")
            return
        
        if source == target:
            print("❌ Source and target folders cannot be the same!")
            return
        
        print(f"\n🗂️ Organizing files by {method}...")
        
        if method == "by_type":
            results = self.organize_by_type(source, target)
        elif method == "by_date":
            results = self.organize_by_date(source, target)
        elif method == "by_size":
            results = self.organize_by_size(source, target)
        
        print(f"\n✅ Files moved: {results['moved']}")
        print(f"⏭️ Files skipped: {results['skipped']}")
        print(f"❌ Errors: {results['errors']}")
        
        input("\nPress Enter to continue...")
    
    def settings_cli(self):
        """Manage settings in CLI"""
        print("\n⚙️ SETTINGS")
        print(f"1. Default folder: {self.default_folder}")
        print(f"2. Create subfolders: {self.create_subfolders}")
        print(f"3. Duplicate action: {self.duplicate_action}")
        
        choice = input("\nChange setting (1-3) or press Enter to continue: ").strip()
        
        if choice == '1':
            new_folder = input("Enter default folder path: ").strip()
            if os.path.exists(new_folder):
                self.default_folder = new_folder
                self.save_settings()
                print("✅ Default folder updated!")
            else:
                print("❌ Folder does not exist!")
        elif choice == '2':
            self.create_subfolders = not self.create_subfolders
            self.save_settings()
            print(f"✅ Create subfolders: {self.create_subfolders}")
        elif choice == '3':
            actions = ['skip', 'rename', 'replace']
            print("Available actions: skip, rename, replace")
            new_action = input("Enter duplicate action: ").strip()
            if new_action in actions:
                self.duplicate_action = new_action
                self.save_settings()
                print(f"✅ Duplicate action updated to: {new_action}")
            else:
                print("❌ Invalid action!")
    
    def view_log_cli(self):
        """View log in CLI"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    print("\n📋 OPERATION LOG")
                    print("=" * 50)
                    print(f.read())
            else:
                print("\n📋 No log file found.")
        except Exception as e:
            print(f"❌ Error reading log: {e}")
        
        input("\nPress Enter to continue...")


def main():
    """Main function to run the folder organizer"""
    print("🗂️ FOLDER ORGANIZER")
    print("=" * 30)
    print("Advanced file organization tool")
    
    organizer = FolderOrganizer()
    
    # Choose interface
    print("Choose interface:")
    print("1. 🖥️ GUI Interface")
    print("2. 💻 CLI Interface")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        organizer.run_gui()
    else:
        organizer.run_cli()


if __name__ == "__main__":
    main()
