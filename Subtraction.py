class Subtraction:
    def __init__(self, n1: str, n2: str) -> None:
        self.n1 = n1
        self.n2 = n2

    def __repr__(self) -> str:
        return f'({self.__class__.__name__})("{self.n1}", "{self.n2}")'

    def solve(self) -> float:
        return float(self.n1) - float(self.n2)

