import os
import shutil
import platform
import sys
from typing import List, Tuple

class BuiltInCommands:
    # Store command history as a class variable
    command_history: List[str] = []
    
    def __init__(self):
        pass
    
    @staticmethod
    def add_to_history(command: str) -> None:
        """Add command to history"""
        BuiltInCommands.command_history.append(command)
        # Keep only last 1000 commands
        if len(BuiltInCommands.command_history) > 1000:
            BuiltInCommands.command_history.pop(0)

    @staticmethod
    def cd(args):
        """Change directory"""
        try:
            path = args[0] if args else os.path.expanduser("~")
            os.chdir(path)
            return True, ""
        except FileNotFoundError:
            return False, f"cd: no such directory: {path}"
        except IndexError:
            return False, "cd: missing directory argument"
    
    @staticmethod
    def pwd(_):
        """Print working directory"""
        return True, os.getcwd()
        
    @staticmethod
    def exit(_):
        """Exit the shell"""
        return True, "exit"

    @staticmethod
    def ls(args):
        """List directory contents"""
        try:
            path = args[0] if args else '.'
            files = os.listdir(path)
            return True, '\n'.join(sorted(files))
        except FileNotFoundError:
            return False, f"ls: cannot access '{path}': No such directory"
        except PermissionError:
            return False, f"ls: cannot open directory '{path}': Permission denied"

    @staticmethod
    def clear(_):
        """Clear the screen"""
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
        return True, ""

    @staticmethod
    def echo(args):
        """Echo the arguments"""
        return True, ' '.join(args)

    @staticmethod
    def history(args) -> Tuple[bool, str]:
        """Show command history"""
        if not args:
            # Show all history with numbers
            history_text = "\n".join(
                f"{idx:4d}  {cmd}" 
                for idx, cmd in enumerate(BuiltInCommands.command_history, 1)
            )
            return True, history_text
        return False, "history: too many arguments"

    @staticmethod
    def help(_):
        """Show help information"""
        help_text = """
Available Commands:
------------------
cd [dir]     - Change directory
pwd          - Print working directory
ls [dir]     - List directory contents
clear        - Clear screen
echo [text]  - Display text
exit         - Exit the shell
help         - Show this help message
history      - Show command history
"""
        return True, help_text.strip()

    @staticmethod
    def whoami(_):
        """Show current user"""
        return True, os.getenv('USERNAME') or os.getenv('USER') or 'Unknown'
        
    @staticmethod
    def mkdir(args):
        """Create a new directory"""
        if not args:
            return False, "mkdir: missing directory operand"
        try:
            os.makedirs(args[0])
            return True, ""
        except FileExistsError:
            return False, f"mkdir: cannot create directory '{args[0]}': File exists"

    @staticmethod
    def cp(args) -> Tuple[bool, str]:
        """Copy files and directories"""
        if len(args) != 2:
            return False, "cp: requires source and destination arguments"
        try:
            source, dest = args
            if os.path.isdir(source):
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            return True, ""
        except FileNotFoundError:
            return False, f"cp: cannot stat '{source}': No such file or directory"
        except PermissionError:
            return False, f"cp: cannot create regular file '{dest}': Permission denied"

    @staticmethod
    def mv(args) -> Tuple[bool, str]:
        """Move/rename files and directories"""
        if len(args) != 2:
            return False, "mv: requires source and destination arguments"
        try:
            source, dest = args
            shutil.move(source, dest)
            return True, ""
        except FileNotFoundError:
            return False, f"mv: cannot stat '{source}': No such file or directory"
        except PermissionError:
            return False, f"mv: cannot move '{source}': Permission denied"

    @staticmethod
    def rm(args) -> Tuple[bool, str]:
        """Remove files and directories"""
        if not args:
            return False, "rm: missing operand"
        
        recursive = "-r" in args or "-R" in args
        args = [arg for arg in args if arg not in ("-r", "-R")]
        
        for path in args:
            try:
                if os.path.isdir(path):
                    if recursive:
                        shutil.rmtree(path)
                    else:
                        return False, f"rm: cannot remove '{path}': Is a directory"
                else:
                    os.remove(path)
            except FileNotFoundError:
                return False, f"rm: cannot remove '{path}': No such file or directory"
            except PermissionError:
                return False, f"rm: cannot remove '{path}': Permission denied"
        
        return True, ""

    @staticmethod
    def aliases(args):
        """Manage shell aliases"""
        from src.core.shell import Shell  # Import here to avoid circular import
        
        if not args:
            # List all aliases
            if not Shell.alias_manager.aliases:
                return True, "No aliases defined"
            return True, "\n".join(f"{name}='{cmd}'" 
                                 for name, cmd in Shell.alias_manager.aliases.items())
        
        if len(args) >= 2 and args[0] == '-s':
            # Set new alias: aliases -s name command
            name = args[1]
            command = ' '.join(args[2:])
            Shell.alias_manager.add_alias(name, command)
            return True, f"Added alias: {name}='{command}'"
            
        return False, "Usage: aliases [-s name command]"