"""
AI Chatbot using OpenAI API
Interactive chatbot with conversation history and multiple features
"""

import openai
import json
import os
from datetime import datetime
from typing import List, Dict
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog


class OpenAIChatbot:
    """AI Chatbot with OpenAI API integration"""
    
    def __init__(self):
        self.api_key = None
        self.conversation_history = []
        self.settings_file = "chatbot_settings.json"
        self.history_file = "chatbot_history.json"
        
        # Load settings
        self.load_settings()
        self.load_history()
        
        # Predefined personas
        self.personas = {
            'assistant': "You are a helpful AI assistant. Be friendly, informative, and helpful.",
            'teacher': "You are a patient teacher. Explain concepts clearly and provide examples.",
            'creative': "You are a creative writer. Be imaginative, poetic, and inspiring.",
            'technical': "You are a technical expert. Provide detailed, accurate technical information.",
            'casual': "You are a casual conversation partner. Be friendly, relaxed, and engaging.",
            'professional': "You are a professional consultant. Be formal, precise, and business-oriented."
        }
        
        self.current_persona = 'assistant'
    
    def load_settings(self):
        """Load chatbot settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.api_key = settings.get('api_key', None)
                    self.current_persona = settings.get('persona', 'assistant')
            else:
                self.api_key = None
                self.current_persona = 'assistant'
        except Exception:
            self.api_key = None
            self.current_persona = 'assistant'
    
    def save_settings(self):
        """Save chatbot settings"""
        try:
            settings = {
                'api_key': self.api_key,
                'persona': self.current_persona,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def load_history(self):
        """Load conversation history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.conversation_history = json.load(f)
        except Exception:
            self.conversation_history = []
    
    def save_history(self):
        """Save conversation history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            print(f"Could not save history: {e}")
    
    def set_api_key(self, api_key: str):
        """Set OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        self.save_settings()
    
    def get_chat_response(self, message: str) -> str:
        """Get response from OpenAI API"""
        if not self.api_key:
            return "⚠️ Please set your OpenAI API key first. Go to Settings → API Key."
        
        try:
            # Prepare conversation context
            messages = [
                {"role": "system", "content": self.personas[self.current_persona]}
            ]
            
            # Add conversation history (last 10 messages for context)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Make API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Save to history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            self.save_history()
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.save_history()
    
    def export_history(self, filename: str):
        """Export conversation history to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Chatbot Conversation History\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Persona: {self.current_persona}\n")
                f.write("=" * 50 + "\n\n")
                
                for msg in self.conversation_history:
                    role = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
                    f.write(f"{role}:\n{msg['content']}\n\n")
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def run_gui(self):
        """Run the GUI version of the chatbot"""
        root = tk.Tk()
        root.title("AI Chatbot - OpenAI")
        root.geometry("800x600")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # API Key section
        api_frame = ttk.LabelFrame(control_frame, text="API Settings", padding="5")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text="OpenAI API Key:").pack(side=tk.LEFT)
        self.api_key_var = tk.StringVar(value=self.api_key or "")
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*", width=40)
        api_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(api_frame, text="Set Key", command=self.set_key_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(api_frame, text="Get API Key", command=self.open_api_link).pack(side=tk.LEFT)
        
        # Persona selection
        persona_frame = ttk.LabelFrame(control_frame, text="Persona", padding="5")
        persona_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.persona_var = tk.StringVar(value=self.current_persona)
        persona_combo = ttk.Combobox(persona_frame, textvariable=self.persona_var, 
                                     values=list(self.personas.keys()), state="readonly")
        persona_combo.pack(side=tk.LEFT, padx=5)
        persona_combo.bind('<<ComboboxSelected>>', self.change_persona)
        
        # Chat display
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding="5")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=15)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(input_frame, textvariable=self.message_var)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        message_entry.bind('<Return>', lambda e: self.send_message_gui())
        
        ttk.Button(input_frame, text="Send", command=self.send_message_gui).pack(side=tk.LEFT)
        
        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export History", command=self.export_history_gui)
        file_menu.add_command(label="Clear History", command=self.clear_history_gui)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Use", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Load conversation history
        self.load_conversation_gui()
        
        root.mainloop()
    
    def set_key_gui(self):
        """Set API key from GUI"""
        api_key = self.api_key_var.get().strip()
        if api_key:
            self.set_api_key(api_key)
            messagebox.showinfo("Success", "API Key set successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")
    
    def open_api_link(self):
        """Open OpenAI API key page"""
        import webbrowser
        webbrowser.open("https://platform.openai.com/api-keys")
    
    def change_persona(self, event=None):
        """Change chatbot persona"""
        self.current_persona = self.persona_var.get()
        self.save_settings()
        self.add_message_gui("System", f"Persona changed to: {self.current_persona}")
    
    def send_message_gui(self):
        """Send message from GUI"""
        message = self.message_var.get().strip()
        if not message:
            return
        
        # Add user message
        self.add_message_gui("You", message)
        self.message_var.set("")
        
        # Get AI response
        response = self.get_chat_response(message)
        self.add_message_gui("Assistant", response)
    
    def add_message_gui(self, sender: str, message: str):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}:\n", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Configure tags
        self.chat_display.tag_config("sender", font=("Arial", 10, "bold"), foreground="#2E86AB")
        self.chat_display.tag_config("message", font=("Arial", 10))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def load_conversation_gui(self):
        """Load conversation history in GUI"""
        for msg in self.conversation_history[-10:]:  # Show last 10 messages
            sender = "You" if msg['role'] == 'user' else "Assistant"
            self.add_message_gui(sender, msg['content'])
    
    def clear_history_gui(self):
        """Clear conversation history from GUI"""
        if messagebox.askyesno("Confirm", "Clear all conversation history?"):
            self.clear_history()
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Conversation history cleared!")
    
    def export_history_gui(self):
        """Export conversation history from GUI"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if self.export_history(filename):
                messagebox.showinfo("Success", f"History exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export history")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """AI Chatbot - How to Use

1. Get an OpenAI API Key:
   - Go to https://platform.openai.com/api-keys
   - Create an account and generate an API key
   - Copy the key and paste it in the API Key field

2. Set Your API Key:
   - Enter your API key in the API Key field
   - Click "Set Key" to save it

3. Choose a Persona:
   - Assistant: Helpful and informative
   - Teacher: Patient and educational
   - Creative: Imaginative and inspiring
   - Technical: Detailed and accurate
   - Casual: Friendly and relaxed
   - Professional: Formal and business-oriented

4. Start Chatting:
   - Type your message in the input field
   - Press Enter or click "Send"
   - The AI will respond based on the selected persona

5. Manage History:
   - Export conversations to text files
   - Clear history when needed
   - History is automatically saved

Note: API usage may incur costs based on OpenAI pricing."""
        
        messagebox.showinfo("Help", help_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """AI Chatbot - OpenAI Integration

Version: 1.0
Author: Advanced Graphics Suite

Features:
• Multiple AI personas
• Conversation history
• Export functionality
• GUI interface
• OpenAI GPT-3.5 integration

This chatbot uses OpenAI's API to provide
intelligent conversational AI capabilities."""
        
        messagebox.showinfo("About", about_text)
    
    def run_cli(self):
        """Run the CLI version of the chatbot"""
        print("🤖 AI CHATBOT - OpenAI Integration")
        print("=" * 50)
        
        # Check API key
        if not self.api_key:
            print("⚠️ No API key found!")
            api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
            if api_key:
                self.set_api_key(api_key)
            else:
                print("⚠️ Running in demo mode without API key")
        
        print(f"🎭 Current persona: {self.current_persona}")
        print("💡 Type 'help' for commands, 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() == 'quit':
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_cli_help()
                    continue
                
                if user_input.lower() == 'persona':
                    self.change_persona_cli()
                    continue
                
                if user_input.lower() == 'clear':
                    self.clear_history()
                    print("🗑️ Conversation history cleared!")
                    continue
                
                if user_input.lower() == 'export':
                    filename = f"chatbot_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    if self.export_history(filename):
                        print(f"📄 Conversation exported to {filename}")
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 Assistant: ", end="", flush=True)
                response = self.get_chat_response(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_cli_help(self):
        """Show CLI help"""
        print("\n📖 Available Commands:")
        print("  help    - Show this help message")
        print("  persona - Change AI persona")
        print("  clear   - Clear conversation history")
        print("  export  - Export conversation to file")
        print("  quit    - Exit the chatbot")
        print("\n🎭 Available Personas:")
        for persona in self.personas.keys():
            print(f"  - {persona}")
    
    def change_persona_cli(self):
        """Change persona from CLI"""
        print("\n🎭 Select a persona:")
        for i, persona in enumerate(self.personas.keys(), 1):
            print(f"  {i}. {persona}")
        
        try:
            choice = input("\nEnter persona number (1-6): ").strip()
            persona_list = list(self.personas.keys())
            
            if choice.isdigit() and 1 <= int(choice) <= len(persona_list):
                self.current_persona = persona_list[int(choice) - 1]
                self.save_settings()
                print(f"✅ Persona changed to: {self.current_persona}")
            else:
                print("❌ Invalid choice!")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function to run the chatbot"""
    print("🤖 AI CHATBOT - OpenAI Integration")
    print("=" * 40)
    
    chatbot = OpenAIChatbot()
    
    # Choose interface
    print("Choose interface:")
    print("1. 🖥️ GUI Interface")
    print("2. 💻 CLI Interface")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        chatbot.run_gui()
    else:
        chatbot.run_cli()


if __name__ == "__main__":
    main()
