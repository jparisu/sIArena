import unittest


class TestGeneratorInit(unittest.TestCase):
    def test_import_module(self):
        import sIArena.terrain.generator

        self.assertEqual(sIArena.terrain.generator.__name__, "sIArena.terrain.generator")
