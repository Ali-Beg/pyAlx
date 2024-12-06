# tests/test_command_parser.py
import pytest
from src.core.command_parser import CommandParser

class TestCommandParser:
    @pytest.fixture
    def parser(self):
        return CommandParser()
    
    def test_simple_command(self, parser):
        cmd, args, is_bg, piped = parser.parse("ls -l")
        assert cmd == "ls"
        assert args == ["-l"]
        assert is_bg == False
        assert piped == None
    
    def test_background_command(self, parser):
        cmd, args, is_bg, piped = parser.parse("sleep 10 &")
        assert cmd == "sleep"
        assert args == ["10"]
        assert is_bg == True
        
    def test_piped_command(self, parser):
        cmd, args, is_bg, piped = parser.parse("ls -l | grep .py")
        assert cmd == "ls"
        assert args == ["-l"]
        assert len(piped) == 1
        assert piped[0] == ("grep", [".py"])