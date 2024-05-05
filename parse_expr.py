from typing import Any, Iterable, Iterator, Optional
from binary_operator import Addition, BinaryOperator, Division, Exponentiate, Log, Multiplication, Subtraction
from expression import Expression
from math_operator import MathOperator
from tk import Token
from unary_operator import Cos, Sin, UnaryOperator


LEFT_PARENTHESES = ('(', '[', '{')
RIGHT_PARENTHESES = (')', ']', '}')
ALL_PARENTHESES = LEFT_PARENTHESES + RIGHT_PARENTHESES


operator_map: dict[str, type[MathOperator]] = {
    '+': Addition,
    '-': Subtraction,
    '*': Multiplication,
    '/': Division,
    '**': Exponentiate,
    'log': Log
}


unary_operators: tuple[type[UnaryOperator], ...] = (Cos, Sin, )


operator_priorities_mapped: dict[int, tuple[type[MathOperator], ...]] = {
    1: (Exponentiate, ),
    2: (Multiplication, Division, ),
    3: (Addition, Subtraction, ),
}

def map_to_operator(tk: Token) -> Optional[type[MathOperator]]:
    return operator_map.get(tk.x)


def is_num(x: str) -> bool:
    """Returns if str is a number or not"""
    return x not in operator_map and x not in ALL_PARENTHESES


def tokenize(segment: str) -> Iterator[Token]:
    """Tokenization."""
    # TODO: Simplify using peekable iterator
    # TODO: Redo tokenization.
    # TODO: Parse unary operators
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


def is_binary(operator_str: str) -> bool:
    operator = operator_map.get(operator_str) 
    assert operator is not None, 'Operator was not found' 
    return issubclass(operator, BinaryOperator)


type IntermediateToken = tuple[int, Optional[Token | Expression | MathOperator]] # int represents index, output represents Intermediate Token.


def get_tokens_at_priority_level(level: int, it: Iterable[IntermediateToken]) -> Iterator[tuple[int, Token | Expression]]:
    match = operator_priorities_mapped.get(level, None)
    assert (level != 0 and match) or level == 0, f'Priority level {level} does not exist.'
    for index, value in it: 
        if (level != 0 and isinstance(value, Expression)) or \
                ((match is None and isinstance(value, Token)) or (isinstance(value, Token) and operator_map.get(value.x) not in match)):
            continue
        yield (index, value)


def map_by_index(expr: Expression) -> Iterator[IntermediateToken]:
    yield from ((index, value) 
                for index, value in enumerate(expr))


type TokenDuplet = tuple[IntermediateToken, IntermediateToken] # unary
type TokenTriplet = tuple[IntermediateToken, IntermediateToken, IntermediateToken] # binary


def map_into_triplets(
        it: Iterable[IntermediateToken]
    ) -> Iterator[TokenTriplet]:
    # TODO : Token duplets for unary operators.
    it = iter(it)
    left, middle, right = next(it, None), next(it, None), next(it, None)
    if all((left, middle, right))\
            and isinstance(middle, tuple)\
            and isinstance(middle[1], Token)\
            and middle[1].x in operator_map:
        assert (left is not None and middle is not None and right is not None), 'Cannot be None.'
        yield (left, middle, right)
    while True:
        left, middle, right = middle, right, next(it, None)
        if not all((left, middle, right)):
            break
        if not isinstance(middle, tuple)\
                or not isinstance(middle[1], Token) \
                or not middle[1].x in operator_map: # or you can just check middle is not None
            continue
        assert (left is not None and middle is not None and right is not None), 'Cannot be None.'
        yield (left, middle, right)



def flatten(it: Iterable[Any]) -> Iterator[Any]:
    for item in it:
        if isinstance(item, Iterable) \
                and not isinstance(item, tuple):
            yield from flatten(item)
        else:
            yield item


def parse(curr_expr: Expression) -> MathOperator:
    """Parses Expression"""
    intermediate_tokens: list[IntermediateToken] = list(map_by_index(curr_expr))
    triplet_map: list[TokenTriplet] = list(map_into_triplets(intermediate_tokens))
    expr_map: dict[tuple[int, MathOperator], set[IntermediateToken]] = {}
    for level in range(0, 4):
        matches: list[tuple[int, Token | Expression]] = list(get_tokens_at_priority_level(level, intermediate_tokens))
        for left, middle, right in triplet_map:
            i, left = left
            j, middle = middle
            k, right = right

            if (j, middle) not in matches:
                continue

            assert isinstance(middle, Token) and map_to_operator(middle), 'Operation not properly matched.' # maybe not check twice

            matched_operation = map_to_operator(middle)

            if isinstance(left, Expression):
                left = parse(left)
            if isinstance(right, Expression):
                right = parse(right)
            
            left_is_matched = (i, left) in flatten(expr_map.values())
            right_is_matched = (k, right) in flatten(expr_map.values())

            left = next((operation[1]
                         for operation, mapped_tokens in expr_map.items()
                         if (i, left) in mapped_tokens or left == operation[1]), left) 

            right = next((operation[1]
                          for operation, mapped_tokens in expr_map.items()
                          if (k, right) in mapped_tokens or right == operation[1]), right)

            assert matched_operation is not None, 'Operation cannot be None'

            n1, n2 = left, right
            if isinstance(left, Token):
                n1 = float(left.x)

            if isinstance(right, Token):
                n2 = float(right.x)

            operation = matched_operation(n1, n2)

            if (j, operation) in expr_map:
                expr_map[(j, operation)].add((i, left))
                expr_map[(j, operation)].add((k, right))
            elif left_is_matched and right_is_matched:
                left_key, left_tokens = next(((op, mapped_tokens) 
                                    for op, mapped_tokens in expr_map.items()
                                    if (i, left) in mapped_tokens or left == op[1]))
                right_key, right_tokens = next(((op, mapped_tokens)
                                     for op, mapped_tokens in expr_map.items()
                                     if (k, right) in mapped_tokens or right == op[1]))
                expr_map.pop(left_key)
                expr_map.pop(right_key)
                expr_map[(j, operation)] = left_tokens.union(right_tokens)
            elif left_is_matched:
                left_key, left_tokens = next(((op, mapped_tokens) 
                                    for op, mapped_tokens in expr_map.items()
                                    if (i, left) in mapped_tokens or left == op[1]))
                left_tokens.add((k, right))
                expr_map.pop(left_key)
                expr_map[(j, operation)] = left_tokens
            elif right_is_matched:
                right_key, right_tokens = next(((op, mapped_tokens)
                                     for op, mapped_tokens in expr_map.items()
                                     if (k, right) in mapped_tokens or right == op[1]))
                right_tokens.add((i, left))
                expr_map.pop(right_key)
                expr_map[(j, operation)] = right_tokens
            else:
                expr_map[(j, operation)] = {(i, left), (k, right)}

    return next((val[1] for val in expr_map))


def main() -> None:
    expr = '2+3*(1234.02 + 5678.03+(1/2+(5/3/4 + 5/3) + 2/9))'
    tokens = tokenize(expr)
    expression = Expression(*tokens)
    res = parse(expression)
    print('parsed expression: ', res)
    print('result: ', res.solve())

if __name__ == "__main__":
    main()

