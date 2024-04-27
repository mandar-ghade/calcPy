from typing import Any, Iterable, Iterator, Optional
from binary_operator import Addition, Division, Exponentiate, Multiplication, Subtraction
from expression import Expression
from math_operator import MathOperator
from parsable_result import ParsableResult
from tk import Token


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


def is_num(x: str) -> bool:
    """Returns if str is a number or not"""
    return x not in operator_map and x not in ALL_PARENTHESES


def tokenize(segment: str) -> Iterator[Token]:
    """Tokenization."""
    segment = segment.replace(' ', '')
    it = iter(segment)
    curr: Optional[str] = None
    while True:
        try:
            tk = next(it)
            token_is_number = is_num(tk)
            if token_is_number and not curr:
                curr = tk
            elif token_is_number and curr: # curr check unnecessary.
                curr += tk
            elif not token_is_number and curr is not None and tk != '*':
                yield from (Token(curr), Token(tk))
                curr = None
            elif not token_is_number and curr is None and tk != '*':
                yield Token(tk)
            elif curr == '*' and tk == curr:
                yield Token(curr + tk)
                curr = None
            elif curr is not None and curr != '*' and tk == '*':
                yield from (Token(curr), Token(tk))
                curr = None
            else:
                curr = tk
        except StopIteration:
            break
    if curr:
        yield Token(curr)


def main() -> None:
    expr = '2+3*(1234.02 + 5678.03+(1/2+(5/3/4 + 5/3) + 2/9))'
    tokens = tokenize(expr)
    expression = Expression(*tokens)
    print(expression.parse())
    print(*map(str, expression.parse()))
    print(str(expression))

if __name__ == "__main__":
    main()
