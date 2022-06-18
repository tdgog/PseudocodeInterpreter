from __future__ import annotations

class Position:
    def __init__(self, index:int, line:int, column:int, filename:str, filetext:str) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char:str=None) -> Position:
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.line += 1
            self.column = 0

        return self

    def copy(self) -> Position:
        return Position(self.index, self.line, self.column, self.filename, self.filetext)