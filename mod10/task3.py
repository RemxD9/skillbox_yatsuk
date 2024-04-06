import sqlite3

if __name__ == '__main__':
    with sqlite3.connect('hw_3_database.db') as connection:
        cursor = connection.cursor()
        for i in ['table_1', 'table_2', 'table_3']:
            cursor.execute(f"select count(*) from '{i}'")
            result1 = cursor.fetchone()[0]
            print(f'В таблице {i} хранится {result1} записей')

        cursor.execute("SELECT COUNT(DISTINCT value) FROM 'table_1'")
        result2 = cursor.fetchone()[0]
        print(f'В таблице table_1 хранится {result2} уникальных записей')
        # Не понятно, что имеется ввиду под "Как много записей из таблицы table_1 встречается в table_2?" Записей, у которых все поля совпадают или же нет?
        # В комментах оставлю запросы на случай, если только одно поле совпадает

        cursor.execute("SELECT COUNT(*) FROM table_1 t1 INNER JOIN table_2 t2 ON t1.id = t2.id AND t1.value = t2.value")
        # SELECT COUNT(*) FROM table_1 t1 INNER JOIN table_2 t2 ON t1.value = t2.value
        result3 = cursor.fetchone()[0]
        print(f'{result3} записей из таблицы table_1 встречается в table_2')

        cursor.execute("SELECT COUNT(*) FROM table_1 t1 INNER JOIN table_2 t2 ON t1.id = t2.id AND t1.value = t2.value INNER JOIN table_3 t3 ON t1.id = t3.id AND t1.value = t3.value")
        # SELECT COUNT(*) FROM table_1 t1 INNER JOIN table_2 t2 ON t1.value = t2.value INNER JOIN table_3 t3 ON t1.value = t3.value
        result4 = cursor.fetchone()[0]
        print(f'{result4} записей из таблицы table_1 встречается и в table_2, и в table_3')

    connection.close()
