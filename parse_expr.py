from typing import Iterable, Iterator, Optional
from binary_operator import Addition, Division, Exponentiate, Multiplication, Subtraction
from expression import Expression
from math_operator import MathOperator
from tk import Token

from pprint import pprint

LEFT_PARENTHESES = ('(', '[', '{')
RIGHT_PARENTHESES = (')', ']', '}')
ALL_PARENTHESES = LEFT_PARENTHESES + RIGHT_PARENTHESES


operator_map: dict[str, type[MathOperator]] = {
    '+': Addition,
    '-': Subtraction,
    '*': Multiplication,
    '/': Division,
    '**': Exponentiate,
}


def map_to_operator(tk: Token) -> Optional[type[MathOperator]]:
    return operator_map.get(tk.x)


def is_digit(x: str) -> bool:
    """Returns if str is a digit or not"""
    return x not in operator_map and x not in ALL_PARENTHESES


def tokenize(segment: str) -> Iterator[Token]:
    """Tokenization."""
    it = iter(segment)
    curr: Optional[str] = None
    while True:
        try:
            tk = next(it)
            if is_digit(tk) and not curr:
                curr = tk
            elif is_digit(tk) and curr: # curr check unnecessary.
                curr += tk
            elif not is_digit(tk) and curr is not None and tk != '*':
                yield from (Token(curr), Token(tk))
                curr = None
            elif not is_digit(tk) and curr is None and tk != '*':
                yield Token(tk)
            elif curr == '*' and tk == curr:
                yield Token(curr + tk)
                curr = None
            else:
                curr = tk
        except StopIteration:
            break
    if curr:
        yield Token(curr)


def main() -> None:
    expr = '(1234.02+5678.03+(1/2+(3/4)))**2/3.0'
    tokens = tokenize(expr)
    expression = Expression(*tokens) + Expression(*tokenize(expr))
    print(repr(expression))
    print(str(expression))

if __name__ == "__main__":
    main()
