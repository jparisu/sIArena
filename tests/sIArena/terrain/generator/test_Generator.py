import unittest

import numpy as np

from sIArena.terrain.generator.Generator import TerrainGenerator


class RecordingTerrain:
    def __init__(self, matrix, origin=None, destination=None, cost_function=None):
        self.matrix = matrix
        self.origin = origin
        self.destination = destination
        self.cost_function = cost_function


class StubGenerator(TerrainGenerator):
    def __init__(self):
        self.calls = []

    def generate_random_matrix_(self, n, m, abruptness=0.5, seed=None):
        self.calls.append(
            {"n": n, "m": m, "abruptness": abruptness, "seed": seed}
        )
        return np.array([[0.0, 0.5], [1.0, 0.25]])


class TestTerrainGenerator(unittest.TestCase):
    def test_generate_random_terrain_clamps_abruptness_and_builds_terrain(self):
        generator = StubGenerator()

        terrain = generator.generate_random_terrain(
            n=2,
            m=7,
            min_height=10,
            max_height=19,
            min_step=3,
            abruptness=2,
            seed=9,
            origin=(0, 0),
            destination=(1, 1),
            terrain_ctor=RecordingTerrain,
        )

        self.assertEqual(generator.calls, [{"n": 2, "m": 7, "abruptness": 1, "seed": 9}])
        self.assertTrue(np.array_equal(terrain.matrix, np.array([[30, 24], [18, 27]])))
        self.assertEqual(terrain.origin, (0, 0))
        self.assertEqual(terrain.destination, (1, 1))
        self.assertIsNone(terrain.cost_function)

    def test_generate_random_terrain_passes_custom_cost_function(self):
        generator = StubGenerator()
        cost_function = lambda start, end: 42

        terrain = generator.generate_random_terrain(
            n=2,
            m=2,
            cost_function=cost_function,
            terrain_ctor=RecordingTerrain,
        )

        self.assertIs(terrain.cost_function, cost_function)

    def test_base_generate_random_matrix_is_pure_virtual(self):
        with self.assertRaisesRegex(NotImplementedError, "must be implemented from a child class"):
            TerrainGenerator().generate_random_matrix_(1, 1)
