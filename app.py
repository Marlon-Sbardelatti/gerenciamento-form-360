import pandas as pd
from models.team import Team
from models.user import User


def create_teams_and_evaluators(df: pd.DataFrame) -> tuple[list[Team], list[Team]]:
    teams_cell_content: list[str] = []
    evaluators_cell_content: list[str] = []

    for _, row in df.iterrows():
        if not (
            evaluators_cell_content.__contains__(
                row["Identifique qual é a sua equipe:"]
            )
        ):
            evaluators_cell_content.append(row["Identifique qual é a sua equipe:"])

        if not (
            teams_cell_content.__contains__(row["Qual equipe você está avaliando:"])
        ):
            teams_cell_content.append(row["Qual equipe você está avaliando:"])

    teams: list[Team] = []
    evaluators: list[Team] = []
    for elm in teams_cell_content:
        nomes = elm.split(",")  # Split into two parts
        first_nome_content = nomes[0].split(" ", 3)
        id = first_nome_content[1]
        user1 = User(first_nome_content[3].strip())
        user2 = User(nomes[1].strip())
        user3 = User(nomes[2].strip())
        teams.append(Team(int(id), [user1, user2, user3]))

    for elm in evaluators_cell_content:
        nomes = elm.split(",")  # Split into two parts
        first_nome_content = nomes[0].split(" ", 3)
        id = first_nome_content[1]
        user1 = User(first_nome_content[3].strip())
        user2 = User(nomes[1].strip())
        user3 = User(nomes[2].strip())
        evaluators.append(Team(int(id), [user1, user2, user3]))

    return teams, evaluators


def generate_grades_from_team(df: pd.DataFrame, team: Team, evaluators: list[Team]):
    for _, row in df.iterrows():
        if row["Qual equipe você está avaliando:"].__contains__(str(team.id)):
            total = 0

            for grade in row.iloc[8:14]:
                total += grade

            avg = total / 6
            id = [
                int(i)
                for i in str(row["Identifique qual é a sua equipe:"]).split()
                if i.isdigit()
            ]

            team.grades.append((id[0], avg))

            evaluator = row["Identifique qual é a sua equipe:"]
            nomes = str(evaluator).split(",")
            first_nome_content = nomes[0].split(" ", 3)
            id = first_nome_content[1]

            for e in evaluators:
                if e.id == int(id):
                    e.evaluated_teams.append(team)


def generate_all_grades(df: pd.DataFrame, teams: list[Team], evaluators: list[Team]):
    for t in teams:
        generate_grades_from_team(df, t, evaluators)


def get_avg_from_teams(teams: list[Team]):
    for t in teams:
        total = 0
        for g in t.grades:
            total += g[1]

        t.average = total / len(t.grades)


def generate_content_users(teams: list[Team]):
    for t in teams:
        for m in t.members:
            m.content = (t.average + (m.professorGrade * 5)) / 6


def generate_deviations(evaluators: list[Team]):
    for e in evaluators:
        print("Evaluator", e.id, "avaliou os teams:")
        own_grades = 0
        own_count = 0
        count = 0
        total = 0
        for t in e.evaluated_teams:
            print(t.id)
            inner_count = 0
            inner_total = 0
            for g in t.grades:
                if g[0] != e.id:
                    inner_total += g[1]
                    inner_count += 1
                else:
                    own_grades += g[1]
                    own_count += 1
            others_team_avg = inner_total / inner_count
            count += 1
            total += others_team_avg
        all_others_team_avg = total / count
        own_avg = own_grades / own_count
        deviation = (all_others_team_avg + own_avg) / 2
        e.deviation = deviation
        print("own avg :", own_avg)
        print("all others avg:", all_others_team_avg)
        print("")


def main():
    df = pd.read_excel(
        "/home/hetzwga/Downloads/IA SIS_ Avaliação dos Painéis TESTE MARLON(1-5).xlsx"
    )

    teams, evaluators = create_teams_and_evaluators(df)

    generate_all_grades(df, teams, evaluators)

    get_avg_from_teams(teams)

    for t in teams:
        print("ID da equipe:", t.id)
        print("Notas:", t.grades)
        print("Média:", t.average)
        print("Desvio:", t.deviation)

    generate_content_users(teams)

    # for t in teams:
    #     for m in t.members:
    #         print(m.name, m.professorGrade)

    generate_deviations(evaluators)

    for e in evaluators:
        print("ID da equipe:", e.id)
        print("Notas:", e.grades)
        print("Média:", e.average)
        print("Desvio:", e.deviation)


main()
