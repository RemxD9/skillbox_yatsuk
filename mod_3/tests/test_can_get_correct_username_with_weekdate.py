import unittest
from unittest.mock import patch
from freezegun import freeze_time
from skillbox_yatsuk.mod_3.hello_name import app
from skillbox_yatsuk.mod_3.hello_name import weekdays_translator


class TestHelloWorldEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    @freeze_time("2024-03-04 12:00:00")
    def test_hello_world_greeting(self):
        username = 'TestName'
        weekdays = range(0, 6)
        with patch('skillbox_yatsuk.mod_3.hello_name.datetime') as mock_datetime:
            for weekday in weekdays:
                mock_datetime.today().weekday.return_value = weekday
                response = self.app.get(self.base_url + username)
                expected_greeting = f'Привет, {username}! {weekdays_translator[weekday]}'
                self.assertEqual(response.data.decode('utf-8'), expected_greeting)


if __name__ == '__main__':
    unittest.main()
