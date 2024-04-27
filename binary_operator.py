from math import log
from math_operator import MathOperator


class BinaryOperator(MathOperator):
    def __init__(self, n1: float, n2: float) -> None:
        self.n1 = n1
        self.n2 = n2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.n1}, {self.n2})' 


class Addition(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return self.n1 + self.n2


class Subtraction(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return self.n1 - self.n2


class Multiplication(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return self.n1 * self.n2


class Division(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return self.n1 / self.n2


class Exponentiate(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return self.n1 ** self.n2


class Log(BinaryOperator):
    def __init__(self, n1: float, n2: float) -> None:
        super().__init__(n1, n2)

    def solve(self) -> float:
        return log(self.n2, self.n1) # n1 is base, n2 is other number


