class Token:
    def __init__(self, x: str) -> None:
        self.x = x

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.x}")'

