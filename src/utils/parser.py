from __future__ import annotations
import utils.tokens as u_token
import utils.nodes as u_node
import utils.errors as u_error

class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
    
    def register(self, result:ParseResult|u_node.NumberNode|u_node.BinaryOperationNode):
        if isinstance(result, ParseResult):
            if result.error: self.error = result.error
            return result.node
        return result

    def success(self, node:u_node.NumberNode|u_node.BinaryOperationNode):
        self.node = node
        return self
    
    def failure(self, error:u_error.Error):
        self.error = error
        return self

class Parser:
    def __init__(self, tokens:list[u_token.Token]) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        result = self.expression()
        if not result.error and self.current_token.type != u_token.TT_EOF:
            return result.failure(u_error.InvalidSyntaxError(
                self.current_token.start, self.current_token.end,
                "Expected '+', '-', '*', or '/'"
            ))
        return result

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (u_token.TT_PLUS, u_token.TT_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(u_node.UnaryOperationNode(token, factor))

        elif token.type in (u_token.TT_INT, u_token.TT_FLOAT):
            result.register(self.advance())
            return result.success(u_node.NumberNode(token))

        elif token.type == u_token.TT_LPAREN:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error: return result
            if self.current_token.type == u_token.TT_RPAREN:
                result.register(self.advance())
                return result.success(expression)
            else:
                return result.failure(u_error.InvalidSyntaxError(
                    self.current_token.start, self.current_token.end, "Expected ')'"
                ))

        return result.failure(u_error.InvalidSyntaxError(token.start, token.end, 'Expected INTEGER or FLOAT'))
    
    def term(self):
        return self.binary_operation(self.factor, (u_token.TT_MUL, u_token.TT_DIV))

    def expression(self):
        return self.binary_operation(self.term, (u_token.TT_PLUS, u_token.TT_MINUS))
    
    def binary_operation(self, function, operation_tokens):
        result = ParseResult()
        left = result.register(function())
        if result.error: return result

        while self.current_token.type in operation_tokens:
            operator_token = self.current_token

            result.register(self.advance())
            right = result.register(function())
            if result.error: return result

            left = u_node.BinaryOperationNode(left, operator_token, right)

        return result.success(left)
