"""
Advanced Graphics & Algorithms Suite - Web-Based Launcher
A modern web interface using Flask for launching all programs
"""

from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import sys
import os
import json
import threading
import time
from datetime import datetime
import importlib.util
from typing import Dict, List, Optional
import webbrowser

app = Flask(__name__)

class WebLauncher:
    """Web-based launcher for all programs"""
    
    def __init__(self):
        self.running_processes = {}
        self.program_status = {}
        
        # Program definitions
        self.programs = {
            'fractals': {
                'name': 'Advanced Fractal Generator',
                'description': 'Generate complex fractals (Mandelbrot, Julia, Sierpinski, Dragon curves)',
                'category': 'Graphics',
                'file': 'fractals.py',
                'icon': '🌀',
                'color': '#FF6B6B',
                'requirements': ['numpy', 'matplotlib', 'tkinter'],
                'difficulty': 'Advanced',
                'features': ['Real-time rendering', 'Multiple fractal types', 'Export capabilities']
            },
            'data_viz': {
                'name': 'Data Visualization Suite',
                'description': 'Interactive charts, graphs, and data analysis tools',
                'category': 'Data Science',
                'file': 'data_viz.py',
                'icon': '📊',
                'color': '#4ECDC4',
                'requirements': ['numpy', 'matplotlib', 'pandas', 'seaborn', 'tkinter'],
                'difficulty': 'Intermediate',
                'features': ['10+ chart types', 'Real-time analysis', 'Data cleaning tools']
            },
            'ml_patterns': {
                'name': 'ML Pattern Recognition',
                'description': 'Machine learning algorithms for classification and clustering',
                'category': 'Machine Learning',
                'file': 'ml_patterns.py',
                'icon': '🤖',
                'color': '#45B7D1',
                'requirements': ['numpy', 'matplotlib', 'scikit-learn', 'tkinter'],
                'difficulty': 'Advanced',
                'features': ['6+ algorithms', 'Model comparison', 'Interactive visualization']
            },
            'animations': {
                'name': 'Animation System',
                'description': 'Interactive animations with physics simulations',
                'category': 'Graphics',
                'file': 'animations.py',
                'icon': '🎮',
                'color': '#96CEB4',
                'requirements': ['pygame', 'numpy'],
                'difficulty': 'Intermediate',
                'features': ['Physics simulation', 'Particle systems', 'Real-time controls']
            },
            'config_manager': {
                'name': 'Configuration Manager',
                'description': 'Manage application settings and user preferences',
                'category': 'Utilities',
                'file': 'config_manager.py',
                'icon': '⚙️',
                'color': '#FFEAA7',
                'requirements': ['tkinter'],
                'difficulty': 'Beginner',
                'features': ['Settings persistence', 'User profiles', 'Import/Export']
            },
            'turtle': {
                'name': 'Geometric Pattern Generator',
                'description': 'Creates beautiful circular patterns using turtle graphics',
                'category': 'Graphics',
                'file': 'Turtle.py',
                'icon': '🐢',
                'color': '#DDA0DD',
                'requirements': ['turtle'],
                'difficulty': 'Beginner',
                'features': ['Customizable patterns', 'Interactive controls', 'Export options']
            },
            'snow': {
                'name': 'Snowflake Pattern Generator',
                'description': 'Creates snowflake patterns with customizable parameters',
                'category': 'Graphics',
                'file': 'snow.py',
                'icon': '❄️',
                'color': '#87CEEB',
                'requirements': ['turtle', 'random'],
                'difficulty': 'Beginner',
                'features': ['Random patterns', 'Color variations', 'Custom parameters']
            },
            'text': {
                'name': 'Text Evolution Simulator',
                'description': 'Demonstrates evolutionary algorithms through text generation',
                'category': 'Algorithms',
                'file': 'text.py',
                'icon': '🧬',
                'color': '#98D8C8',
                'requirements': ['random', 'string', 'time'],
                'difficulty': 'Intermediate',
                'features': ['Evolution visualization', 'Performance metrics', 'Configurable parameters']
            },
            'grv_styles': {
                'name': 'GRV Text Styles',
                'description': 'Display GRV in 10 different artistic styles',
                'category': 'Fun',
                'file': 'grv_styles.py',
                'icon': '🎨',
                'color': '#E91E63',
                'requirements': [],
                'difficulty': 'Beginner',
                'features': ['10 artistic styles', 'ASCII art', 'Pattern designs']
            },
            'mathstables': {
                'name': 'Multiplication Table Generator',
                'description': 'Generates customizable multiplication tables',
                'category': 'Education',
                'file': 'mathstables.py',
                'icon': '🔢',
                'color': '#F7DC6F',
                'requirements': [],
                'difficulty': 'Beginner',
                'features': ['Customizable size', 'File export', 'Formatted output']
            }
        }
        
        # Initialize status
        for key in self.programs:
            self.program_status[key] = {
                'status': 'ready',
                'last_run': None,
                'dependencies_ok': self.check_program_dependencies(self.programs[key]['requirements'])
            }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', programs=web_launcher.programs, status=web_launcher.program_status)

