import unittest
from skillbox_yatsuk.mod_4.task1_2 import app


class RegistrationFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_valid_registration_form(self):
        valid_data = {
            'email': 'test@example.com',
            'phone': 1234567890,
            'name': 'John Doe',
            'address': '123 Main St',
            'index': 12345,
            'comment': 'Some comment'
        }
        response = self.app.post('/registration', data=valid_data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_registration_form(self):
        invalid_data = {
            'email': 'invalid_email',
            'phone': 'invalid phone',
            'name': '',
            'address': '',
            'index': 'invalid index',
            'comment': 'Some comment'
        }
        response = self.app.post('/registration', data=invalid_data)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
