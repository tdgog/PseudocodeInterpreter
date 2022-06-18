from __future__ import annotations
import utils.errors as u_error
import utils.tokens as u_token
import utils.position as u_position

class Lexer:
    def __init__(self, filename:str, text:str) -> None:
        self.filename = filename
        self.text = text
        self.position = u_position.Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
        self.position.advance(self.current_char)
        self.current_char = self.text[self.position.index] if self.position.index < len(self.text) else None

    def make_tokens(self) -> tuple[list[u_token.Token], None|u_error.IllegalCharError]:
        tokens = []

        while self.current_char != None:
            # Ignore tabs and spaces
            if self.current_char in ' \t':
                self.advance()

            # Match numbers
            if self.current_char in u_token.DIGITS:
                tokens.append(self.make_number())
                continue

            # Match symbols
            match(self.current_char):
                case '+': tokens.append(u_token.Token(u_token.TT_PLUS, start=self.position))
                case '-': tokens.append(u_token.Token(u_token.TT_MINUS, start=self.position))
                case '*': tokens.append(u_token.Token(u_token.TT_MUL, start=self.position))
                case '/': tokens.append(u_token.Token(u_token.TT_DIV, start=self.position))
                case '(': tokens.append(u_token.Token(u_token.TT_LPAREN, start=self.position))
                case ')': tokens.append(u_token.Token(u_token.TT_RPAREN, start=self.position))
                case _: 
                    start = self.position.copy()
                    return [], u_error.IllegalCharError(
                        start, self.position,
                        f"'{self.current_char}'")

            self.advance()

        tokens.append(u_token.Token(u_token.TT_EOF, start=self.position))
        return tokens, None

    def make_number(self) -> u_token.Token:
        num_str = ''
        dot_count = 0
        start = self.position.copy()

        while self.current_char != None and self.current_char in u_token.DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    break
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0: return u_token.Token(u_token.TT_INT, int(num_str), start, self.position)
        return u_token.Token(u_token.TT_FLOAT, float(num_str), start, self.position)
