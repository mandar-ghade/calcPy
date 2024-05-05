from typing import Iterable, Iterator, Optional, TypeVar

T = TypeVar('T')

class PeekableIterator(object):
    """Iterator object with peeking
    Accepts Iterable or arbitrary length of arguments"""
    def __init__(self, it: Optional[Iterable[T]] = None, *args: T) -> None:
        self.it_copy = list[T]()
        arguments: Optional[Iterable[T] | tuple[T, ...]] = None
        if it:
            assert isinstance(it, Iterable), ('Expected type "Iterable" for "it". '
                                              f'Instead received type: {it.__class__.__name__}')
            arguments = it
        elif args:
            arguments = args
        assert arguments is not None, 'Iterable not found.'
        self.it_copy = [x for x in arguments]
        self.it = iter(self)
        #print(*self, '...')
        self.prev, self.curr = None, next(self.it, None)

    def __next__(self) -> object:
        if self.prev == self.curr == None:
            self.prev = next(self.it, None)
            self.curr = next(self.it, None)
        else:
            self.prev = self.curr
            self.curr = next(self.it, None)
        if self.prev == self.curr == None:
            raise StopIteration("Iteration has ended.")
        return self.prev

    def __iter__(self) -> Iterator[object]:
        return (x for x in self.it_copy)

    def peek(self) -> object:
        return self.curr

