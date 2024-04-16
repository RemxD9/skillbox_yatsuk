import sqlite3
from typing import List, Dict

DATA = [
    {'id': 0, 'title': 'A byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 2, 'title': 'Mar and Peace', 'author': 'Lev Tolstoy'},
]


class Book:
    def __init__(self, title: str, author: str, id: int = None, view_count: int = 0):
        self.id = id
        self.title = title
        self.author = author
        self.view_count = view_count

    def __getitem__(self, item):
        return getattr(self, item)

    def save(self):
        with sqlite3.connect('table_books.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO table_books (title, author) VALUES (?, ?)',
                (self.title, self.author)
            )
            conn.commit()

    @staticmethod
    def increasing_count(book):
        with sqlite3.connect('table_books.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE table_books SET view_count = view_count + 1 WHERE id = ?',
                (book[0],)
            )
            conn.commit()


def init_db(initial_records: List[Dict]):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='table_books';"
        )
        exists = cursor.fetchone()
        # Если таблицы нет, создаем ее и заполняем
        if not exists:
            exists = cursor.executescript(
                "CREATE TABLE 'table_books'"
                '(id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, view_count INT DEFAULT 0)'
            )
            cursor.executemany(
                'INSERT INTO table_books'
                '(title, author) VALUES (?, ?)',
                [(item['title'], item['author']) for item in initial_records]
                # Делаем записи
            )


def get_all_books() -> list[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from table_books')
        all_books = cursor.fetchall()
        for book in all_books:
            Book.increasing_count(book)
        return [Book(row[0], row[1], row[2]) for row in all_books]


def get_author_books(author_name):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from table_books where author=?', (author_name,))
        all_books = cursor.fetchall()
        for book in all_books:
            Book.increasing_count(book)
        return [Book(row[0], row[1], row[2]) for row in all_books]


def get_book_by_id_from_db(id):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * from table_books where id=?', (id,))
        all_books = cursor.fetchall()
        for book in all_books:
            Book.increasing_count(book)
        return [Book(row[0], row[1], row[2], row[3]) for row in all_books]


if __name__ == '__main__':
    init_db(DATA)
