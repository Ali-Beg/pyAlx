import pytest
import os
import getpass
import socket
from src.utils.helpers import ShellPrompt

class TestShellPrompt:
    @pytest.fixture
    def prompt(self):
        return ShellPrompt()
    
    def test_prompt_format(self, prompt):
        generated = prompt.generate_prompt()
        username = getpass.getuser()
        hostname = socket.gethostname()
        assert username in generated
        assert hostname in generated
        assert generated.startswith("[")
        assert generated.endswith("]$ ")
    
    def test_home_directory_shortening(self, prompt):
        home = os.path.expanduser("~")
        os.chdir(home)
        generated = prompt.generate_prompt()
        assert "~" in generated
    
    def test_long_path_shortening(self, prompt, tmp_path):
        # Create deep directory structure
        deep_path = tmp_path
        for i in range(5):
            deep_path = deep_path / f"dir{i}"
            deep_path.mkdir()
        
        os.chdir(deep_path)
        generated = prompt.generate_prompt()
        assert "..." in generated