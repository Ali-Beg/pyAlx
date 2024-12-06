# src/core/shell.py
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
            # Create all processes in the pipeline
            for i, (cmd, args) in enumerate(commands):
                # Create pipe for next command
                if i < len(commands) - 1:
                    read_fd, write_fd = os.pipe()
                    next_pipe = write_fd
                else:
                    next_pipe = stdout
                
                # Find executable
                executable = self.executor.find_executable(cmd)
                if not executable:
                    print(f"Command not found: {cmd}")
                    return
                
                # Create process with proper stream redirection
                process = subprocess.Popen(
                    [executable] + args,
                    stdin=prev_pipe,
                    stdout=next_pipe if next_pipe else subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    close_fds=True
                )
                
                processes.append(process)
                
                # Setup for next iteration
                if i < len(commands) - 1:
                    os.close(write_fd)
                    prev_pipe = read_fd
                else:
                    prev_pipe = None
            
            # Handle background processes
            if is_background:
                pid = processes[-1].pid
                self.background_processes[pid] = processes[-1]
                print(f"[{pid}] Running in background")
                return
            
            # Wait for completion and get output
            for i, process in enumerate(processes):
                stdout, stderr = process.communicate()
                
                if stderr:
                    print(f"Error in command {commands[i][0]}: {stderr}")
                
                if i == len(processes) - 1 and stdout:
                    print(stdout.strip())
                    
        except Exception as e:
            print(f"Pipe execution failed: {e}")
        finally:
            # Cleanup processes
            for process in processes:
                try:
                    process.kill()
                except:
                    pass

    def execute_command(self, user_input):
        """Execute command with I/O redirection support"""
        if not user_input.strip():
            return
            
        BuiltInCommands.add_to_history(user_input)
        self._check_background_processes()
        
        # Update unpacking to match all returned values
        command, args, is_background, piped_commands, input_file, output_file = self.parser.parse(user_input)
        
        if not command:
            return
            
        # Handle built-in commands
        if command in self.built_ins:
            success, output = self.built_ins[command](args)
            if output:
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(output)
                else:
                    print(output)
            return
        
        # Handle external commands
        executable = self.executor.find_executable(command)
        if not executable:
            print(f"Command not found: {command}")
            return
            
        try:
            # Setup I/O redirection
            stdin = open(input_file, 'r') if input_file else None
            stdout = open(output_file, 'w') if output_file else None
            
            if piped_commands:
                self.execute_piped_commands(
                    [(command, args)] + piped_commands,
                    is_background,
                    stdin,
                    stdout
                )
            else:
                process = subprocess.Popen(
                    [executable] + args,
                    stdin=stdin or subprocess.PIPE,
                    stdout=stdout or subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if is_background:
                    self.background_processes[process.pid] = process
                    print(f"[{process.pid}] Running in background")
                else:
                    output, error = process.communicate()
                    if error:
                        print(f"Error: {error.strip()}")
                    if output and not output_file:
                        print(output.strip())
                        
        except Exception as e:
            print(f"Error executing command: {e}")
        finally:
            if stdin: stdin.close()
            if stdout: stdout.close()

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