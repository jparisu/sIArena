import unittest

import numpy as np

from sIArena.utils.math_utils import scalade


class TestMathUtils(unittest.TestCase):
    def test_scalade_scales_values_into_new_range(self):
        array = np.array([1.0, 2.0, 3.0])

        scaled = scalade(array, 10, 20)

        self.assertTrue(np.allclose(scaled, np.array([10.0, 15.0, 20.0])))

    def test_scalade_returns_original_array_when_all_values_match(self):
        array = np.array([7.0, 7.0, 7.0])

        scaled = scalade(array, 0, 1)

        self.assertIs(scaled, array)
