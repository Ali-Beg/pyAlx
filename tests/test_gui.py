import pytest
import tkinter as tk
import time
from src.gui.main_window import MainWindow, TerminalWidget
from src.core.shell import Shell
pytest_plugins = ["pytest_asyncio"]

class TestGUI:
    @pytest.fixture
    def gui(self):
        root = tk.Tk()
        shell = Shell()
        terminal = TerminalWidget(root, shell)
        yield terminal
        try:
            if root.winfo_exists():
                root.destroy()
        except:
            pass

    @pytest.fixture
    def main_window(self):
        window = MainWindow()
        yield window
        try:
            if window.root.winfo_exists():
                window.root.destroy()
        except:
            pass

    def test_terminal_widget_init(self, gui):
        assert isinstance(gui.shell, Shell)
        assert len(gui.command_history) == 0
        assert gui.history_index == 0

    def test_clear_command(self, gui):
        gui.write("test output\n")
        gui.clear_terminal()
        assert gui.output.get("1.0", tk.END).strip() == "$"

    def test_command_history(self, gui):
        commands = ["ls", "pwd", "echo test"]
        for cmd in commands:
            gui.write(f"$ {cmd}\n")
            gui.handle_return()
            time.sleep(0.1)  # Allow command to process
        assert gui.command_history == commands

    def test_color_output(self, gui):
        gui.write("Error message", '31')  # Red
        assert 'color_31' in gui.output.tag_names()

    def test_history_navigation(self, gui):
        commands = ["cmd1", "cmd2"]
        for cmd in commands:
            gui.command_history.append(cmd)
        
        gui.history_up(None)
        time.sleep(0.1)  # Allow UI update
        current = gui.output.get("insert linestart", "insert lineend")
        assert "cmd2" in current

    def test_main_window_init(self, main_window):
        assert isinstance(main_window.shell, Shell)
        assert isinstance(main_window.terminal, TerminalWidget)

    def test_execute_command(self, main_window):
        main_window.terminal.write("$ ls\n")
        main_window.terminal.handle_return()
        # Check if output contains directory listing

    def test_long_running_command(self, main_window):
        main_window.terminal.write("$ sleep 2\n")
        main_window.terminal.handle_return()
        time.sleep(0.1)
        assert main_window.terminal.output.get("1.0", tk.END).strip() != ""

    def test_window_close(self, main_window):
        main_window.cleanup()
        assert len(main_window.shell.background_processes) == 0