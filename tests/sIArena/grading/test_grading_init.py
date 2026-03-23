import unittest


class TestGradingInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.grading

        self.assertEqual(sIArena.grading.__name__, "sIArena.grading")
