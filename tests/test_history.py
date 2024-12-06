import pytest
import os
from src.utils.history import HistoryManager

class TestHistoryManager:
    @pytest.fixture
    def history(self, tmp_path):
        history_file = tmp_path / "test_history"
        return HistoryManager(str(history_file))
        
    def test_add_and_get_command(self, history):
        history.add_command("test command")
        assert "test command" in history.get_history()
        
    def test_clear_history(self, history):
        history.add_command("test command")
        history.clear_history()
        assert len(history.get_history()) == 0
        
    def test_save_and_load_history(self, history):
        history.add_command("test command")
        history.save_history()
        
        # Create new instance to test loading
        new_history = HistoryManager(history.history_file)
        assert "test command" in new_history.get_history()
        
    def test_search_history(self, history):
        commands = ["ls -l", "cd /tmp", "ls test"]
        for cmd in commands:
            history.add_command(cmd)
        
        results = history.search_history("ls")
        assert len(results) == 2
        assert all("ls" in cmd for cmd in results)
        
    def test_get_last_command(self, history):
        history.add_command("first")
        history.add_command("last")
        assert history.get_last_command() == "last"