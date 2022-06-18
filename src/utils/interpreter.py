from __future__ import annotations
import utils.nodes as u_node
import utils.tokens as u_token
import utils.types as u_types

class RuntimeResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, result:RuntimeResult) -> None:
        if result.error: self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined.')

    def visit_NumberNode(self, node:u_node.NumberNode) -> u_types.Number:
        return RuntimeResult().success(u_types.Number(node.token.value).set_position(node.start, node.end)) 
        
    def visit_BinaryOperationNode(self, node:u_node.BinaryOperationNode):
        result = RuntimeResult()
        left = result.register(self.visit(node.left_node))
        if result.error: return result
        right = result.register(self.visit(node.right_node))
        if result.error: return result

        value = None
        error = None
        match(node.operator_token.type):
            case u_token.TT_PLUS:
                value, error = left + right
            case u_token.TT_MINUS:
                value, error = left - right
            case u_token.TT_MUL:
                value, error = left * right
            case u_token.TT_DIV:
                value, error = left / right
        
        if error:
            return result.failure(error)
        return result.success(value.set_position(node.start, node.end))

    def visit_UnaryOperationNode(self, node:u_node.UnaryOperationNode):
        result = RuntimeResult()
        number = result.register(self.visit(node.node))
        if result.error: return result

        error = None
        if node.operator_token.type == u_token.TT_MINUS:
            number, error = number * u_types.Number(-1)

        if error:
            return result.failure(error)
        return result.success(number.set_position(node.start, node.end))
