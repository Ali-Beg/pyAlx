# src/gui/main_window.py
import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedTk
import platform
import sys
import io
from typing import List
from src.core.shell import Shell
from src.utils.helpers import ShellPrompt

class TerminalWidget(ttk.Frame):
    ANSI_COLORS = {
        '30': '#000000',  # Black
        '31': '#FF0000',  # Red
        '32': '#00FF00',  # Green
        '33': '#FFFF00',  # Yellow
        '34': '#0000FF',  # Blue
        '35': '#FF00FF',  # Magenta
        '36': '#00FFFF',  # Cyan
        '37': '#FFFFFF',  # White
    }

    def __init__(self, parent, shell):
        super().__init__(parent)
        self.shell = shell  # Store shell reference
        self.prompt_generator = ShellPrompt()
        self.setup_ui()
        self.command_history: List[str] = []
        self.history_index = 0
        self.input_start = "1.0"
        
    def setup_ui(self):
        # Configure font
        if platform.system() == 'Windows':
            term_font = font.Font(family='Consolas', size=10)
        else:
            term_font = font.Font(family='DejaVu Sans Mono', size=10)
            
        # Terminal output area
        self.output = tk.Text(
            self,
            wrap=tk.WORD,
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='white',
            selectbackground='#264F78',
            font=term_font,
            pady=5,
            padx=5
        )
        self.output.grid(row=0, column=1, sticky='nsew')
        
        # Line numbers
        self.linenumbers = tk.Text(
            self,
            width=4,
            bg='#2D2D2D',
            fg='#858585',
            font=term_font,
            pady=5,
            padx=5
        )
        self.linenumbers.grid(row=0, column=0, sticky='nsew')
        self.linenumbers.config(state='disabled')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.output.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.output['yscrollcommand'] = scrollbar.set
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Key bindings
        self.output.bind('<Return>', self.handle_return)
        self.output.bind('<Up>', self.history_up)
        self.output.bind('<Down>', self.history_down)
        
    def clear_terminal(self):
        """Clear terminal output"""
        self.output.delete("1.0", tk.END)
        self.update_line_numbers()
        self.show_prompt()
        
    def handle_return(self, event=None):
        current_line = self.output.get("insert linestart", "insert lineend")
        command = current_line.replace(self.prompt_generator.generate_prompt(), "").strip()
        
        if command:
            # Add to history BEFORE executing
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            if command.lower() == 'clear':
                self.clear_terminal()
                return "break"
                
            # Execute command using shell instance
            try:
                if command.lower() == 'exit':
                    self.master.quit()
                    return "break"
                    
                stdout = sys.stdout
                output_capture = io.StringIO()
                sys.stdout = output_capture
                
                self.shell.execute_command(command)
                
                sys.stdout = stdout
                output = output_capture.getvalue()
                if output:
                    self.write(output)
            except Exception as e:
                self.write(f"Error: {str(e)}\n", '31')
            finally:
                self.write("\n")
                self.show_prompt()
                
        return "break"
        
    def history_up(self, event=None):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.output.delete("insert linestart", "insert lineend")
            self.output.insert("insert linestart", f"$ {self.command_history[self.history_index]}")
        return "break"
        
    def history_down(self, event=None):
        """Navigate command history down"""
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.replace_current_line(self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.replace_current_line("")
        return "break"
        
    def replace_current_line(self, text):
        """Replace current command line with text"""
        self.output.delete("insert linestart", "insert lineend")
        self.output.insert("insert linestart", f"$ {text}")
        
    def write(self, text, color=None):
        """Write text to terminal with optional color"""
        tag = None
        if color:
            tag = f'color_{color}'
            self.output.tag_configure(tag, foreground=self.ANSI_COLORS.get(color, '#FFFFFF'))
            
        self.output.insert(tk.END, text, tag)
        self.output.see(tk.END)
        self.update_line_numbers()
        
        # Update input start position
        self.input_start = self.output.index("end-1c")
        
    def update_line_numbers(self):
        """Update line numbers"""
        lines = self.output.get('1.0', tk.END).count('\n')
        self.linenumbers.config(state='normal')
        self.linenumbers.delete('1.0', tk.END)
        for i in range(1, lines + 1):
            self.linenumbers.insert(tk.END, f'{i}\n')
        self.linenumbers.config(state='disabled')
        
    def show_prompt(self):
        """Display shell prompt"""
        prompt = self.prompt_generator.generate_prompt()
        self.write(prompt, '36')  # Cyan color

class MainWindow:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("PyShell Terminal")
        self.shell = Shell()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.configure(bg='#1E1E1E')
        self.root.geometry('800x600')
        
        # Pass shell instance directly to TerminalWidget
        self.terminal = TerminalWidget(self.root, self.shell)
        self.terminal.pack(fill=tk.BOTH, expand=True)
        
        self.terminal.write("Welcome to PyShell Terminal\n", '32')
        self.terminal.write("Type 'exit' to quit\n\n", '33')
        self.terminal.show_prompt()
        
    def run(self):
        self.root.mainloop()
        
    def cleanup(self):
        """Clean up resources before closing"""
        if hasattr(self, 'shell'):
            for process in self.shell.background_processes.values():
                try:
                    process.kill()
                except:
                    pass
        if hasattr(self, 'root'):
            self.root.quit()
            self.root.destroy()