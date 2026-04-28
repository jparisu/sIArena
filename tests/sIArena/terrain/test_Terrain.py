import unittest

import numpy as np

from sIArena.terrain.Terrain import (
    MultiEndpointTerrain,
    MultipleDestinationTerrain,
    NoPathTerrain,
    SequentialDestinationTerrain,
    Terrain,
    default_cost_function,
)


class TestDefaultCostFunction(unittest.TestCase):
    def test_same_height_costs_one(self):
        self.assertEqual(default_cost_function(3, 3), 1)

    def test_going_down_costs_height_difference(self):
        self.assertEqual(default_cost_function(5, 2), 3)

    def test_going_up_costs_double_height_difference(self):
        self.assertEqual(default_cost_function(2, 5), 6)


class TestNoPathTerrain(unittest.TestCase):
    def setUp(self):
        self.terrain = NoPathTerrain([[1, 2], [3, 4]])

    def test_init_converts_matrix_to_numpy_array(self):
        self.assertIsInstance(self.terrain.matrix, np.ndarray)
        self.assertNotIsInstance(self.terrain.matrix, np.matrix)

    def test_str_and_repr_render_grid(self):
        text = str(self.terrain)

        self.assertIn("| 1 | 2 |", text)
        self.assertEqual(repr(self.terrain), text)

    def test_len_and_size_use_matrix_dimensions(self):
        self.assertEqual(len(self.terrain), 4)
        self.assertEqual(self.terrain.size(), (2, 2))

    def test_getitem_reads_matrix_value(self):
        self.assertEqual(self.terrain[(1, 0)], 3)

    def test_get_neighbors_returns_cardinal_neighbors(self):
        self.assertEqual(self.terrain.get_neighbors((0, 0)), [(1, 0), (0, 1)])
        self.assertEqual(self.terrain.get_neighbors((1, 1)), [(0, 1), (1, 0)])

    def test_get_cost_and_path_cost_use_cost_function(self):
        self.assertEqual(self.terrain.get_cost((0, 0), (0, 1)), 2)
        self.assertEqual(self.terrain.get_path_cost([(0, 0), (0, 1), (1, 1)]), 6)

    def test_valid_path_helpers_delegate_to_why_valid_path(self):
        path = [(0, 0), (0, 1), (1, 1)]

        self.assertTrue(self.terrain.is_valid_path(path))
        self.assertTrue(self.terrain.is_complete_path(path))
        self.assertEqual(self.terrain.why_complete_path(path), (True, "Valid path"))

    def test_why_valid_path_rejects_empty_and_non_neighbor_steps(self):
        self.assertEqual(self.terrain.why_valid_path([]), (False, "Empty path"))
        self.assertEqual(
            self.terrain.why_valid_path([(0, 0), (1, 1)]),
            (False, "Invalid path: (0, 0) -> (1, 1)"),
        )

    def test_get_destinations_returns_none(self):
        self.assertIsNone(self.terrain.get_destinations())


class TestTerrain(unittest.TestCase):
    def setUp(self):
        self.terrain = Terrain([[1, 2], [3, 4]])

    def test_default_origin_and_destination(self):
        self.assertEqual(self.terrain.origin, (0, 0))
        self.assertEqual(self.terrain.destination, (1, 1))
        self.assertEqual(self.terrain.get_destinations(), [(1, 1)])

    def test_complete_path_must_start_and_end_correctly(self):
        self.assertTrue(self.terrain.is_complete_path([(0, 0), (0, 1), (1, 1)]))
        self.assertEqual(
            self.terrain.why_complete_path([(0, 1), (1, 1)]),
            (False, "Path does not start in the origin (0, 0)"),
        )
        self.assertEqual(
            self.terrain.why_complete_path([(0, 0), (0, 1)]),
            (False, "Path does not end in the destination (1, 1)"),
        )

    def test_str_marks_origin_and_destination(self):
        text = str(self.terrain)

        self.assertIn("|O 1 ", text)
        self.assertIn("|X 4 ", text)

    def test_out_of_bounds_coordinates_are_not_rejected_by_current_checks(self):
        terrain = Terrain([[1]], origin=(-1, 0), destination=(2, 0))

        self.assertEqual(terrain.origin, (-1, 0))
        self.assertEqual(terrain.destination, (2, 0))


