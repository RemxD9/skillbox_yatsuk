import sqlite3
import random

# изначальные команды участницы
STRONG_TEAMS = ["Real Madrid", "Barcelona", "Bayern Munich", "Liverpool"]
MEDIUM_TEAMS = ["Atletico Madrid", "Manchester City", "Juventus", "Chelsea"]
WEAK_TEAMS = ["Sevilla", "Borussia Dortmund", "Inter Milan", "Arsenal", "Zenit", "Manchester United", "Real Betis",
              "Paris saint-german"]


def generate_test_data(c: sqlite3.Cursor, number_of_groups: int) -> None:
    teams = []
    for name, country in zip(STRONG_TEAMS,["Spain", "Spain", "Germany", "England"]):
        teams.append((name, country, "Strong"))
    for name, country in zip(MEDIUM_TEAMS,["Spain", "England", "Italy", "England"]):
        teams.append((name, country, "Medium"))
    for name, country in zip(WEAK_TEAMS, ["Spain", "Germany", "Italy", "England", "Russia", "England", "Spain", "France"]):
        teams.append((name, country, "Weak"))
    random.shuffle(teams)

    draw_results = []
    copy_teams = teams.copy()
    for i in range(number_of_groups):
        strong_team = random.choice([team for team in copy_teams if team[2] == 'Strong'])
        copy_teams.remove(strong_team)
        medium_team = random.choice([team for team in copy_teams if team[2] == 'Medium'])
        copy_teams.remove(medium_team)
        weak_team1 = random.choice([team for team in copy_teams if team[2] == 'Weak'])
        copy_teams.remove(weak_team1)
        weak_team2 = random.choice([team for team in copy_teams if team[2] == 'Weak'])
        copy_teams.remove(weak_team2)
        draw_results.append([strong_team, medium_team, weak_team1, weak_team2, i+1])

    result_with_group_numbers = []
    for group in draw_results:
        group_number = group[-1]
        teams_in_group = group[:-1]
        result_with_group_numbers.extend([(team[0], group_number) for team in teams_in_group])

    insert_teams_query = "INSERT INTO uefa_commands (command_name, command_country, command_level) VALUES (?, ?, ?)"
    insert_draw_results_query = "INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?)"

    # Вставка данных в таблицы с использованием метода executemany
    cursor.executemany(insert_teams_query, teams)
    cursor.executemany(insert_draw_results_query, result_with_group_numbers)


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as con:
        cursor = con.cursor()
        generate_test_data(cursor, 4)




