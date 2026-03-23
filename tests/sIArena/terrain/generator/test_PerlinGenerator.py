import math
import unittest
from unittest.mock import patch

import numpy as np

from sIArena.terrain.generator.PerlinGenerator import PerlinGenerator


class TestPerlinGenerator(unittest.TestCase):
    def test_generate_random_matrix_uses_seeded_base_and_helper(self):
        generator = PerlinGenerator()

        with patch("sIArena.terrain.generator.PerlinGenerator.random.randint", return_value=7):
            with patch.object(PerlinGenerator, "perlin_value_generator", side_effect=lambda i, j, base, scale: i + j) as value_mock:
                matrix = generator.generate_random_matrix_(2, 3, abruptness=0.5, seed=9)

        self.assertTrue(np.array_equal(matrix, np.array([[0.0, 1.0, 2.0], [1.0, 2.0, 3.0]])))
        first_call = value_mock.call_args_list[0].args
        self.assertEqual(first_call[:3], (0, 0, 7))
        self.assertAlmostEqual(first_call[3], math.sqrt(6) / 12.5)

    def test_generate_random_matrix_clamps_zero_abruptness(self):
        generator = PerlinGenerator()

        with patch("sIArena.terrain.generator.PerlinGenerator.random.randint", return_value=1):
            with patch.object(PerlinGenerator, "perlin_value_generator", return_value=0) as value_mock:
                generator.generate_random_matrix_(1, 1, abruptness=0)

        self.assertGreater(value_mock.call_args.args[3], 1000)

    def test_perlin_value_generator_delegates_to_noise_library(self):
        with patch("sIArena.terrain.generator.PerlinGenerator.pnoise2", return_value=1.5) as noise_mock:
            value = PerlinGenerator.perlin_value_generator(2, 3, base=10, scale=5)

        self.assertEqual(value, 1.5)
        self.assertEqual(noise_mock.call_args.args, ((12 / 5), (13 / 5)))
        self.assertEqual(
            noise_mock.call_args.kwargs,
            {"persistence": 0.5, "octaves": 2, "lacunarity": 2.0},
        )
