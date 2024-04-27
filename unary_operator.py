from math import cos, sin
from math_operator import MathOperator


class UnaryOperator(MathOperator):
    """Represents Unary operator."""
    
    def __init__(self, n: float) -> None:
        self.n = n

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.n})'


class Cos(UnaryOperator):
    def __init__(self, n: float) -> None:
        super().__init__(n)

    def solve(self) -> float:
        return cos(self.n)


class Sin(UnaryOperator):
    def __init__(self, n: float) -> None:
        super().__init__(n)

    def solve(self) -> float:
        return sin(self.n)

