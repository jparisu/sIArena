import unittest
from unittest.mock import patch

import numpy as np

from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator


class TestFocusedGenerator(unittest.TestCase):
    def test_generate_random_matrix_uses_focused_values_to_fill_grid(self):
        generator = FocusedGenerator()

        with patch.object(FocusedGenerator, "focused_value_generator", side_effect=[2, 3, 4]) as value_mock:
            matrix = generator.generate_random_matrix_(2, 2, abruptness=0.5)

        self.assertTrue(np.array_equal(matrix, np.array([[1.0, 2.0], [3.0, 4.0]])))
        self.assertEqual(value_mock.call_args_list[0].args, ([1.0], 0.5))
        self.assertEqual(value_mock.call_args_list[1].args, ([1.0], 0.5))
        self.assertEqual(value_mock.call_args_list[2].args, ([2.0, 3.0], 0.5))

    def test_generate_random_matrix_is_reproducible_with_seed(self):
        generator = FocusedGenerator()

        matrix_a = generator.generate_random_matrix_(3, 3, abruptness=0.2, seed=4)
        matrix_b = generator.generate_random_matrix_(3, 3, abruptness=0.2, seed=4)

        self.assertTrue(np.array_equal(matrix_a, matrix_b))

    def test_focused_value_generator_builds_value_range_from_sources(self):
        with patch("sIArena.terrain.generator.FocusedGenerator.random.choice", side_effect=lambda values: values[-1]) as choice_mock:
            value = FocusedGenerator.focused_value_generator([2.0, 4.0], 0.5, possibilities=5)

        self.assertEqual(choice_mock.call_args.args[0], [0.5, 1.75, 3.0, 4.25, 5.5])
        self.assertEqual(value, 5.5)
