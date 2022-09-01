class TagNotFound(Exception):
    def __init__(self, argument: str):
        super().__init__(argument)


class NoPerm(Exception):
    ...
