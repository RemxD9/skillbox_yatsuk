import datetime
import sqlite3


def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str) -> None:
    query = "INSERT INTO bird_journal (bird_name, date_time) VALUES (?, ?)"
    cursor.execute(query, (bird_name, date_time))


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    query = "SELECT EXISTS(SELECT 1 FROM bird_journal WHERE bird_name = ? LIMIT 1)"
    cursor.execute(query, (bird_name,))
    result = cursor.fetchone()[0]

    return bool(result)


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name = input("Пожалуйста введите имя птицы\n> ")
    count_str = input("Сколько птиц вы увидели?\n> ")
    count = int(count_str)
    right_now = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("hw.db") as connection:
        cursor = connection.cursor()
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
