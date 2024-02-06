class Symbol:
    def __init__(self, char: str) -> None:
        assert isinstance(char, str)
        self.symbol = char
    
    def __repr__(self) -> str:
        return f'({self.__class__.__name__})("{self.symbol}")'

    def __str__(self) -> str:
        return self.symbol
