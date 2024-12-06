# src/core/executable_finder.py
import os
import shutil

class ExecutableFinder:
    def __init__(self):
        self.path = os.getenv('PATH', '').split(os.pathsep)
        # Add Windows System32 directory explicitly
        if os.name == 'nt':
            system32 = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')
            if system32 not in self.path:
                self.path.append(system32)

    def find_executable(self, command):
        """Find the full path of an executable"""
        if os.path.isabs(command):
            return command if os.access(command, os.X_OK) else None

        # Handle Windows executables
        if os.name == 'nt':
            # Try with and without .exe extension
            cmd_variants = [command]
            if not command.lower().endswith('.exe'):
                cmd_variants.append(f"{command}.exe")
            
            for cmd in cmd_variants:
                # Try direct which() first
                path = shutil.which(cmd)
                if path:
                    return path
                
                # Manual search in PATH
                for directory in self.path:
                    full_path = os.path.join(directory, cmd)
                    if os.path.isfile(full_path):
                        return full_path
            return None
        
        # Unix-like systems
        return shutil.which(command)