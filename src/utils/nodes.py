import utils.tokens as u_token

class NumberNode:
    def __init__(self, token:u_token.Token) -> None:
        self.token = token
    
    def __repr__(self) -> str:
        return f'{self.token}'

class BinaryOperationNode:
    def __init__(self, left_node:u_token.Token, operator_token:u_token.Token, right_node:u_token.Token) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class UnaryOperationNode:
    def __init__(self, operator_token:u_token.Token, node:NumberNode|BinaryOperationNode) -> None:
        self.operator_token = operator_token
        self.node = node

    def __repr__(self) -> str:
        return f'{self.operator_token}, {self.node}'
