class Team:
    def __init__(self, id: int, members: list) -> None:
        self.id: int = id
        self.members: list = members
        self.evaluated_teams: list = []
        self.grades: list = []
        self.average: float = 0.0
        self.avg: float = 0.0
