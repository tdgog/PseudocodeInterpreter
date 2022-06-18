import utils.position as u_position

class Error:
    def __init__(self, start:u_position.Position, end:u_position.Position, error_name:str, details:str) -> None:
        self.start = start
        self.end = end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile {self.start.filename}, line {self.start.line + 1} & column {self.start.column + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, start:u_position.Position, end:u_position.Position, details) -> None:
        super().__init__(start, end, 'IllegalCharacter', details)

class InvalidSyntaxError(Error):
    def __init__(self, start:u_position.Position, end:u_position.Position, details) -> None:
        super().__init__(start, end, 'InvalidSyntax', details)
