# tests/test_built_ins.py
import pytest
import os
import tempfile
from src.commands.built_ins import BuiltInCommands

class TestBuiltIns:
    @pytest.fixture
    def builtin(self):
        return BuiltInCommands()
    
    def test_cd(self, builtin, tmp_path):
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        success, output = BuiltInCommands.cd([str(test_dir)])
        assert success == True
        assert os.getcwd() == str(test_dir)
    
    def test_pwd(self, builtin):
        success, output = BuiltInCommands.pwd([])
        assert success == True
        assert output == os.getcwd()
    
    def test_mkdir(self, builtin, tmp_path):
        new_dir = tmp_path / "new_dir"
        success, output = BuiltInCommands.mkdir([str(new_dir)])
        assert success == True
        assert new_dir.exists()
    
    def test_history(self, builtin):
        BuiltInCommands.command_history.clear()
        test_commands = ["ls", "pwd", "echo test"]
        for cmd in test_commands:
            BuiltInCommands.add_to_history(cmd)
        success, output = BuiltInCommands.history([])
        assert success == True
        for cmd in test_commands:
            assert cmd in output

# src/commands/built_ins.py
# Add to BuiltInCommands class:
    @staticmethod
    def aliases(args):
        """List or set aliases"""
        from src.core.shell import Shell  # Import here to avoid circular import
        
        if not args:
            # List all aliases
            aliases_list = [f"{name}='{cmd}'" for name, cmd in Shell.alias_manager.aliases.items()]
            return True, "\n".join(aliases_list) if aliases_list else "No aliases defined"
            
        if len(args) >= 2 and args[0] == '-s':
            # Set new alias: aliases -s name command
            name = args[1]
            command = ' '.join(args[2:])
            Shell.alias_manager.add_alias(name, command)
            return True, f"Alias added: {name}='{command}'"
            
        return False, "Usage: aliases [-s name command]"