from delims import ALL_DELIMS
from itertools import pairwise
from typing import Callable

# BINARY_OPS = (...)
# UNARY_OPS = (...)

ADD_SUBTRACT = ('+', '-')

PRIORITY_DICT: dict[int, Callable[[str], bool]] = {
    1: lambda segment: any(c in ALL_DELIMS for c in segment),
    2: lambda segment: any((obj1, obj2) == ('*', '*') 
                           for obj1, obj2 in tuple(pairwise(segment))),
    3: lambda segment: any((obj1 == '*' and obj2 != '*')
                           or (obj1 != '*' and obj2 == '*')
                           for obj1, obj2 in tuple(pairwise(segment))),
    4: lambda segment: '/' in segment,
    5: lambda segment: any(c in ADD_SUBTRACT for c in segment)
}


def pre_parse(segment: str) -> list[tuple[int, int]]: #tuple format: (index, priority dict key)
    parsed_operations = []
    for i, s in enumerate(segment):
        for key, func in PRIORITY_DICT.items():
            res = func(s)
            mult_or_exponent = (s == '*' and func(segment[i:i+2]))
            if not res and not mult_or_exponent: 
                continue
            if mult_or_exponent:
                res = func(segment[i:i+2])
                if (i-1, 2) in parsed_operations: # if exponent already appended
                    continue
            parsed_operations.append((i, key))
    return parsed_operations


def main():
    segment = '(123+345)**2-3/4'
    parsed_operations = pre_parse(segment)
    print(parsed_operations)
    

if __name__ == '__main__':
    main()

