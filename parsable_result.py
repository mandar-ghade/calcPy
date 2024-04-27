from typing import Self
from tk import Token


class ParsableResult:
    """Represents an expression as a Parsable Result.
    Pre-parsing for tokens in expressions."""
    def __init__(self, *tokens: Token | Self) -> None:
        self.tokens = list(tokens)

    def extend(self, *tokens: Token | Self) -> None:
        if all(isinstance(tk, Token) for tk in tokens):
            self.tokens.append(ParsableResult(*tokens)) # type: ignore
        else:
            self.tokens.append(tokens) # type: ignore

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(repr, self.tokens))})'

    def __str__(self) -> str:
        return f'({"".join(map(str, self.tokens))})'

    def solve(self) -> float:
        """Gets result by parsing from tokens"""
        raise NotImplementedError("Parser not implemented yet")

