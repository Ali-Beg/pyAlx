import os
import socket
import getpass

class ShellPrompt:
    def __init__(self):
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        
    def generate_prompt(self):
        """Generate shell prompt with [user@host:path]$ format"""
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        
        # Replace home directory with ~
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
            
        # Shorten path if too long
        if len(cwd) > 30:
            parts = cwd.split(os.sep)
            if len(parts) > 3:
                cwd = os.path.join("...", *parts[-2:])
                
        return f"[{self.username}@{self.hostname}:{cwd}]$ "