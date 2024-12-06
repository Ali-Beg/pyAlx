import os
import configparser

class ShellConfig:
    def __init__(self, config_file='~/.myshellrc'):
        self.config = configparser.ConfigParser()
        self.config_file = os.path.expanduser(config_file)
        self.load_config()
        
    def load_config(self):
        self.config.read(self.config_file)
        
    def save_config(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            self.config.write(f)