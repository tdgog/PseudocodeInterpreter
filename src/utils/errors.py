import utils.position as u_position
from utils.string_with_arrows import *

class Error:
    def __init__(self, start:u_position.Position, end:u_position.Position, error_name:str, details:str) -> None:
        self.start = start
        self.end = end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'File {self.start.filename}, line {self.start.line + 1}\n'
        result += string_with_arrows(self.start.filetext, self.start, self.end)
        result += f'\n{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, start:u_position.Position, end:u_position.Position, details) -> None:
        super().__init__(start, end, 'IllegalCharacter', details)

class InvalidSyntaxError(Error):
    def __init__(self, start:u_position.Position, end:u_position.Position, details) -> None:
        super().__init__(start, end, 'InvalidSyntax', details)

class RuntimeError(Error):
    def __init__(self, start:u_position.Position, end:u_position.Position, details, context) -> None:
        super().__init__(start, end, 'RuntimeError', details)
        self.context = context
    
    def as_string(self):
        result = self.generate_traceback()
        result += string_with_arrows(self.start.filetext, self.start, self.end)
        result += f'\n{self.error_name}: {self.details}\n\n'
        return result

    def generate_traceback(self):
        result = ''
        pos = self.start
        ctx = self.context
        while ctx:
            result = f'    File {self.start.filename}, line {self.start.line +1}, in {self.context.display_name}\n{result}'
            pos = ctx.parent_entry_position
            ctx = ctx.parent

        return f'Traceback (most recent call last):\n{result}'