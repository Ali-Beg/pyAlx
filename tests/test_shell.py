# tests/test_shell.py
import os
import pytest
from src.core.shell import Shell

class TestShell:
    @pytest.fixture
    def shell(self):
        return Shell()
    
    def test_shell_initialization(self, shell):
        assert shell.running == True
        assert shell.prompt == "myshell> "
        assert isinstance(shell.built_ins, dict)
        
    def test_background_process(self, shell):
        shell.execute_command("ping localhost -n 1 &")
        assert len(shell.background_processes) > 0
        
    def test_pipe_execution(self, shell, capsys):
        # Windows-specific test since grep isn't available
        if os.name == 'nt':
            shell.execute_command("echo test | findstr test")
        else:
            shell.execute_command("echo test | grep test")
        
        captured = capsys.readouterr()
        assert "test" in captured.out.lower()
        
    def test_path_completion(self, shell, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.touch()
        os.chdir(tmp_path)
        completion = shell._path_completer("te", 0)
        assert completion == "test.txt "
        
    def test_pipe_io_handling(self, shell, capsys):
        # Test multi-pipe command
        if os.name == 'nt':
            shell.execute_command('dir | find "test" | sort')
        else:
            shell.execute_command('ls | grep test | sort')
        
        captured = capsys.readouterr()
        assert captured.err == ''  # No errors
        
    def test_pipe_error_handling(self, shell, capsys):
        # Test pipe with nonexistent command
        shell.execute_command('echo test | nonexistentcmd')
        captured = capsys.readouterr()
        assert "Command not found" in captured.out
        
    def test_pipe_background(self, shell):
        # Test piped command in background
        shell.execute_command('ping localhost | find "Reply" &')
        assert len(shell.background_processes) > 0