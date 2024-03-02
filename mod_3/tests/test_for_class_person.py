import unittest
from skillbox_yatsuk.mod_3.task_4 import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("John Doe", 1990, "123 Main St")

    def test_get_age(self):
        expected_age = 2024 - 1990
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "John Doe")

    def test_set_name(self):
        new_name = "Jane Doe"
        self.person.set_name(new_name)
        self.assertEqual(self.person.get_name(), new_name)

    def test_set_address(self):
        new_address = "456 Oak St"
        self.person.set_address(new_address)
        self.assertEqual(self.person.get_address(), new_address)

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), "123 Main St")

    def test_is_homeless_with_address(self):
        self.assertFalse(self.person.is_homeless())

    def test_is_homeless_without_address(self):
        homeless_person = Person("Homeless Joe", 1985)
        self.assertTrue(homeless_person.is_homeless())


if __name__ == '__main__':
    unittest.main()
