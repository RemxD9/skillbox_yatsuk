import unittest
from unittest.mock import patch
from skillbox_yatsuk.mod_3.hello_name import app
from skillbox_yatsuk.mod_3.hello_name import weekdays_translator


class TestHelloWorldEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_hello_world_endpoint_with_incorrect_name(self):
        usernames = list(weekdays_translator.values())  # Получаем ключи, а не значения
        with patch('skillbox_yatsuk.mod_3.hello_name.datetime') as mock_datetime:
            for i in range(len(usernames)):
                username = usernames[i]
                mock_datetime.today().weekday.return_value = i
                response = self.app.get(self.base_url + username)
                expected_greeting = f'Привет, неизвестный пользователь! {weekdays_translator[i]}'
                self.assertEqual(response.data.decode('utf-8'), expected_greeting)


if __name__ == '__main__':
    unittest.main()
