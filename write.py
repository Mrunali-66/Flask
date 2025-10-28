import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from datetime import datetime
import time

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Dangerous Writing App")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # State variables
        self.is_active = False
        self.last_keystroke_time = None
        self.danger_threshold = 5  # seconds
        self.warning_threshold = 3  # seconds before deletion
        self.total_words = 0
        self.session_start_time = None
        self.check_interval = 100  # ms
        self.timer_id = None
        
        # Color scheme
        self.colors = {
            'safe': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'bg': '#1a1a1a',
            'text': '#ecf0f1',
            'header': '#34495e'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="The Dangerous Writing App",
            font=('Arial', 24, 'bold'),
            bg=self.colors['header'],
            fg=self.colors['text']
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Stop typing for 5 seconds and lose everything...",
            font=('Arial', 11),
            bg=self.colors['header'],
            fg='#95a5a6'
        )
        subtitle_label.pack()
        
        # Stats bar
        stats_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        stats_frame.pack(fill='x')
        stats_frame.pack_propagate(False)
        
        self.timer_label = tk.Label(
            stats_frame,
            text="Time Remaining: --",
            font=('Arial', 14, 'bold'),
            bg='#2c3e50',
            fg=self.colors['safe']
        )
        self.timer_label.pack(side='left', padx=20)
        
        self.word_count_label = tk.Label(
            stats_frame,
            text="Words: 0",
            font=('Arial', 12),
            bg='#2c3e50',
            fg=self.colors['text']
        )
        self.word_count_label.pack(side='left', padx=20)
        
        self.status_label = tk.Label(
            stats_frame,
            text="Status: Not Started",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.status_label.pack(side='left', padx=20)
        
        # Text editor
        editor_frame = tk.Frame(self.root, bg=self.colors['bg'])
        editor_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.text_widget = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=('Georgia', 14),
            bg='#2c3e50',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            selectbackground='#34495e',
            selectforeground=self.colors['text'],
            relief=tk.FLAT,
            padx=20,
            pady=20
        )
        self.text_widget.pack(fill='both', expand=True)
        self.text_widget.bind('<Key>', self.on_keystroke)
        self.text_widget.focus()
        
        # Placeholder text
        placeholder = "Start typing to begin... Once you start, don't stop for more than 5 seconds or everything will be deleted!"
        self.text_widget.insert('1.0', placeholder)
        self.text_widget.config(fg='#7f8c8d')
        self.text_widget.bind('<FocusIn>', self.clear_placeholder)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.start_button = tk.Button(
            control_frame,
            text="Start Session",
            command=self.start_session,
            bg=self.colors['safe'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        self.start_button.pack(side='left', padx=5)
        
        self.save_button = tk.Button(
            control_frame,
            text="Save Progress",
            command=self.save_file,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT,
            state='disabled'
        )
        self.save_button.pack(side='left', padx=5)
        
        self.reset_button = tk.Button(
            control_frame,
            text="Reset",
            command=self.reset_session,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            relief=tk.FLAT
        )
        self.reset_button.pack(side='left', padx=5)
        
        # Settings
        settings_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        settings_frame.pack(side='right')
        
        tk.Label(
            settings_frame,
            text="Danger Time:",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 5))
        
        self.danger_time_var = tk.StringVar(value="5")
        danger_options = ['3', '5', '10', '15']
        danger_menu = tk.OptionMenu(
            settings_frame,
            self.danger_time_var,
            *danger_options,
            command=self.update_danger_time
        )
        danger_menu.config(
            bg='#34495e',
            fg=self.colors['text'],
            font=('Arial', 10),
            relief=tk.FLAT,
            highlightthickness=0
        )
        danger_menu.pack(side='left')
        
    def clear_placeholder(self, event=None):
        """Clear placeholder text on first focus"""
        if self.text_widget.get('1.0', 'end-1c').startswith("Start typing to begin..."):
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.config(fg=self.colors['text'])
            self.text_widget.unbind('<FocusIn>')
    
    def update_danger_time(self, value):
        """Update danger threshold from dropdown"""
        self.danger_threshold = int(value)
        self.warning_threshold = max(1, self.danger_threshold - 2)
        
    def start_session(self):
        """Start the dangerous writing session"""
        if not self.is_active:
            self.is_active = True
            self.session_start_time = time.time()
            self.last_keystroke_time = time.time()
            self.start_button.config(text="Session Active", state='disabled', bg='#95a5a6')
            self.save_button.config(state='normal')
            self.status_label.config(text="Status: Writing", fg=self.colors['safe'])
            self.text_widget.config(bg='#2c3e50')
            self.check_inactivity()
    
    def on_keystroke(self, event):
        """Handle keystroke event"""
        # Ignore special keys
        if event.keysym in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 
                             'Alt_L', 'Alt_R', 'Caps_Lock']:
            return
        
        # Start session on first keystroke if not started
        if not self.is_active and event.char:
            self.start_session()
        
        if self.is_active:
            self.last_keystroke_time = time.time()
            self.update_word_count()
            
            # Reset text color if it was warning
            self.text_widget.config(bg='#2c3e50')
            self.timer_label.config(fg=self.colors['safe'])
            self.status_label.config(text="Status: Writing", fg=self.colors['safe'])
    
    def check_inactivity(self):
        """Check if user has been inactive too long"""
        if not self.is_active:
            return
        
        current_time = time.time()
        time_since_last_keystroke = current_time - self.last_keystroke_time
        time_remaining = self.danger_threshold - time_since_last_keystroke
        
        # Update timer display
        if time_remaining > 0:
            self.timer_label.config(text=f"Time Remaining: {time_remaining:.1f}s")
            
            # Warning state
            if time_remaining <= self.warning_threshold:
                self.text_widget.config(bg='#c0392b')
                self.timer_label.config(fg=self.colors['danger'])
                self.status_label.config(text="Status: DANGER!", fg=self.colors['danger'])
            elif time_remaining <= self.warning_threshold + 1:
                self.text_widget.config(bg='#d35400')
                self.timer_label.config(fg=self.colors['warning'])
                self.status_label.config(text="Status: Warning", fg=self.colors['warning'])
        else:
            # Time's up - delete everything
            self.delete_all_text()
            return
        
        # Schedule next check
        self.timer_id = self.root.after(self.check_interval, self.check_inactivity)
    
    def delete_all_text(self):
        """Delete all text - the dangerous part"""
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.config(bg='#e74c3c')
        self.timer_label.config(text="Time Remaining: 0.0s", fg=self.colors['danger'])
        self.status_label.config(text="Status: Text Deleted!", fg=self.colors['danger'])
        
        # Show dramatic message
        self.text_widget.insert('1.0', 
            "YOUR TEXT HAS BEEN DELETED!\n\n"
            "You stopped typing for too long.\n"
            "Click Reset to try again.",
            )
        self.text_widget.config(fg=self.colors['danger'], font=('Arial', 16, 'bold'))
        
        self.is_active = False
        self.start_button.config(text="Start Session", state='normal', bg=self.colors['safe'])
        self.save_button.config(state='disabled')
        
        # Play system beep if available
        try:
            self.root.bell()
        except:
            pass
    
    def update_word_count(self):
        """Update word count display"""
        text = self.text_widget.get('1.0', 'end-1c')
        words = len(text.split())
        self.word_count_label.config(text=f"Words: {words}")
        self.total_words = words
    
    def save_file(self):
        """Save current text to file"""
        text = self.text_widget.get('1.0', 'end-1c')
        
        if not text or text.startswith("YOUR TEXT HAS BEEN DELETED"):
            messagebox.showwarning("Warning", "No text to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", f"File saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def reset_session(self):
        """Reset the application"""
        if self.is_active:
            confirm = messagebox.askyesno(
                "Confirm Reset",
                "Session is active. Are you sure you want to reset?\nAll text will be lost!"
            )
            if not confirm:
                return
        
        # Cancel any pending timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        # Reset state
        self.is_active = False
        self.last_keystroke_time = None
        self.session_start_time = None
        self.total_words = 0
        
        # Reset UI
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.config(
            bg='#2c3e50',
            fg=self.colors['text'],
            font=('Georgia', 14)
        )
        
        placeholder = "Start typing to begin... Once you start, don't stop for more than 5 seconds or everything will be deleted!"
        self.text_widget.insert('1.0', placeholder)
        self.text_widget.config(fg='#7f8c8d')
        self.text_widget.bind('<FocusIn>', self.clear_placeholder)
        
        self.timer_label.config(text="Time Remaining: --", fg=self.colors['safe'])
        self.word_count_label.config(text="Words: 0")
        self.status_label.config(text="Status: Not Started", fg='#95a5a6')
        self.start_button.config(text="Start Session", state='normal', bg=self.colors['safe'])
        self.save_button.config(state='disabled')

def main():
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()