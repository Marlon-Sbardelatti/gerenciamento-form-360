import pandas as pd
from models.team import Team
from models.user import User


def create_teams_and_evaluators(df: pd.DataFrame) -> tuple[list[Team], list[Team]]:
    teams_cell_content: set = set()  # Agora usamos um SET para evitar duplicatas
    evaluators_cell_content: set = set()

    for _, row in df.iterrows():
        evaluator = str(row["Identifique qual é a sua equipe:"]).strip()
        evaluated_team = str(row["Qual equipe você está avaliando:"]).strip()

        evaluators_cell_content.add(evaluator)
        teams_cell_content.add(evaluated_team)  

    teams: list[Team] = []
    evaluators: list[Team] = []
    
    processed_team_ids = set()  # Conjunto para evitar IDs duplicados

    for elm in teams_cell_content:
        nomes = elm.split(",")

        first_nome_content = nomes[0].split()
        if len(first_nome_content) < 2:
            continue  # Evita erros se o formato estiver errado

        id = first_nome_content[1].strip()  

        if id in processed_team_ids:
            continue  # Se o ID já foi processado, pula para o próximo

        processed_team_ids.add(id)  # Marca como processado

        user1 = User(first_nome_content[-1].strip())  
        user2 = User(nomes[1].strip()) if len(nomes) > 1 else User("Desconhecido")
        user3 = User(nomes[2].strip()) if len(nomes) > 2 else User("Desconhecido")

        teams.append(Team(int(id), [user1, user2, user3]))

    processed_evaluator_ids = set()

    for elm in evaluators_cell_content:
        nomes = elm.split(",")

        first_nome_content = nomes[0].split()
        if len(first_nome_content) < 2:
            continue  

        id = first_nome_content[1].strip()  

        if id in processed_evaluator_ids:
            continue  

        processed_evaluator_ids.add(id)  

        user1 = User(first_nome_content[-1].strip())  
        user2 = User(nomes[1].strip()) if len(nomes) > 1 else User("Desconhecido")
        user3 = User(nomes[2].strip()) if len(nomes) > 2 else User("Desconhecido")

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



def generate_deviations(teams: list[Team]):
    for t in teams:
        for grade in t.grades:
            evaluator_id, evaluated_grade = grade  # ID do avaliador e a nota atribuída
            team_avg = t.average  # Média da equipe avaliada

            # Calcula o desvio como a diferença absoluta entre a nota atribuída e a média da equipe
            deviation = abs(evaluated_grade - team_avg)

            # Encontra a equipe avaliadora com base no evaluator_id
            evaluator_team = next((team for team in teams if team.id == evaluator_id), None)
            if evaluator_team:
                # Ajusta o avaliatorGrade da equipe avaliadora
                evaluator_team.avaliatorGrade -= deviation

            # Exibe o desvio calculado
            print(f"Team {t.id} - Evaluator {evaluator_id} - Deviation: {deviation}")



# def generate_deviations(evaluators: list[Team]):
#     for e in evaluators:
#         print(f"\nEvaluator {e.id} avaliou os teams:")

#         for t in e.evaluated_teams:
#             print(f"Team {t.id}")

#             team_grades = [g[1] for g in t.grades]
#             own_team_grade = next((g[1] for g in t.grades if g[0] == e.id), None)

#             if team_grades and own_team_grade is not None:
#                 others_team_avg = sum(team_grades) / len(team_grades)

#                 variation = abs(others_team_avg - own_team_grade)
#                 t.deviation = variation  # Armazena o desvio na equipe avaliada
#                 t.avaliatorGrade = 10 - variation  # Atribui a nota ajustada para a equipe avaliada

#                 print(f"Team {t.id} - Deviation: {variation}, Adjusted Grade: {t.avaliatorGrade}")






def calculate_final_grades(teams: list[Team]):
    for t in teams:
        # Calculando a nota final de cada membro da equipe
        for m in t.members:
            m.finalGrade = m.content * 0.6 + t.avaliatorGrade * 0.4
            # Impressão da nota final de cada membro
            print(f"Final grade for {m.name}: {m.finalGrade} (content: {m.content}, team evaluator grade: {t.avaliatorGrade})")

 


def main():
    df = pd.read_excel(
        "C:/Users/User/Downloads/IA SIS_ Avaliação dos Painéis TESTE MARLON(1-4).xlsx"
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

    generate_deviations(teams)

    # for e in evaluators:
    #   print("ID da equipe:", e.id)
    #   print("Notas:", e.grades)
    #   print("Média:", e.avaliatorGrade)
    #   print("Desvio:", e.deviation)

    calculate_final_grades(teams)

main()
	