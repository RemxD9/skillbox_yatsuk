import sqlite3


def check_if_vaccine_has_spoiled(cursor: sqlite3.Cursor, truck_number: str) -> bool:
    query = """
        SELECT COUNT(*) 
        FROM (
            SELECT 
                truck_number,
                SUM(CASE WHEN temperature_celsius NOT BETWEEN 16 AND 20 THEN 1 ELSE 0 END) AS out_of_range_count
            FROM table_truck_with_vaccine 
            GROUP BY truck_number
        ) AS subquery
        WHERE truck_number = ? AND out_of_range_count > 3
    """

    cursor.execute(query, (truck_number,))
    hours_out_of_range = cursor.fetchone()[0]
    print(hours_out_of_range)
    return hours_out_of_range <= 3


def getting_truck_number(c: sqlite3.Cursor) -> list:
    result = []
    c.execute("SELECT DISTINCT truck_number FROM table_truck_with_vaccine")
    trucks_numbers = c.fetchall()
    for number_tuple in trucks_numbers:
        number = number_tuple[0]
        vaccine_is_spoiled = check_if_vaccine_has_spoiled(c, number)
        result.append({number: vaccine_is_spoiled})
    return result


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as con:
        cursor = con.cursor()

    print(getting_truck_number(cursor))
