import unittest
import sys
from io import StringIO
from skillbox_yatsuk.mod_5.task4 import Redirect


class TestRedirect(unittest.TestCase):
    def test_redirect_both_streams(self):
        with StringIO() as stdout, StringIO() as stderr:
            with Redirect(stdout=stdout, stderr=stderr):
                print('Hello stdout')
                print('Hello stderr', file=sys.stderr)

            self.assertEqual(stdout.getvalue(), 'Hello stdout\n')
            self.assertEqual(stderr.getvalue(), 'Hello stderr\n')

    def test_redirect_stdout_only(self):
        with StringIO() as stdout:
            with Redirect(stdout=stdout):
                print('Hello stdout')

            self.assertEqual(stdout.getvalue(), 'Hello stdout\n')

    def test_redirect_stderr_only(self):
        with StringIO() as stderr:
            with Redirect(stderr=stderr):
                print('Hello stderr', file=sys.stderr)

            self.assertEqual(stderr.getvalue(), 'Hello stderr\n')

    def test_no_redirect(self):
        with StringIO() as stdout, StringIO() as stderr:
            with Redirect():
                print('Hello stdout')
                print('Hello stderr', file=sys.stderr)

            self.assertEqual(stdout.getvalue(), '')
            self.assertEqual(stderr.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
