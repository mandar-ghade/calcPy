from abc import ABC, abstractmethod


class MathOperator(ABC):
    """Represents Operator."""

    @abstractmethod 
    def solve(self) -> float:
        """Solves expression."""

