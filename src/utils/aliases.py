class AliasManager:
    def __init__(self):
        self.aliases = {}
        
    def add_alias(self, name, command):
        self.aliases[name] = command
        
    def expand_alias(self, command):
        return self.aliases.get(command, command)