import sqlite3

with sqlite3.connect('hw_4_database.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT (SELECT COUNT(salary) FROM salaries WHERE salary < 5000) AS people_below_poverty_line,"
                    "ROUND(AVG(salary), 2) AS average_salary,"
                    "(SELECT salary FROM salaries ORDER BY salary LIMIT 1 OFFSET (SELECT COUNT(salary) / 2 FROM salaries)) AS median_salary,"
                    "ROUND((SELECT SUM(salary) FROM salaries ORDER BY salary DESC LIMIT (SELECT COUNT(salary) * 0.1 FROM salaries)) / (SELECT SUM(salary) FROM salaries ORDER BY salary ASC LIMIT (SELECT COUNT(salary) * 0.9 FROM salaries)), 2) FROM salaries")
    people_below_poverty_line, average_salary, median_salary, social_inequality_percentage = cursor.fetchone()
    print(f'{people_below_poverty_line} человек с острова N находятся за чертой бедности, то есть получает меньше 5000 гульденов в год')
    print(f'{average_salary} средняя зарплата по острову N')
    print(f'{median_salary} медианная зарплата по острову')
    print(f'{social_inequality_percentage} - число социального неравенства')

conn.close()