class TestMultipleDestinationTerrain(unittest.TestCase):
    def setUp(self):
        self.terrain = MultipleDestinationTerrain(
            [[1, 2], [3, 4]],
            origin=(0, 0),
            destination={(0, 1), (1, 1)},
        )

    def test_complete_path_requires_all_destinations(self):
        self.assertTrue(self.terrain.is_complete_path([(0, 0), (0, 1), (1, 1)]))
        valid, message = self.terrain.why_complete_path([(0, 0), (1, 0), (1, 1)])

        self.assertFalse(valid)
        self.assertIn("Path does not go through the destination", message)

    def test_str_marks_origin_and_all_destinations(self):
        text = str(self.terrain)

        self.assertIn("|O 1 ", text)
        self.assertGreaterEqual(text.count("|X "), 1)

    def test_get_destinations_returns_destination_set(self):
        self.assertEqual(self.terrain.get_destinations(), {(0, 1), (1, 1)})

    def test_rejects_destination_equal_to_origin(self):
        with self.assertRaisesRegex(AttributeError, "Destination is the origin"):
            MultipleDestinationTerrain([[1]], origin=(0, 0), destination={(0, 0)})


class TestMultiEndpointTerrain(unittest.TestCase):
    def setUp(self):
        self.terrain = MultiEndpointTerrain(
            [[1, 2, 3], [4, 5, 6]],
            origin={(0, 0), (1, 0)},
            destination={(0, 2), (1, 2)},
        )

    def test_default_origin_and_destination_sets(self):
        terrain = MultiEndpointTerrain([[1, 2], [3, 4]])

        self.assertEqual(terrain.get_origins(), {(0, 0)})
        self.assertEqual(terrain.get_destinations(), {(1, 1)})

    def test_single_coordinate_inputs_are_normalized_to_sets(self):
        terrain = MultiEndpointTerrain(
            [[1, 2], [3, 4]],
            origin=(1, 0),
            destination=(0, 1),
        )

        self.assertEqual(terrain.get_origins(), {(1, 0)})
        self.assertEqual(terrain.get_destinations(), {(0, 1)})

    def test_complete_path_accepts_any_origin_and_any_destination(self):
        self.assertTrue(self.terrain.is_complete_path([(1, 0), (1, 1), (1, 2)]))
        self.assertTrue(self.terrain.is_complete_path([(0, 0), (0, 1), (0, 2)]))

    def test_complete_path_rejects_wrong_start_or_end(self):
        valid, message = self.terrain.why_complete_path([(0, 1), (0, 2)])
        self.assertFalse(valid)
        self.assertIn("Path does not start in any origin", message)

        valid, message = self.terrain.why_complete_path([(0, 0), (0, 1)])
        self.assertFalse(valid)
        self.assertIn("Path does not end in any destination", message)

    def test_invalid_steps_are_rejected_before_endpoint_checks(self):
        self.assertEqual(
            self.terrain.why_complete_path([(0, 0), (1, 1), (1, 2)]),
            (False, "Invalid path: (0, 0) -> (1, 1)"),
        )

    def test_str_marks_all_origins_and_destinations(self):
        text = str(self.terrain)

        self.assertGreaterEqual(text.count("|O "), 2)
        self.assertGreaterEqual(text.count("|X "), 2)

    def test_rejects_out_of_bounds_endpoints(self):
        with self.assertRaisesRegex(AttributeError, "Origin row is out of bounds"):
            MultiEndpointTerrain([[1]], origin={(-1, 0)}, destination={(0, 0)})
        with self.assertRaisesRegex(AttributeError, "Destination column is out of bounds"):
            MultiEndpointTerrain([[1]], origin={(0, 0)}, destination={(0, 1)})


class TestSequentialDestinationTerrain(unittest.TestCase):
    def setUp(self):
        self.terrain = SequentialDestinationTerrain(
            [[1, 2, 3], [4, 5, 6]],
            origin=(0, 0),
            destination=[(0, 1), (1, 2)],
        )

    def test_complete_path_requires_destinations_in_order(self):
        self.assertTrue(
            self.terrain.is_complete_path([(0, 0), (0, 1), (0, 2), (1, 2)])
        )
        self.assertEqual(
            self.terrain.why_complete_path([(0, 0), (1, 0), (1, 1), (1, 2)]),
            (False, "Path does not go through the destination (0, 1)"),
        )

    def test_str_marks_origin_and_sequential_destinations(self):
        text = str(self.terrain)

        self.assertIn("|<0> 1 ", text)
        self.assertIn("|<1> 2 ", text)

    def test_get_destinations_returns_destination_list(self):
        self.assertEqual(self.terrain.get_destinations(), [(0, 1), (1, 2)])
