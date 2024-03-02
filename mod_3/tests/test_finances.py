import unittest
from skillbox_yatsuk.mod_3.finances import app, storage


class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        storage.clear()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_add_expense_valid_date(self):
        response = self.app.get('/add/20220304/150')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Добавлена трата за 4.3.2022: 150 рублей, (наверное)')

    def test_add_expense_invalid_date(self):
        response = self.app.get('/add/2022-03-04/150')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Ошибка даты 2022-03-04 не существует')

    def test_add_expense_invalid_number_format(self):
        response = self.app.get('/add/20220304/abc')
        self.assertEqual(response.status_code, 404)

    def test_calculate_year(self):
        self.app.get('/add/20220301/100')
        self.app.get('/add/20220302/150')
        response = self.app.get('/calculate/2022')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'year': 2022, 'total expense': 250.0})

    def test_calculate_month(self):
        self.app.get('/add/20220301/100')
        self.app.get('/add/20220302/150')
        response = self.app.get('/calculate/2022/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'year': 2022, 'month': 3, 'total expense': 250.0})

    def test_calculate_month_with_negative_numbers(self):
        self.app.get('/add/20230301/-100')
        self.app.get('/add/20230302/-150')
        response = self.app.get('/calculate/2023/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'year': 2023, 'month': 3, 'total expense': 0})

    def test_calculate_year_with_string_numbers(self):
        self.app.get('/add/20210301/one')
        self.app.get('/add/20210302/150')
        response = self.app.get('/calculate/2021')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'year': 2021, 'total expense': 150.0})


if __name__ == '__main__':
    unittest.main()
