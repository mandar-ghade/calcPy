from math import cos, sin
from math_operator import MathOperator


class UnaryOperator(MathOperator):
    """Represents Unary operator."""
    
    def __init__(self, n: MathOperator | float) -> None:
        assert any((isinstance(n, MathOperator),
                    isinstance(n, float)))
        self.n = n

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.n})'


class Cos(UnaryOperator):

    def solve(self) -> float:
        if isinstance(self.n, MathOperator):
            n = self.n.solve()
        else:
            n = self.n
        return cos(n)


class Sin(UnaryOperator):

    def solve(self) -> float:
        if isinstance(self.n, MathOperator):
            n = self.n.solve()
        else:
            n = self.n
        return sin(n)

