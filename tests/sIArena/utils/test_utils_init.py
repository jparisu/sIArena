import unittest


class TestUtilsInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.utils

        self.assertEqual(sIArena.utils.__name__, "sIArena.utils")
