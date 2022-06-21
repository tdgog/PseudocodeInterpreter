from __future__ import annotations
import utils.position as u_position
import utils.errors as u_error

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_position()
        self.set_context()
    
    def set_position(self, start:u_position.Position=None, end:u_position.Position=None) -> Number:
        self.start = start
        self.end = end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def __add__(self, other:Number) -> Number:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def __sub__(self, other:Number) -> Number:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def __mul__(self, other:Number) -> Number:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def __truediv__(self, other:Number) -> Number:
        if isinstance(other, Number):
            if other.value == 0:
                return None, u_error.RuntimeError(other.start, other.end, 'Division by zero', self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self) -> str:
        return f'{self.value}'
