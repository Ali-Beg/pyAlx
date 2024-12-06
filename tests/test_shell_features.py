import pytest
import os
import configparser
from src.utils.environment import Environment
from src.utils.aliases import AliasManager
from src.utils.history import HistoryManager
from src.utils.config import ShellConfig

class TestShellFeatures:
    @pytest.fixture
    def env(self):
        return Environment()
        
    @pytest.fixture
    def aliases(self):
        return AliasManager()
        
    def test_environment_variables(self, env):
        env.set('TEST_VAR', 'test_value')
        assert env.get('TEST_VAR') == 'test_value'
        
    def test_aliases(self, aliases):
        aliases.add_alias('ll', 'ls -l')
        assert aliases.expand_alias('ll') == 'ls -l'
        
    def test_history_file(self, tmp_path):
        history_file = tmp_path / "test_history"
        history = HistoryManager(str(history_file))
        history.add_command("test")
        history.save_history()
        assert os.path.exists(history_file)
        
    def test_config_loading(self, tmp_path):
        config_file = tmp_path / "test_config"
        config = ShellConfig(str(config_file))
        assert isinstance(config.config, configparser.ConfigParser)