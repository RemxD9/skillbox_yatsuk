import unittest
from skillbox_yatsuk.mod_5.task2 import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_timeout_below_execution_time(self):
        # Тест на случай, когда тайм-аут меньше времени выполнения
        data = {
            'code': f"import time\nprint('Start')\ntime.sleep(5)\nprint('Finish')",
            'timeout': 2
        }
        response = self.app.post('/execute_code', data=data)
        self.assertIn(b'Execution timed out', response.data)

    def test_invalid_form_data(self):
        # Тест на случай, когда введены некорректные данные в форме
        data = {'invalid_field': 'invalid_value'}
        response = self.app.post('/execute_code', data=data)
        self.assertIn(b'Invalid input', response.data)

    def test_unsafe_input_code(self):
        data = {'code': "from subprocess import run\nrun(['./kill_the_system.sh'])", 'timeout': 10}
        response = self.app.post('/execute_code', data=data)
        self.assertIn(b'Execution failed with error', response.data)


if __name__ == '__main__':
    unittest.main()
