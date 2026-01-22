"""
Network Traffic Analyzer
Real-time network monitoring and analysis tool
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import socket
import threading
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from collections import deque
import json
import os


class NetworkAnalyzer:
    """Network traffic monitoring and analysis application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Traffic Analyzer")
        self.root.geometry("1400x900")
        
        # Data storage
        self.network_data = {
            'timestamps': deque(maxlen=100),
            'bytes_sent': deque(maxlen=100),
            'bytes_recv': deque(maxlen=100),
            'packets_sent': deque(maxlen=100),
            'packets_recv': deque(maxlen=100)
        }
        
        self.connection_history = deque(maxlen=50)
        self.process_network_data = deque(maxlen=20)
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        
        self.setup_ui()
        self.start_monitoring()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Real-time monitoring tab
        self.monitor_frame = ttk.Frame(notebook)
        notebook.add(self.monitor_frame, text="Real-time Monitor")
        self.setup_monitor_tab()
        
        # Connections tab
        self.connections_frame = ttk.Frame(notebook)
        notebook.add(self.connections_frame, text="Connections")
        self.setup_connections_tab()
        
        # Processes tab
        self.processes_frame = ttk.Frame(notebook)
        notebook.add(self.processes_frame, text="Network Processes")
        self.setup_processes_tab()
        
        # Analysis tab
        self.analysis_frame = ttk.Frame(notebook)
        notebook.add(self.analysis_frame, text="Analysis")
        self.setup_analysis_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to monitor network traffic")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_monitor_tab(self):
        """Setup real-time monitoring tab"""
        # Control panel
        control_frame = ttk.Frame(self.monitor_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.monitor_btn = ttk.Button(control_frame, text="Stop Monitoring", command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Clear Data", command=self.clear_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Data", command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        # Statistics display
        stats_frame = ttk.LabelFrame(self.monitor_frame, text="Current Statistics", padding="10")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create statistics labels
        self.stats_labels = {}
        stats = [
            ("Upload Speed", "0.0 KB/s"),
            ("Download Speed", "0.0 KB/s"),
            ("Total Uploaded", "0.0 MB"),
            ("Total Downloaded", "0.0 MB"),
            ("Active Connections", "0"),
            ("Monitoring Time", "00:00:00")
        ]
        
        for i, (label, value) in enumerate(stats):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(stats_frame, text=f"{label}:").grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            stats_label = ttk.Label(stats_frame, text=value, font=('Arial', 10, 'bold'))
            stats_label.grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=2)
            self.stats_labels[label] = stats_label
        
        # Create matplotlib figure for real-time graphs
        self.fig = Figure(figsize=(12, 6), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        
        self.ax1.set_title("Network Traffic (Bytes/sec)")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Bytes/sec")
        self.ax1.grid(True, alpha=0.3)
        
        self.ax2.set_title("Packet Traffic (Packets/sec)")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Packets/sec")
        self.ax2.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        
        # Embed matplotlib in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.monitor_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Start time
        self.start_time = time.time()
    
    def setup_connections_tab(self):
        """Setup connections monitoring tab"""
        # Control panel
        control_frame = ttk.Frame(self.connections_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Refresh", command=self.refresh_connections).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close Selected", command=self.close_connection).pack(side=tk.LEFT, padx=5)
        
        # Connections treeview
        columns = ('Local Address', 'Local Port', 'Remote Address', 'Remote Port', 'Status', 'PID', 'Process')
        self.connections_tree = ttk.Treeview(self.connections_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        for col in columns:
            self.connections_tree.heading(col, text=col)
            self.connections_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.connections_frame, orient=tk.VERTICAL, command=self.connections_tree.yview)
        self.connections_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.connections_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Initial refresh
        self.refresh_connections()
    
    def setup_processes_tab(self):
        """Setup network processes tab"""
        # Control panel
        control_frame = ttk.Frame(self.processes_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Refresh", command=self.refresh_processes).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Kill Process", command=self.kill_process).pack(side=tk.LEFT, padx=5)
        
        # Processes treeview
        columns = ('PID', 'Name', 'Connections', 'Bytes Sent', 'Bytes Recv', 'Status')
        self.processes_tree = ttk.Treeview(self.processes_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        for col in columns:
            self.processes_tree.heading(col, text=col)
            self.processes_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.processes_frame, orient=tk.VERTICAL, command=self.processes_tree.yview)
        self.processes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.processes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Initial refresh
        self.refresh_processes()
    
    def setup_analysis_tab(self):
        """Setup analysis tab"""
        # Control panel
        control_frame = ttk.Frame(self.analysis_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Generate Report", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
        # Analysis display
        self.analysis_text = tk.Text(self.analysis_frame, wrap=tk.WORD, height=30)
        analysis_scrollbar = ttk.Scrollbar(self.analysis_frame, orient=tk.VERTICAL, command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=analysis_scrollbar.set)
        
        self.analysis_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        analysis_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
    
    def start_monitoring(self):
        """Start network monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_network, daemon=True)
        self.monitor_thread.start()
        
        # Start GUI update
        self.update_display()
    
    def toggle_monitoring(self):
        """Toggle monitoring state"""
        if self.monitoring:
            self.monitoring = False
            self.monitor_btn.config(text="Start Monitoring")
            self.status_var.set("Monitoring stopped")
        else:
            self.monitoring = True
            self.start_time = time.time()
            self.monitor_thread = threading.Thread(target=self.monitor_network, daemon=True)
            self.monitor_thread.start()
            self.monitor_btn.config(text="Stop Monitoring")
            self.status_var.set("Monitoring started")
    
    def monitor_network(self):
        """Monitor network traffic in background"""
        last_stats = psutil.net_io_counters()
        last_time = time.time()
        
        while self.monitoring:
            try:
                # Get current network stats
                current_stats = psutil.net_io_counters()
                current_time = time.time()
                
                # Calculate rates
                time_delta = current_time - last_time
                if time_delta > 0:
                    bytes_sent_rate = (current_stats.bytes_sent - last_stats.bytes_sent) / time_delta
                    bytes_recv_rate = (current_stats.bytes_recv - last_stats.bytes_recv) / time_delta
                    packets_sent_rate = (current_stats.packets_sent - last_stats.packets_sent) / time_delta
                    packets_recv_rate = (current_stats.packets_recv - last_stats.packets_recv) / time_delta
                    
                    # Store data
                    self.network_data['timestamps'].append(current_time)
                    self.network_data['bytes_sent'].append(bytes_sent_rate)
                    self.network_data['bytes_recv'].append(bytes_recv_rate)
                    self.network_data['packets_sent'].append(packets_sent_rate)
                    self.network_data['packets_recv'].append(packets_recv_rate)
                
                last_stats = current_stats
                last_time = current_time
                
                # Update connection history periodically
                if len(self.connection_history) == 0 or time.time() - self.connection_history[-1]['time'] > 5:
                    connections = psutil.net_connections()
                    self.connection_history.append({
                        'time': time.time(),
                        'count': len(connections)
                    })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(1)
    
    def update_display(self):
        """Update the display with current data"""
        if self.monitoring:
            # Update statistics
            self.update_statistics()
            
            # Update graphs
            self.update_graphs()
            
            # Schedule next update
            self.root.after(1000, self.update_display)
    
    def update_statistics(self):
        """Update statistics display"""
        if len(self.network_data['bytes_sent']) > 0:
            # Current rates
            current_upload = self.network_data['bytes_sent'][-1]
            current_download = self.network_data['bytes_recv'][-1]
            
            # Total bytes
            total_stats = psutil.net_io_counters()
            total_uploaded = total_stats.bytes_sent / (1024 * 1024)  # MB
            total_downloaded = total_stats.bytes_recv / (1024 * 1024)  # MB
            
            # Active connections
            active_connections = len(psutil.net_connections())
            
            # Monitoring time
            elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            
            # Update labels
            self.stats_labels["Upload Speed"].config(text=f"{current_upload/1024:.1f} KB/s")
            self.stats_labels["Download Speed"].config(text=f"{current_download/1024:.1f} KB/s")
            self.stats_labels["Total Uploaded"].config(text=f"{total_uploaded:.1f} MB")
            self.stats_labels["Total Downloaded"].config(text=f"{total_downloaded:.1f} MB")
            self.stats_labels["Active Connections"].config(text=str(active_connections))
            self.stats_labels["Monitoring Time"].config(text=time_str)
    
    def update_graphs(self):
        """Update real-time graphs"""
        if len(self.network_data['timestamps']) > 1:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Convert timestamps to relative time
            timestamps = list(self.network_data['timestamps'])
            if timestamps:
                base_time = timestamps[0]
                relative_times = [(t - base_time) for t in timestamps]
                
                # Plot bytes traffic
                self.ax1.plot(relative_times, list(self.network_data['bytes_sent']), 'b-', label='Upload', linewidth=2)
                self.ax1.plot(relative_times, list(self.network_data['bytes_recv']), 'r-', label='Download', linewidth=2)
                self.ax1.set_title("Network Traffic (Bytes/sec)")
                self.ax1.set_xlabel("Time (seconds)")
                self.ax1.set_ylabel("Bytes/sec")
                self.ax1.legend()
                self.ax1.grid(True, alpha=0.3)
                
                # Plot packet traffic
                self.ax2.plot(relative_times, list(self.network_data['packets_sent']), 'g-', label='Upload', linewidth=2)
                self.ax2.plot(relative_times, list(self.network_data['packets_recv']), 'm-', label='Download', linewidth=2)
                self.ax2.set_title("Packet Traffic (Packets/sec)")
                self.ax2.set_xlabel("Time (seconds)")
                self.ax2.set_ylabel("Packets/sec")
                self.ax2.legend()
                self.ax2.grid(True, alpha=0.3)
                
                # Redraw canvas
                self.canvas.draw()
    
    def refresh_connections(self):
        """Refresh connections list"""
        # Clear existing items
        for item in self.connections_tree.get_children():
            self.connections_tree.delete(item)
        
        try:
            connections = psutil.net_connections()
            
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    
                    # Get process name
                    try:
                        process = psutil.Process(conn.pid) if conn.pid else None
                        process_name = process.name() if process else "Unknown"
                    except:
                        process_name = "Unknown"
                    
                    self.connections_tree.insert('', 'end', values=(
                        conn.laddr.ip if conn.laddr else "N/A",
                        conn.laddr.port if conn.laddr else "N/A",
                        conn.raddr.ip if conn.raddr else "N/A",
                        conn.raddr.port if conn.raddr else "N/A",
                        conn.status,
                        conn.pid if conn.pid else "N/A",
                        process_name
                    ))
            
            self.status_var.set(f"Found {len(connections)} connections")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh connections: {str(e)}")
    
    def refresh_processes(self):
        """Refresh network processes list"""
        # Clear existing items
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
        
        try:
            # Get all processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Get network connections for this process
                    connections = proc.connections()
                    network_connections = [conn for conn in connections if conn.status == 'ESTABLISHED']
                    
                    if network_connections:
                        # Calculate network usage
                        bytes_sent = sum(conn.raddr.port if conn.raddr else 0 for conn in network_connections)
                        bytes_recv = sum(conn.laddr.port if conn.laddr else 0 for conn in network_connections)
                        
                        self.processes_tree.insert('', 'end', values=(
                            proc.info['pid'],
                            proc.info['name'],
                            len(network_connections),
                            f"{bytes_sent} B",
                            f"{bytes_recv} B",
                            "Active" if proc.is_running() else "Inactive"
                        ))
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.status_var.set("Process list refreshed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh processes: {str(e)}")
    
    def close_connection(self):
        """Close selected connection"""
        selection = self.connections_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a connection to close")
            return
        
        # Note: psutil doesn't provide a direct way to close connections
        # This would require system-level operations
        messagebox.showinfo("Info", "Connection closing requires system-level privileges")
    
    def kill_process(self):
        """Kill selected process"""
        selection = self.processes_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to kill")
            return
        
        item = self.processes_tree.item(selection[0])
        pid = int(item['values'][0])
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to kill process {pid}?"):
            try:
                proc = psutil.Process(pid)
                proc.kill()
                self.refresh_processes()
                self.status_var.set(f"Process {pid} killed")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to kill process: {str(e)}")
    
    def generate_report(self):
        """Generate network analysis report"""
        self.analysis_text.delete(1.0, tk.END)
        
        report = "Network Traffic Analysis Report\n"
        report += "=" * 50 + "\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Overall statistics
        total_stats = psutil.net_io_counters()
        report += "Overall Statistics:\n"
        report += f"  Total Bytes Sent: {total_stats.bytes_sent:,}\n"
        report += f"  Total Bytes Received: {total_stats.bytes_recv:,}\n"
        report += f"  Total Packets Sent: {total_stats.packets_sent:,}\n"
        report += f"  Total Packets Received: {total_stats.packets_recv:,}\n"
        report += f"  Packet Drop In: {total_stats.dropin:,}\n"
        report += f"  Packet Drop Out: {total_stats.dropout:,}\n"
        report += f"  Err In: {total_stats.errin:,}\n"
        report += f"  Err Out: {total_stats.errout:,}\n\n"
        
        # Current rates
        if len(self.network_data['bytes_sent']) > 0:
            avg_upload = np.mean(list(self.network_data['bytes_sent']))
            avg_download = np.mean(list(self.network_data['bytes_recv']))
            max_upload = np.max(list(self.network_data['bytes_sent']))
            max_download = np.max(list(self.network_data['bytes_recv']))
            
            report += "Traffic Rates (last 100 seconds):\n"
            report += f"  Average Upload: {avg_upload/1024:.1f} KB/s\n"
            report += f"  Average Download: {avg_download/1024:.1f} KB/s\n"
            report += f"  Peak Upload: {max_upload/1024:.1f} KB/s\n"
            report += f"  Peak Download: {max_download/1024:.1f} KB/s\n\n"
        
        # Connection statistics
        connections = psutil.net_connections()
        established = len([c for c in connections if c.status == 'ESTABLISHED'])
        listening = len([c for c in connections if c.status == 'LISTEN'])
        
        report += "Connection Statistics:\n"
        report += f"  Total Connections: {len(connections)}\n"
        report += f"  Established: {established}\n"
        report += f"  Listening: {listening}\n"
        report += f"  Other States: {len(connections) - established - listening}\n\n"
        
        # Network interfaces
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        report += "Network Interfaces:\n"
        for interface_name, addresses in net_if_addrs.items():
            if interface_name in net_if_stats:
                stats = net_if_stats[interface_name]
                report += f"  {interface_name}:\n"
                report += f"    Status: {'Up' if stats.isup else 'Down'}\n"
                report += f"    Speed: {stats.speed} Mbps\n"
                report += f"    MTU: {stats.mtu}\n"
                
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        report += f"    IPv4: {addr.address}\n"
                    elif addr.family == socket.AF_INET6:
                        report += f"    IPv6: {addr.address}\n"
                report += "\n"
        
        self.analysis_text.insert(tk.END, report)
        self.status_var.set("Report generated")
    
    def clear_data(self):
        """Clear monitoring data"""
        for key in self.network_data:
            self.network_data[key].clear()
        
        self.start_time = time.time()
        self.update_graphs()
        self.status_var.set("Data cleared")
    
    def clear_history(self):
        """Clear analysis history"""
        self.connection_history.clear()
        self.process_network_data.clear()
        self.analysis_text.delete(1.0, tk.END)
        self.status_var.set("History cleared")
    
    def export_data(self):
        """Export monitoring data to file"""
        if len(self.network_data['timestamps']) == 0:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = f"network_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            export_data = {
                'timestamps': list(self.network_data['timestamps']),
                'bytes_sent': list(self.network_data['bytes_sent']),
                'bytes_recv': list(self.network_data['bytes_recv']),
                'packets_sent': list(self.network_data['packets_sent']),
                'packets_recv': list(self.network_data['packets_recv']),
                'export_time': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.status_var.set(f"Data exported to {filename}")
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


def main():
    """Main function to run the network analyzer"""
    print("Network Traffic Analyzer")
    print("=" * 30)
    print("Starting network monitoring application...")
    
    try:
        app = NetworkAnalyzer()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
