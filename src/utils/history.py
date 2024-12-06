import os
import readline
from typing import List, Optional

class HistoryManager:
    def __init__(self, history_file='~/.myshell_history'):
        self.history_file = os.path.expanduser(history_file)
        self.load_history()
        
    def load_history(self):
        """Load command history from file"""
        try:
            with open(self.history_file, 'r') as f:
                for line in f:
                    readline.add_history(line.strip())
        except FileNotFoundError:
            pass
            
    def save_history(self):
        """Save command history to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            for i in range(readline.get_current_history_length()):
                f.write(readline.get_history_item(i + 1) + '\n')
                
    def add_command(self, command: str):
        """Add a command to history"""
        if command.strip():  # Don't add empty commands
            readline.add_history(command)
        
    def get_history(self) -> List[str]:
        """Get all commands in history"""
        return [
            readline.get_history_item(i + 1)
            for i in range(readline.get_current_history_length())
        ]
        
    def clear_history(self):
        """Clear command history"""
        readline.clear_history()
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            
    def search_history(self, pattern: str) -> List[str]:
        """Search history for commands matching pattern"""
        return [cmd for cmd in self.get_history() if pattern in cmd]
        
    def get_last_command(self) -> Optional[str]:
        """Get the most recent command"""
        length = readline.get_current_history_length()
        return readline.get_history_item(length) if length > 0 else None