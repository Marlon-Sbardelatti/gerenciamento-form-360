import csv
import pandas as pd

from models.user import User


def create_user(df: pd.DataFrame) -> list[User]:
    users_content = []
    for _, row in df.iterrows():
        if not (users_content.__contains__(row.iloc[5])):
            users_content.append(row.iloc[5])

    users = []
    for c in users_content:
        users.append(User(name=c))

    return users


def create_grades_per_user(df: pd.DataFrame, users: list[User]):
    for u in users:
        for _, row in df.iterrows():
            if row.iloc[5] == u.name:
                totalGrades = 0
                for grade in row.iloc[6:12]:
                    totalGrades += grade
                avg = totalGrades / 6
                u.grades.append(avg)


def generate_avg(users: list[User]):
    for u in users:
        total = 0
        for g in u.grades:
            total += g
        u.average = total / len(u.grades)


def save_final_grades_to_csv(users: list[User], filename="final_grades_360.csv"):
    students = []

    for u in users:
        students.append(
            {
                "name": u.name,
                "final_grade": u.average,
            }
        )

    students.sort(key=lambda x: x["name"])

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Nome", "Media"])

        for student in students:
            writer.writerow(
                [
                    student["name"],
                    f"{student['final_grade']:.2f}"
                    if student["final_grade"] is not None
                    else "",
                ]
            )


def main():
    df = pd.read_excel(
        "/home/hetzwga/Downloads/IA SIS_ Avaliação 360º -SEMINÁRIOS (TESTE)(1-16).xlsx"
    )

    users = create_user(df)

    create_grades_per_user(df, users)

    generate_avg(users)

    # for u in users:
    #     print(u.name, u.average)

    save_final_grades_to_csv(users)


main()
