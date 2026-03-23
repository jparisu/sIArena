import unittest


class TestMeasurementsInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.measurements

        self.assertEqual(sIArena.measurements.__name__, "sIArena.measurements")
