import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('hw.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO `table_users` (username, password)
            VALUES ('{username}', '{password}')"""
        )
        conn.commit()


def hack() -> None:
    username: str = "GRANT DROP ON table_name TO user_name;', 500);"
    password: str = "xD"
    register(username, password)


if __name__ == '__main__':
    hack()
