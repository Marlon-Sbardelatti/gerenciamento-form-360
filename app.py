import pandas as pd
from models.team import Team
from models.user import User


def create_teams_and_evaluators(df: pd.DataFrame) -> tuple[list[Team], list[User]]:
    teams_cell_content: list[str] = []
    evaluators: list[User] = []
    for _, row in df.iterrows():
        if not (
            teams_cell_content.__contains__(row["Qual equipe você está avaliando:"])
        ):
            teams_cell_content.append(row["Qual equipe você está avaliando:"])

        evaluator = User(row["Name"])
        if not any(u.name == evaluator.name for u in evaluators):
            evaluators.append(evaluator)

    teams: list[Team] = []
    for elm in teams_cell_content:
        nomes = elm.split(",")  # Split into two parts
        first_nome_content = nomes[0].split(" ", 3)
        id = first_nome_content[1]
        user1 = User(first_nome_content[3].strip())
        user2 = User(nomes[1].strip())
        user3 = User(nomes[2].strip())
        teams.append(Team(int(id), [user1, user2, user3]))

    return teams, evaluators


def generate_grades_from_team(df: pd.DataFrame, team: Team, evaluators: list[User]):
    for _, row in df.iterrows():
        if row["Qual equipe você está avaliando:"].__contains__(str(team.id)):
            total = 0

            for grade in row.iloc[7:13]:
                total += grade

            avg = total / 6
            team.grades.append((row["Name"], avg))
            for e in evaluators:
                if e.name == row["Name"]:
                    e.teams_evaluated.append(team)


def generate_all_grades(df: pd.DataFrame, teams: list[Team], evaluators: list[User]):
    for t in teams:
        generate_grades_from_team(df, t, evaluators)


def get_avg_from_teams(teams: list[Team]):
    for t in teams:
        total = 0
        for g in t.grades:
            total += g[1]

        t.average = total / len(t.grades)


def main():
    df = pd.read_excel(
        "/home/hetzwga/Downloads/IA SIS_ Avaliação dos Painéis TESTE MARLON(1-2).xlsx"
    )

    teams, users = create_teams_and_evaluators(df)

    generate_all_grades(df, teams, users)

    get_avg_from_teams(teams)

    # for t in teams:
    #     print(t.id)
    #     print(t.grades)
    #     print(t.average)
    #     print("")

    # for u in users:
    #     print(u.name)

    for u in users:
        print("User:", u.name, "avaliou as equipes: ")
        for t in u.teams_evaluated:
            print(t.id)
            for m in t.members:
                print(m.name)
            print("")

main()
