class Team:
    def __init__(self, id: int, members: list) -> None:
        self.id: int = id
        self.members: list = members
        self.grades: list = []
        self.average: float = 0.0
