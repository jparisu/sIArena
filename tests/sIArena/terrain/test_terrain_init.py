import unittest


class TestTerrainInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.terrain

        self.assertEqual(sIArena.terrain.__name__, "sIArena.terrain")
