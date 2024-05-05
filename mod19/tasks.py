import sqlite3
import pandas as pd  # Запросы конечно хорошо, но вот они очень уж не красивые


def task1(cursor):
    cursor.execute(''' SELECT t.full_name, avg(ag.grade) as 'average_grade'
                        FROM assignments a
                        INNER JOIN teachers t ON a.teacher_id = t.teacher_id
                        JOIN main.assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                        group by t.full_name
                        order by average_grade
                        limit 1''')
    return cursor.fetchone()


def task2(cursor):
    cursor.execute('''SELECT s.full_name, avg(grade) as 'average_grade'
                        FROM assignments_grades a
                        INNER JOIN students s ON a.student_id = s.student_id
                        group by s.full_name
                        order by average_grade desc, s.full_name ASC
                        limit 10''')
    return pd.DataFrame(cursor.fetchall(), columns=['Student_name', 'Average_grade']).to_string(index=False)


def task3(cursor):
    cursor.execute('''SELECT s.full_name
FROM students s
JOIN assignments_grades ag ON s.student_id = ag.student_id
JOIN (
    SELECT assisgnment_id, teacher_id
    FROM assignments
    WHERE assisgnment_id IN (
        SELECT assisgnment_id
        FROM assignments_grades
        GROUP BY assisgnment_id
        ORDER BY AVG(grade) ASC
        LIMIT 1
    )
) a ON ag.assisgnment_id = a.assisgnment_id;
''')
    return pd.DataFrame(cursor.fetchall(), columns=['Student_name']).to_string(index=False)


def task4(cursor):
    cursor.execute('''SELECT 
    *,
    (SELECT MIN(total_overdue_assignments) FROM (
        SELECT
            a.group_id,
            COUNT(g.assisgnment_id) AS total_assignments,
            SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS total_overdue_assignments
        FROM
            assignments a
        LEFT JOIN
            assignments_grades g ON a.assisgnment_id = g.assisgnment_id
        GROUP BY
            a.group_id
    ) AS subquery) AS min_total_overdue_assignments,
    (SELECT MAX(total_overdue_assignments) FROM (
        SELECT
            a.group_id,
            COUNT(g.assisgnment_id) AS total_assignments,
            SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS total_overdue_assignments
        FROM
            assignments a
        LEFT JOIN
            assignments_grades g ON a.assisgnment_id = g.assisgnment_id
        GROUP BY
            a.group_id
    ) AS subquery) AS max_total_overdue_assignments
FROM (
    SELECT
        a.group_id,
        COUNT(g.assisgnment_id) AS total_assignments,
        SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS total_overdue_assignments,
        AVG(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS average_overdue_assignments
    FROM
        assignments a
    LEFT JOIN
        assignments_grades g ON a.assisgnment_id = g.assisgnment_id
    GROUP BY
        a.group_id
) AS main_query;
        ''')
    return (pd.DataFrame(cursor.fetchall(), columns=['Номер группы', 'Всего заданий', 'Количество просроченных заданий',
                                                     'Среднее количество просроченных заданий', 'Минимум', 'Максимум'])
            .to_string(index=False))


def task5(cursor):
    cursor.execute('''SELECT 
    s.group_id,
    COUNT(DISTINCT s.student_id) AS total_students,
    AVG(g.grade) AS average_grade,
    SUM(CASE WHEN g.grade IS NULL THEN 1 ELSE 0 END) AS students_without_grade,
    SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS students_with_overdue_assignments,
    SUM(CASE WHEN attempts > 1 THEN 1 ELSE 0 END) AS students_with_multiple_attempts
FROM
    students s
LEFT JOIN
    (
        SELECT
            student_id,
            assisgnment_id,
            COUNT(DISTINCT date) AS attempts
        FROM
            assignments_grades
        GROUP BY
            student_id,
            assisgnment_id
    ) AS attempts ON s.student_id = attempts.student_id
LEFT JOIN
    assignments_grades g ON s.student_id = g.student_id AND attempts.assisgnment_id = g.assisgnment_id
LEFT JOIN
    assignments a ON g.assisgnment_id = a.assisgnment_id
GROUP BY
    s.group_id;
                    ''')
    return pd.DataFrame(cursor.fetchall(), columns=['Номер группы', 'Всего студентов', 'Средний балл по группе', 'Студенты без оценки', 'Студенты с просроченными дедлайнами', 'Количество пересдач студентов в группе']).to_string(index=False)


def task6(cursor):
    cursor.execute('''SELECT 
    AVG(g.grade) AS average_grade_for_reading_and_memorizing
FROM
    assignments a
JOIN
    (
        SELECT
            assisgnment_id
        FROM
            assignments
        WHERE
            assignment_text LIKE '%прочитать%' OR assignment_text LIKE '%выучить%'
    ) AS reading_memorizing_tasks ON a.assisgnment_id = reading_memorizing_tasks.assisgnment_id
JOIN
    assignments_grades g ON a.assisgnment_id = g.assisgnment_id;
''')
    return cursor.fetchone()


if __name__ == '__main__':
    connection = sqlite3.connect('homework.sqlite')
    cursor = connection.cursor()
    print('Задание № 1')
    print(f'\nИмя преподавателя - {task1(cursor)[0]}, средний балл его обучающихся по заданиям составляет: '
          f'{task1(cursor)[1]}\n')
    print('Задание № 2')
    print(f'\n{task2(cursor)}\n')
    print('Задание № 3')
    print(f'\n{task3(cursor)}\n')
    print('Задание № 4')
    print(f'\n{task4(cursor)}\n')
    print('Задание № 5')
    print(f'\n{task5(cursor)}\n')
    print('Задание № 6')
    print(f'\nСредний балл за задания, где надо что-то почитать или выучить - {task6(cursor)[0]}\n')
