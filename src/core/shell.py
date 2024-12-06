import os
import subprocess
import readline
import glob
import signal
import argparse
from typing import Dict, Optional
from src.commands.built_ins import BuiltInCommands
from src.core.command_parser import CommandParser
from src.core.executable_finder import ExecutableFinder
from src.utils.helpers import ShellPrompt
from src.utils.aliases import AliasManager

def parse_args():
    parser = argparse.ArgumentParser(description='Custom Python Shell')
    parser.add_argument('--init-file', help='Shell initialization file')
    parser.add_argument('--no-prompt', action='store_true', help='Disable custom prompt')
    parser.add_argument('--history-file', default='~/.myshell_history', help='Command history file')
    return parser.parse_args()

class Shell:
    # Add class variable for alias manager
    alias_manager = AliasManager()
    
    def __init__(self):
        self.running = True
        self.prompt = "myshell> "  # Add this line
        self.prompt_generator = ShellPrompt()
        self.parser = CommandParser()
        self.executor = ExecutableFinder()
        self.built_ins = {
            'cd': BuiltInCommands.cd,
            'pwd': BuiltInCommands.pwd,
            'exit': BuiltInCommands.exit,
            'aliases': BuiltInCommands.aliases,  # Add aliases command
            'ls': BuiltInCommands.ls,
            'clear': BuiltInCommands.clear,
            'echo': BuiltInCommands.echo,
            'help': BuiltInCommands.help,
            'history': BuiltInCommands.history,
            'whoami': BuiltInCommands.whoami,
            'mkdir': BuiltInCommands.mkdir
        }
        
        # Initialize readline with tab completion
        readline.set_completer_delims(' \t\n=')
        readline.set_completer(self._path_completer)
        readline.parse_and_bind('tab: complete')

        self.built_ins.update({
            'cp': BuiltInCommands.cp,
            'mv': BuiltInCommands.mv,
            'rm': BuiltInCommands.rm,
            'history': BuiltInCommands.history,
            'aliases': BuiltInCommands.aliases
        })
        
        self.background_processes: Dict[int, subprocess.Popen] = {}

    def _path_completer(self, text, state):
        """Complete file and directory paths"""
        # Get the current line and word being completed
        line = readline.get_line_buffer()
        
        # Handle empty input
        if not text:
            text = '.'
            
        # Expand user paths (e.g. ~/)
        if text.startswith('~'):
            text = os.path.expanduser(text)
            
        # Get matching paths
        matches = glob.glob(text + '*')
        
        # Add trailing slash to directories
        matches = [f"{m}{'/' if os.path.isdir(m) else ' '}" for m in matches]
        
        # Return the state-th match or None if no more matches
        try:
            return matches[state]
        except IndexError:
            return None

    def _command_completer(self, text, state):
        """Complete built-in commands"""
        commands = list(self.built_ins.keys())
        matches = [cmd for cmd in commands if cmd.startswith(text)]
        try:
            return matches[state]
        except IndexError:
            return None

    def _check_background_processes(self):
        """Check and clean up finished background processes"""
        finished = []
        for pid, process in self.background_processes.items():
            if process.poll() is not None:
                finished.append(pid)
                print(f"[{pid}] Done")
        
        for pid in finished:
            del self.background_processes[pid]

    def execute_piped_commands(self, commands, is_background=False, stdin=None, stdout=None):
        """Execute a series of piped commands with proper stream handling"""
        processes = []
        prev_pipe = stdin
        
        try:
            # Validate all commands first
            for cmd, args in commands:
                executable = self.executor.find_executable(cmd)
                if not executable:
                    print(f"Command not found: {cmd}")
                    return False

            # Create pipes
            for i, (cmd, args) in enumerate(commands):
                executable = self.executor.find_executable(cmd)
                
                # Setup pipes
                if i < len(commands) - 1:
                    read_fd, write_fd = os.pipe()
                    next_pipe = write_fd
                else:
                    next_pipe = stdout

                try:
                    process = subprocess.Popen(
                        [executable] + args,
                        stdin=prev_pipe,
                        stdout=next_pipe if next_pipe else subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1  # Line buffered
                    )
                    
                    processes.append(process)
                    
                    # Setup for next iteration
                    if i < len(commands) - 1:
                        os.close(write_fd)
                        prev_pipe = read_fd

                except Exception as e:
                    print(f"Error starting process {cmd}: {e}")
                    return False

            # Background process handling
            if is_background:
                pid = processes[-1].pid
                self.background_processes[pid] = processes[-1]
                print(f"[{pid}] Running in background")
                return True

            # Wait and collect output
            success = True
            for i, process in enumerate(processes):
                try:
                    output, error = process.communicate()
                    if error:
                        print(f"Error in {commands[i][0]}: {error.strip()}")
                        success = False
                    if i == len(processes) - 1 and output and not stdout:
                        print(output.strip())
                except Exception as e:
                    print(f"Error in process communication: {e}")
                    success = False

            return success

        except Exception as e:
            print(f"Pipe execution failed: {e}")
            return False
            
        finally:
            # Clean up processes and file descriptors
            for process in processes:
                try:
                    if process.poll() is None:
                        process.kill()
                except:
                    pass

    def execute_command(self, user_input):
        """Execute command with proper error handling"""
        if not user_input.strip():
            return

        # Update unpacking to match parser return values
        command, args, is_background, piped_commands, input_file, output_file = self.parser.parse(user_input)
        
        if not command:
            return
            
        try:
            if piped_commands:
                # Handle piped commands
                for cmd, _ in [(command, args)] + piped_commands:
                    if not self.executor.find_executable(cmd):
                        print(f"Command not found: {cmd}")
                        return
                        
                self.execute_piped_commands(
                    [(command, args)] + piped_commands,
                    is_background,
                    input_file,
                    output_file
                )
            else:
                # Handle single command
                if command in self.built_ins:
                    success, output = self.built_ins[command](args)
                    if output:
                        if output_file:
                            with open(output_file, 'w') as f:
                                f.write(output)
                        else:
                            print(output)
                    return

                executable = self.executor.find_executable(command)
                if not executable:
                    print(f"Command not found: {command}")
                    return

                try:
                    process = subprocess.Popen(
                        [executable] + args,
                        stdin=open(input_file, 'r') if input_file else None,
                        stdout=open(output_file, 'w') if output_file else subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    if is_background:
                        self.background_processes[process.pid] = process
                        print(f"[{process.pid}] Running in background")
                    else:
                        output, error = process.communicate()
                        if error:
                            print(error.strip())
                        if output and not output_file:
                            print(output.strip())

                except Exception as e:
                    print(f"Error executing command: {e}")
                    
        except Exception as e:
            print(f"Error: {e}")

    def get_prompt(self):
        """Get the current prompt string"""
        return self.prompt_generator.generate_prompt()

    def stop(self):
        """Stop the shell and cleanup"""
        self.running = False
        # Cleanup background processes
        for process in self.background_processes.values():
            try:
                process.kill()
            except:
                pass

    def run(self):
        print("Welcome to MyShell! Type 'exit' to quit.\n")
        
        while self.running:
            try:
                prompt = self.prompt_generator.generate_prompt()
                user_input = input(prompt).strip()
                
                if user_input:
                    if user_input.lower() == 'exit':
                        self.stop()
                        break
                    self.execute_command(user_input)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except EOFError:
                self.stop()
                break