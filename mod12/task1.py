import requests
import sqlite3
import time
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_star_wars_characters():
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
        logger.info(f'added to db {name} {age} {gender}')

    conn.commit()
    conn.close()
    return 'Ok'


def thread_pool():
    logger.info('Starting thread_pool func')
    threads_pool = ThreadPool(processes=cpu_count())
    start_time = time.time()
    result = threads_pool.apply(get_star_wars_characters)
    threads_pool.close()
    threads_pool.join()
    end_time = time.time()
    logger.info(result)
    logger.info(f'Time of thread pool = {end_time - start_time}')


def pool():
    logger.info('Starting pool func')
    pool = Pool(processes=cpu_count())
    start_time = time.time()
    result = pool.apply(get_star_wars_characters)
    pool.close()
    pool.join()
    end_time = time.time()
    logger.info(result)
    logger.info(f'Time of pool = {end_time - start_time}')


if __name__ == '__main__':
    logger.info('Starts')
    pool()
    thread_pool()
    logger.info('Finished')
