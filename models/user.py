class User:
    def __init__(self, name) -> None:
        self.name = name
        self.grades: list = []
        self.average = 0.0
