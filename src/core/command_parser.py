# src/core/command_parser.py
class CommandParser:
    def __init__(self):
        pass
    
    def parse(self, command_string):
        """Parse command with redirections"""
        if not command_string:
            return None, [], False, None, None, None
        
        # Check for background process
        is_background = command_string.strip().endswith('&')
        if is_background:
            command_string = command_string[:-1].strip()
        
        # Handle redirections
        input_file = output_file = None
        parts = command_string.split()
        new_parts = []
        
        i = 0
        while i < len(parts):
            if parts[i] == '>':
                if i + 1 < len(parts):
                    output_file = parts[i + 1]
                    i += 2
                    continue
            elif parts[i] == '<':
                if i + 1 < len(parts):
                    input_file = parts[i + 1]
                    i += 2
                    continue
            new_parts.append(parts[i])
            i += 1
            
        command_string = ' '.join(new_parts)
        
        # Split on pipes
        pipe_commands = [cmd.strip() for cmd in command_string.split('|')]
        
        if len(pipe_commands) == 1:
            parts = new_parts
            command = parts[0].lower() if parts else None
            args = parts[1:] if len(parts) > 1 else []
            return command, args, is_background, None, input_file, output_file
            
        parsed_commands = []
        for cmd in pipe_commands:
            parts = cmd.strip().split()
            if not parts:
                continue
            parsed_commands.append((parts[0].lower(), parts[1:] if len(parts) > 1 else []))
            
        return parsed_commands[0][0], parsed_commands[0][1], is_background, parsed_commands[1:], input_file, output_file