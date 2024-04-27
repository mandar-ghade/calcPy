from typing import Optional, Self
from parsable_result import ParsableResult
from tk import Token

LEFT_PARENTHESES = ('(', '[', '{')
RIGHT_PARENTHESES = (')', ']', '}')
ALL_PARENTHESES = LEFT_PARENTHESES + RIGHT_PARENTHESES


class RightParenthesisNotFoundException(Exception):
    """Raised when right parenthesis is not found."""


class Expression:
    """Sorts tokens into Expressions.
    Handles parenthesis nesting and things of that sort."""

    def __init__(self, *expr: Token | Self) -> None:
        self.expr: list[Token | Self] = list(expr)
        self.simplify_conversion()

    def extend(self, *expr: Token | Self) -> None:
        if all(isinstance(tk, Token) for tk in expr):
            self.expr.append(Expression(*expr)) # type: ignore
        else:
            self.expr.extend(expr)

    def _get_rpi(self, lpi: int, lp_token: Token, tokens: list[Token | Self]) -> Optional[int]:
        """Returns matching rpi to lpi"""
        return next(iter((n - 1
                          for n in range(lpi + 1, len(tokens) + 1)
                          if (1 + sum(-1 if tk.x in LEFT_PARENTHESES else 1
                                      for tk in tokens[lpi:n]
                                      if isinstance(tk, Token) and tk.x in ALL_PARENTHESES
                                      ) > 0)
                          and tokens[n - 1] == RIGHT_PARENTHESES[LEFT_PARENTHESES.index(lp_token.x)])), None)

    def get_tokens_of_expression(self) -> list[Token]:
        return [t for t in self.expr if isinstance(t, Token)]

    def simplify_conversion(self) -> None:
        tokens: list[Token] = self.get_tokens_of_expression()
        while any(lp in tokens for lp in map(Token, LEFT_PARENTHESES)):
            for i, token in enumerate(self.expr):
                if isinstance(token, Expression) or token.x not in LEFT_PARENTHESES:
                    continue
                rpi: Optional[int] = self._get_rpi(i, token, self.expr) # type: ignore
                if rpi is None:
                    raise RightParenthesisNotFoundException("Matching right parenthesis not found.")
                break
            self.expr = self.expr[:i] + [Expression(*self.expr[i+1:rpi])] + self.expr[rpi + 1:] # type: ignore
            tokens = self.get_tokens_of_expression()

    def __add__(self, other: Token | Self) -> Self:
        raise NotImplementedError("Not implemented yet")

    def parse(self) -> list[ParsableResult]:
        res = list[ParsableResult]()
        if all(isinstance(tk, Token) for tk in self.expr):
            return [*self.expr] # type: ignore
        tks = list[Token]()
        for tk in self.expr:
            if isinstance(tk, Token):
                tks.append(tk)
            elif isinstance(tk, Expression):
                res.append(ParsableResult(*tks))
                res[-1].tokens.append(ParsableResult(*tk.parse()))
                tks.clear()
        if len(tks) > 1:
            res.extend(tks) # type: ignore
        return res

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(repr, self.expr))})'

    def __str__(self) -> str:
        return f'({"".join(map(str, self.expr))})'

