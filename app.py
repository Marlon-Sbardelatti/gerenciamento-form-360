import pandas as pd
import csv
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
        nomes = elm.split(",") 
        first_nome_content = nomes[0].split(" ", 3)
        id = first_nome_content[1]
        user1 = User(first_nome_content[3].strip())
        user2 = User(nomes[1].strip())
        user3 = User(nomes[2].strip())
        teams.append(Team(int(id), [user1, user2, user3]))

    for elm in evaluators_cell_content:
        nomes = elm.split(",")  
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



def calculate_evaluator_grades(evaluators: list[Team], teams: list[Team]):
    for e in evaluators:
        if not e.evaluated_teams:
            continue  

        given_grades = []
        real_grades = []

        for t in e.evaluated_teams:
            for g in t.grades:
                if g[0] == e.id:
                    given_grades.append(g[1])

            real_grades.append(t.average)

        if given_grades and real_grades:
            avg_given = sum(given_grades) / len(given_grades)
            avg_real = sum(real_grades) / len(real_grades)

            deviation = abs(avg_given - avg_real)
            e.avaliatorGrade = max(10 - deviation, 0) 

            print(f"Evaluator {e.id} - Given Avg: {avg_given}, Real Avg: {avg_real}, Adjusted Grade: {e.avaliatorGrade}")

            for t in teams:
                if t.id == e.id:
                    t.avaliatorGrade = e.avaliatorGrade





def calculate_final_grades(teams: list[Team]):
    for t in teams:
        avaliator_grade = t.avaliatorGrade  

        for m in t.members:
            m.finalGrade = m.content * 0.6 + avaliator_grade * 0.4  

            print(f"Final grade for {m.name}: {m.finalGrade} (content: {m.content}, team evaluator grade: {avaliator_grade})")



def save_final_grades_to_csv(teams: list[Team], filename="final_grades.csv"):
    students = []

    for t in teams:
        for m in t.members:
            students.append((m.name, m.finalGrade))

    students.sort(key=lambda x: x[0])

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")  
        writer.writerow(["Nome", "Nota Final"]) 

        for name, final_grade in students:
            writer.writerow([name, f"{final_grade:.2f}"]) 

    print(f"Arquivo '{filename}' salvo com sucesso!")




def main():
    df = pd.read_excel(
        "C:/Users/User/Downloads/IA SIS_ Avaliação dos Painéis TESTE MARLON(1-4).xlsx"
    )

    teams, evaluators = create_teams_and_evaluators(df)

    generate_all_grades(df, teams, evaluators)

    get_avg_from_teams(teams)

    generate_content_users(teams)

    calculate_evaluator_grades(evaluators, teams) 

    calculate_final_grades(teams)

    save_final_grades_to_csv(teams)

main()
	