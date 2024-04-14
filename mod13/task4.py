import sqlite3


def ivan_sovin_the_most_effective(c: sqlite3.Cursor, name: str, manager_salary: int) -> None:
    c.execute('select salary from table_effective_manager where name = ?', (name,))
    employee_salary = c.fetchone()[0]
    if employee_salary * 1.1 > manager_salary:
        print("Employee is dismissed")
        c.execute("DELETE FROM table_effective_manager WHERE name = ?", (name,))
    else:
        c.execute('update table_effective_manager set salary = ? where name = ?', (employee_salary * 1.1, name))
    print('Operation completed successfully')


if __name__ == "__main__":
    with sqlite3.connect('hw.db') as con:
        names = []
        cursor = con.cursor()
        cursor.execute('Select name from table_effective_manager')
        result = [', '.join(tup) for tup in cursor.fetchall()]
        for person in result[1:]:
            names.append(person)
        cursor.execute('select max(salary) from table_effective_manager')
        sovins_salary = cursor.fetchone()[0]

        for name in names:
            ivan_sovin_the_most_effective(cursor, str(name), sovins_salary)


