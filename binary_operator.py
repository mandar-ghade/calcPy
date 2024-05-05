from math import log
from math_operator import MathOperator


class BinaryOperator(MathOperator):
    def __init__(self, n1: float | MathOperator, n2: float | MathOperator) -> None:
        self.n1 = n1
        self.n2 = n2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.n1}, {self.n2})' 

    def __hash__(self) -> int:
        return hash((self.n1, self.n2))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)


class Addition(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return n1 + n2


class Subtraction(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return n1 - n2


class Multiplication(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return n1 * n2


class Division(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return n1 / n2


class Exponentiate(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return n1 ** n2


class Log(BinaryOperator):

    def solve(self) -> float:
        n1, n2 = self.n1, self.n2
        if isinstance(n1, MathOperator):
            n1 = n1.solve()
        if isinstance(n2, MathOperator):
            n2 = n2.solve()
        return log(n2, n1) # n1 is base, n2 is other number


