import random
import sqlite3
from datetime import datetime, timedelta


def get_week_day(day: int) -> str:
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days_of_week[(day - 1) % 7]


def generate_employees(number_of_employees: int) -> list:
    preferences = ["Football", "Hockey", "Chess", "SUP-Surfing", "Boxing", "Dota2", "ChessBoxing"]
    employees = [(f"Employee{i+1}", random.choice(preferences)) for i in range(number_of_employees)]
    return employees


def update_work_schedule(c: sqlite3.Cursor) -> None:
    # таблицы не существует, создадим пустую
    c.execute('CREATE TABLE IF NOT EXISTS table_work_schedule (id INTEGER PRIMARY KEY, day INTEGER, employee TEXT)')
    c.execute('DELETE FROM table_work_schedule')

    employees = generate_employees(366)

    days_of_week = {
        "Monday": "Football",
        "Tuesday": "Hockey",
        "Wednesday": "Chess",
        "Thursday": "SUP-Surfing",
        "Friday": "Boxing",
        "Saturday": "Dota2",
        "Sunday": "ChessBoxing"
    }
    current_date = datetime(2022, 1, 1)
    days = [current_date + timedelta(days=i) for i in range(366)]

    for day in days:
        day_of_week = day.strftime("%A")
        preference = days_of_week[day_of_week]
        suitable_employees = [(employee, pref) for employee, pref in employees if pref == preference]
        selected_employees = random.sample(suitable_employees, k=10)
        for employee, _ in selected_employees:
            cursor.execute("INSERT INTO table_work_schedule (day, employee) VALUES (?, ?)", (day.strftime("%Y-%m-%d"), employee))


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as con:
        cursor = con.cursor()

        update_work_schedule(cursor)
