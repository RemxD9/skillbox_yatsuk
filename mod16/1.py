import sqlite3


conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE actors (
                    act_id INTEGER PRIMARY KEY,
                    act_first_name VARCHAR(50),
                    act_last_name VARCHAR(50),
                    act_gender VARCHAR(1)
                )''')

cursor.execute('''CREATE TABLE movie_cast (
                    mov_id INTEGER,
                    act_id INTEGER,
                    role VARCHAR(50),
                    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE,
                    FOREIGN KEY (act_id) REFERENCES actors(act_id) ON DELETE CASCADE
                )''')

cursor.execute('''CREATE TABLE movie (
                    mov_id INTEGER PRIMARY KEY,
                    mov_title VARCHAR(50)
                )''')

cursor.execute('''CREATE TABLE oscar_awarded (
                    award_id INTEGER PRIMARY KEY,
                    mov_id INTEGER,
                    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
                )''')

cursor.execute('''CREATE TABLE movie_director (
                    dir_id INTEGER,
                    mov_id INTEGER,
                    FOREIGN KEY (dir_id) REFERENCES director(dir_id) ON DELETE CASCADE,
                    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
                )''')

cursor.execute('''CREATE TABLE director (
                    dir_id INTEGER PRIMARY KEY,
                    dir_last_name VARCHAR(50),
                    dir_first_name VARCHAR(50)
                )''')

conn.commit()
conn.close()
