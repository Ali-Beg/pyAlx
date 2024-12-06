# tests/test_redirection.py
import pytest
import os
from src.core.shell import Shell

class TestRedirection:
    @pytest.fixture
    def shell(self):
        """Create a shell instance for testing"""
        shell = Shell()
        yield shell
        # Cleanup any running processes
        for process in shell.background_processes.values():
            try:
                process.kill()
            except:
                pass

    def test_output_redirection(self, shell, tmp_path):
        output_file = tmp_path / "test.txt"
        shell.execute_command(f"echo hello > {str(output_file)}")
        assert output_file.exists()
        assert output_file.read_text().strip() == "hello"
        
    def test_input_redirection(self, shell, tmp_path, capsys):
        input_file = tmp_path / "input.txt"
        input_file.write_text("test data")
        shell.execute_command(f"cat < {str(input_file)}")
        captured = capsys.readouterr()
        assert "test data" in captured.out

    def test_combined_redirection(self, shell, tmp_path):
        input_file = tmp_path / "input.txt"
        output_file = tmp_path / "output.txt"
        input_file.write_text("test data")
        shell.execute_command(f"cat < {str(input_file)} > {str(output_file)}")
        assert output_file.exists()
        assert output_file.read_text().strip() == "test data"