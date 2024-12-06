# src/utils/environment.py
import os

class Environment:
    def __init__(self):
        self.variables = {}
        
    def set(self, name, value):
        self.variables[name] = value
        os.environ[name] = str(value)
        
    def get(self, name):
        return self.variables.get(name, os.getenv(name))