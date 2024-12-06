# tests/test_executable_finder.py
import pytest
import os
from src.core.executable_finder import ExecutableFinder

class TestExecutableFinder:
    @pytest.fixture
    def finder(self):
        return ExecutableFinder()
    
    def test_find_system_command(self, finder):
        if os.name == 'nt':
            # Test multiple Windows commands
            windows_cmds = ['cmd.exe', 'cmd', 'notepad.exe', 'notepad']
            found = False
            for cmd in windows_cmds:
                path = finder.find_executable(cmd)
                if path is not None:
                    found = True
                    break
            assert found, "No Windows system command found"
        else:
            path = finder.find_executable('ls')
            assert path is not None
    
    def test_find_nonexistent_command(self, finder):
        path = finder.find_executable("nonexistentcommand123")
        assert path is None
    
    def test_find_absolute_path(self, finder):
        if os.name == 'nt':
            cmd = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'cmd.exe')
        else:
            cmd = '/bin/ls'
        path = finder.find_executable(cmd)
        assert path is not None