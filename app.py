import pandas as pd
from pandas.core.indexes.category import contains

from models.team import Team
from models.user import User


def create_teams(df: pd.DataFrame) -> list[Team]:
    teams_cell_content: list[str] = []
    for _, row in df.iterrows():
        if not (
            teams_cell_content.__contains__(row["Qual equipe você está avaliando:"])
        ):
            teams_cell_content.append(row["Qual equipe você está avaliando:"])
        # print(f"Column 1: {row['Qual equipe você está avaliando:']}")

    teams: list[Team] = []
    for elm in teams_cell_content:
        nomes = elm.split(",")  # Split into two parts
        first_nome_content = nomes[0].split(" ", 3)
        id = first_nome_content[1]
        user1 = User(first_nome_content[3].strip())
        user2 = User(nomes[1].strip())
        user3 = User(nomes[2].strip())
        teams.append(Team(int(id), [user1, user2, user3]))

    return teams


def generate_grades_from_team(df: pd.DataFrame, team: Team):
    for _, row in df.iterrows():
        if row["Qual equipe você está avaliando:"].__contains__(str(team.id)):
            total = 0

            for grade in row.iloc[7:13]:
                total += grade

            avg = total / 6
            team.grades.append((row["Name"], avg))


def generate_all_grades(df: pd.DataFrame, teams: list[Team]):
    for t in teams:
        generate_grades_from_team(df, t)


def main():
    df = pd.read_excel(
        "/home/hetzwga/Downloads/IA SIS_ Avaliação dos Painéis TESTE MARLON(1-2).xlsx"
    )

    teams = create_teams(df)

    # printing all cells in an excel sheet
    # for row in df.itertuples(index=False):
    #     for cell in row:
    #         print(cell)
    #     print("")

    generate_all_grades(df, teams)

    for t in teams:
        print(t.id)
        print(t.grades)


main()
