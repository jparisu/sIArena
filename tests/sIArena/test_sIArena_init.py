import unittest


class TestSIArenaInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena

        self.assertEqual(sIArena.__name__, "sIArena")
