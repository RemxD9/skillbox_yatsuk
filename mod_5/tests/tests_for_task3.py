import unittest
from skillbox_yatsuk.mod_5.task3 import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_ignore_child_errors(self):
        with BlockErrors({ZeroDivisionError}):
            with self.assertRaises(ZeroDivisionError):
                a = 1 / 0

    def test_ignore_error(self):
        with BlockErrors({ZeroDivisionError}):
            with self.assertRaises(ZeroDivisionError):
                a = 1 / 0

    def test_nested_blocks(self):
        with BlockErrors({ZeroDivisionError}):
            with self.assertRaises(ZeroDivisionError):
                a = 1 / 0
            print('Внутренний блок: выполнено без ошибок')
        print('Внешний блок: выполнено без ошибок')

    def test_propagate_error(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0


if __name__ == '__main__':
    unittest.main()