@app.route('/launch/<program_key>')
def launch_program(program_key):
    """Launch a program"""
    if program_key not in web_launcher.programs:
        return jsonify({'error': 'Program not found'}), 404
    
    program = web_launcher.programs[program_key]
    
    # Check dependencies
    if not web_launcher.check_program_dependencies(program['requirements']):
        return jsonify({
            'error': 'Missing dependencies',
            'missing': program['requirements']
        }), 400
    
    try:
        # Launch the program
        process = subprocess.Popen(
            [sys.executable, program['file']],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        web_launcher.running_processes[program_key] = process
        web_launcher.program_status[program_key]['status'] = 'running'
        web_launcher.program_status[program_key]['last_run'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': f'Launched {program["name"]}',
            'process_id': process.pid
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def get_status():
    """Get status of all programs"""
    # Update running process status
    for key, process in list(web_launcher.running_processes.items()):
        if process.poll() is not None:
            # Process has finished
            del web_launcher.running_processes[key]
            web_launcher.program_status[key]['status'] = 'stopped'
        else:
            web_launcher.program_status[key]['status'] = 'running'
    
    return jsonify(web_launcher.program_status)

@app.route('/stop/<program_key>')
def stop_program(program_key):
    """Stop a running program"""
    if program_key in web_launcher.running_processes:
        try:
            web_launcher.running_processes[program_key].terminate()
            del web_launcher.running_processes[program_key]
            web_launcher.program_status[program_key]['status'] = 'stopped'
            return jsonify({'success': True, 'message': 'Program stopped'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Program not running'}), 404

@app.route('/dependencies')
def check_dependencies():
    """Check all dependencies"""
    deps_status = {}
    for key, program in web_launcher.programs.items():
        deps_status[key] = {
            'ok': web_launcher.check_program_dependencies(program['requirements']),
            'missing': web_launcher.get_missing_dependencies(program['requirements'])
        }
    return jsonify(deps_status)

@app.route('/install_dependencies')
def install_dependencies():
    """Install all dependencies"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            # Update dependency status
            for key in web_launcher.programs:
                web_launcher.program_status[key]['dependencies_ok'] = web_launcher.check_program_dependencies(
                    web_launcher.programs[key]['requirements']
                )
            
            return jsonify({
                'success': True,
                'message': 'Dependencies installed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'error': 'Installation failed',
                'output': result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def check_program_dependencies(requirements: List[str]) -> bool:
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

def get_missing_dependencies(requirements: List[str]) -> List[str]:
    """Get list of missing dependencies"""
    missing = []
    for module in requirements:
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'turtle':
                import turtle
            else:
                importlib.import_module(module)
        except ImportError:
            missing.append(module)
    return missing

# Add methods to WebLauncher class
WebLauncher.check_program_dependencies = staticmethod(check_program_dependencies)
WebLauncher.get_missing_dependencies = staticmethod(get_missing_dependencies)

# Create web launcher instance
web_launcher = WebLauncher()

if __name__ == '__main__':
    # Create templates directory and HTML file
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # Create HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Graphics & Algorithms Suite</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats-bar {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-around;
            color: white;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        
        .categories {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .category {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            color: white;
        }
        
        .category h2 {
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .programs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        
        .program-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .program-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .program-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--card-color);
        }
        
        .program-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .program-name {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .program-description {
            color: #7f8c8d;
            margin-bottom: 15px;
            font-size: 0.9em;
        }
        
        .program-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.8em;
        }
        
        .difficulty {
            padding: 3px 8px;
            border-radius: 12px;
            font-weight: bold;
        }
        
        .difficulty.beginner { background: #d4edda; color: #155724; }
        .difficulty.intermediate { background: #fff3cd; color: #856404; }
        .difficulty.advanced { background: #f8d7da; color: #721c24; }
        
        .status {
            padding: 3px 8px;
            border-radius: 12px;
            font-weight: bold;
        }
        
        .status.ready { background: #d4edda; color: #155724; }
        .status.running { background: #cce5ff; color: #004085; }
        .status.stopped { background: #f8d7da; color: #721c24; }
        
        .features {
            margin-bottom: 15px;
        }
        
        .feature-tag {
            display: inline-block;
            background: #e9ecef;
            color: #495057;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.7em;
            margin: 2px;
        }
        
        .launch-btn {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .launch-btn.launch {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
        }
        
        .launch-btn.launch:hover {
            background: linear-gradient(45deg, #218838, #1ea085);
            transform: scale(1.05);
        }
        
        .launch-btn.stop {
            background: linear-gradient(45deg, #dc3545, #c82333);
            color: white;
        }
        
        .launch-btn.stop:hover {
            background: linear-gradient(45deg, #c82333, #bd2130);
        }
        
        .launch-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
            transform: scale(1);
        }
        
        .control-panel {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .control-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            background: white;
            color: #333;
        }
        
        .control-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification.success { background: #28a745; }
        .notification.error { background: #dc3545; }
        .notification.info { background: #17a2b8; }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .programs-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-bar {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Advanced Graphics & Algorithms Suite</h1>
            <p class="subtitle">Interactive Web Dashboard for Program Management</p>
        </header>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number" id="total-programs">{{ programs|length }}</div>
                <div>Total Programs</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="running-count">0</div>
                <div>Running</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="ready-count">0</div>
                <div>Ready</div>
            </div>
            <div class="stat-item">
                <div class="stat-number" id="deps-count">0</div>
                <div>Dependencies OK</div>
            </div>
        </div>
        
        <div class="control-panel">
            <button class="control-btn" onclick="checkAllDependencies()">Check Dependencies</button>
            <button class="control-btn" onclick="installAllDependencies()">Install Dependencies</button>
            <button class="control-btn" onclick="refreshStatus()">Refresh Status</button>
            <button class="control-btn" onclick="stopAllPrograms()">Stop All Programs</button>
        </div>
        
        <div class="categories">
            {% set categories = programs|groupby('category') %}
            {% for category, programs_list in categories %}
            <div class="category">
                <h2>{{ category }}</h2>
                <div class="programs-grid">
                    {% for program in programs_list %}
                    <div class="program-card" style="--card-color: {{ program.color }};">
                        <div class="program-icon">{{ program.icon }}</div>
                        <div class="program-name">{{ program.name }}</div>
                        <div class="program-description">{{ program.description }}</div>
                        
                        <div class="program-meta">
                            <span class="difficulty {{ program.difficulty.lower() }}">{{ program.difficulty }}</span>
                            <span class="status {{ status[program.key].status }}" id="status-{{ program.key }}">{{ status[program.key].status.upper() }}</span>
                        </div>
                        
                        <div class="features">
                            {% for feature in program.features %}
                            <span class="feature-tag">{{ feature }}</span>
                            {% endfor %}
                        </div>
                        
                        <button class="launch-btn" id="btn-{{ program.key }}" onclick="toggleProgram('{{ program.key }}')">
                            Launch
                        </button>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div id="notification" class="notification"></div>
    
    <script>
        let runningPrograms = new Set();
        
        function showNotification(message, type = 'info') {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type} show`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        function updateStats() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    let running = 0;
                    let ready = 0;
                    let depsOk = 0;
                    
                    for (const [key, status] of Object.entries(data)) {
                        if (status.status === 'running') {
                            running++;
                            runningPrograms.add(key);
                        } else {
                            runningPrograms.delete(key);
                        }
                        
                        if (status.status === 'ready') ready++;
                        if (status.dependencies_ok) depsOk++;
                        
                        // Update status display
                        const statusEl = document.getElementById(`status-${key}`);
                        if (statusEl) {
                            statusEl.textContent = status.status.toUpperCase();
                            statusEl.className = `status ${status.status}`;
                        }
                        
                        // Update button
                        const btn = document.getElementById(`btn-${key}`);
                        if (btn) {
                            if (status.status === 'running') {
                                btn.textContent = 'Stop';
                                btn.className = 'launch-btn stop';
                            } else {
                                btn.textContent = 'Launch';
                                btn.className = 'launch-btn launch';
                            }
                            
                            btn.disabled = !status.dependencies_ok;
                        }
                    }
                    
                    document.getElementById('running-count').textContent = running;
                    document.getElementById('ready-count').textContent = ready;
                    document.getElementById('deps-count').textContent = depsOk;
                });
        }
        
        function toggleProgram(programKey) {
            if (runningPrograms.has(programKey)) {
                stopProgram(programKey);
            } else {
                launchProgram(programKey);
            }
        }
        
        function launchProgram(programKey) {
            fetch(`/launch/${programKey}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'success');
                        updateStats();
                    } else {
                        showNotification(data.error || 'Failed to launch program', 'error');
                    }
                })
                .catch(error => {
                    showNotification('Network error', 'error');
                });
        }
        
        function stopProgram(programKey) {
            fetch(`/stop/${programKey}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message, 'info');
                        updateStats();
                    } else {
                        showNotification(data.error || 'Failed to stop program', 'error');
                    }
                })
                .catch(error => {
                    showNotification('Network error', 'error');
                });
        }
        
        function checkAllDependencies() {
            fetch('/dependencies')
                .then(response => response.json())
                .then(data => {
                    let message = 'Dependency Check:\\n\\n';
                    for (const [key, deps] of Object.entries(data)) {
                        message += `${key}: ${deps.ok ? '✓ OK' : '✗ Missing ' + deps.missing.join(', ')}\\n`;
                    }
                    showNotification('Dependency check completed', 'info');
                    updateStats();
                });
        }
        
        function installAllDependencies() {
            showNotification('Installing dependencies...', 'info');
            fetch('/install_dependencies')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification('Dependencies installed successfully!', 'success');
                        updateStats();
                    } else {
                        showNotification('Installation failed: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showNotification('Installation error', 'error');
                });
        }
        
        function refreshStatus() {
            updateStats();
            showNotification('Status refreshed', 'info');
        }
        
        function stopAllPrograms() {
            runningPrograms.forEach(programKey => {
                stopProgram(programKey);
            });
        }
        
        // Auto-refresh status every 5 seconds
        setInterval(updateStats, 5000);
        
        // Initial status update
        updateStats();
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(html_content)
    
    print("🌐 Starting Web Launcher...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔄 The web interface will auto-refresh status every 5 seconds")
    print("🎯 Click any program card to launch it instantly!")
    
    # Auto-open browser
    webbrowser.open('http://localhost:5000')
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
