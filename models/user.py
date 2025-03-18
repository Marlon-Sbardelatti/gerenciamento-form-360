class User:
    def __init__(self, name) -> None:
        self.name = name
        self.teams_evaluated: list = []
        self.avaliationGrade = 0
        self.professorGrade = 10
        self.content = 0
        self.finalGrade = 0
