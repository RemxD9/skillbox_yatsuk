import requests
import sqlite3
import time
import threading


def get_star_wars_characters_sequential():
    conn = sqlite3.connect('star_wars_characters.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS characters
                      (id INTEGER PRIMARY KEY, name TEXT, age TEXT, gender TEXT)''')

    # Запрос 20 персонажей
    url = "https://swapi.dev/api/people/"
    for i in range(1, 22):
        if i == 17:
            continue
        response = requests.get(url + str(i))
        character_data = response.json()
        name = character_data['name']
        age = str(character_data['birth_year'].split('BBY')[0]) if character_data['birth_year'] != 'unknown' else None
        gender = character_data['gender']
        cursor.execute("INSERT INTO characters (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))

    conn.commit()
    conn.close()


def measure_time_sequential():
    start_time = time.time()
    get_star_wars_characters_sequential()
    end_time = time.time()
    print("Sequential Execution Time:", end_time - start_time, "seconds")


def measure_time_parallel():
    start_time = time.time()
    threads = []
    for _ in range(4):
        thread = threading.Thread(target=get_star_wars_characters_sequential)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()
    print("Parallel Execution Time:", end_time - start_time, "seconds")


if __name__ == "__main__":
    measure_time_sequential()
    measure_time_parallel()
