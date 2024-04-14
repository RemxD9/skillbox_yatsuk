import sqlite3
import csv


def delete_wrong_fees(c: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            truck_number, date = row
            c.execute('delete from table_fees where timestamp = ? and truck_number = ?', (date, truck_number))


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()

        delete_wrong_fees(cursor, "wrong_fees.csv")
