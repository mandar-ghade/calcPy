from abc import ABCMeta

from binary_operator import Addition, Division, Exponentiate, Multiplication, Subtraction


operator_priorities_mapped: dict[int, tuple[ABCMeta, ...]] = {
    1: (Exponentiate, ),
    2: (Multiplication, Division, ),
    3: (Addition, Subtraction, ),
}

