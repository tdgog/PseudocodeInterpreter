import utils.position as u_position


DIGITS = '0123456789'

TT_INT = 'INTEGER'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

class Token:
    def __init__(self, type_, value=None, start:u_position.Position=None, end:u_position.Position=None) -> None:
        self.type = type_
        self.value = value
        
        if start: 
            self.start = start.copy()
            self.end = start.copy()
            self.end.advance()
        if end: self.end = end.copy()

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    