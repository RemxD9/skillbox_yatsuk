import unittest
from skillbox_yatsuk.mod_3.decrypt import decrypter


class TestDecoder(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_no_dots(self):
        with self.subTest(msg="No dots"):
            result = decrypter("абра-кадабра")
            self.assertEqual(result, "абра-кадабра")

    def test_single_dots(self):
        with self.subTest(msg="Single dots"):
            result = decrypter("абраа..-кадабра")
            self.assertEqual(result, "абра-кадабра")

            result = decrypter("абраа..-.кадабра")
            self.assertEqual(result, "абра-кадабра")

            result = decrypter("абра--..кадабра")
            self.assertEqual(result, "абра-кадабра")

    def test_multiple_dots(self):
        with self.subTest(msg="Multiple dots"):
            result = decrypter("абрау...-кадабра")
            self.assertEqual(result, "абра-кадабра")

            result = decrypter("абра........")
            self.assertEqual(result, "")

            result = decrypter("абр......a.")
            self.assertEqual(result, "a")

            result = decrypter("1..2.3")
            self.assertEqual(result, "23")

    def test_empty_input(self):
        with self.subTest(msg="Empty input"):
            result = decrypter(".")
            self.assertEqual(result, "")

            result = decrypter("1.......................")
            self.assertEqual(result, "")

            result = decrypter("")
            self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()
