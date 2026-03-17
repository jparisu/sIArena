import unittest


class TestPlotInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.terrain.plot

        self.assertEqual(sIArena.terrain.plot.__name__, "sIArena.terrain.plot")
