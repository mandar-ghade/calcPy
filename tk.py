class Token:
    def __init__(self, x: str) -> None:
        self.x = x

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.x}")'

    def __str__(self) -> str:
        return self.x

    def __hash__(self) -> int:
        return hash(self.x)

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)
