import time
import unittest

from sIArena.utils.threading_utils import run_function_with_timeout


class TestThreadingUtils(unittest.TestCase):
    def test_returns_function_result_before_timeout(self):
        self.assertEqual(run_function_with_timeout(lambda: 7, 0.1), 7)

    def test_returns_none_when_timeout_expires(self):
        def slow():
            time.sleep(0.05)
            return 9

        self.assertIsNone(run_function_with_timeout(slow, 0.001))
