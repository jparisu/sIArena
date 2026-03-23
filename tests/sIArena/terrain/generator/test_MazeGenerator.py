import unittest
from unittest.mock import patch

import numpy as np

from sIArena.terrain.generator.MazeGenerator import (
    Maze,
    MazeGenerator,
    Tile,
    weigthed_distrubution,
)


class TestMazeGenerator(unittest.TestCase):
    def test_generate_random_terrain_rewrites_default_height_parameters(self):
        generator = MazeGenerator()

        with patch("sIArena.terrain.generator.Generator.TerrainGenerator.generate_random_terrain", return_value="terrain") as super_mock:
            result = generator.generate_random_terrain(2, 3, min_step=1)

        self.assertEqual(result, "terrain")
        self.assertEqual(
            super_mock.call_args.kwargs,
            {
                "n": 2,
                "m": 3,
                "min_height": 0,
                "max_height": 6,
                "min_step": 6,
                "abruptness": 0.2,
                "seed": None,
                "origin": None,
                "destination": None,
                "terrain_ctor": unittest.mock.ANY,
                "cost_function": None,
            },
        )

    def test_generate_random_matrix_returns_binary_maze_and_even_grid_exit(self):
        matrix = MazeGenerator().generate_random_matrix_(4, 4, seed=3)

        self.assertEqual(matrix.shape, (4, 4))
        self.assertEqual(matrix[-1, -1], 0)
        self.assertEqual(matrix[-2, -1], 0)
        self.assertTrue(set(np.unique(matrix)).issubset({0, 1}))


class TestTile(unittest.TestCase):
    def test_mutator_methods_toggle_each_wall_and_visit_state(self):
        tile = Tile()

        tile.add_up()
        tile.add_down()
        tile.add_left()
        tile.add_right()
        tile.visit()

        self.assertTrue(tile.up)
        self.assertTrue(tile.down)
        self.assertTrue(tile.left)
        self.assertTrue(tile.right)
        self.assertTrue(tile.visited)


class TestWeightedDistribution(unittest.TestCase):
    def test_single_choice_returns_zero(self):
        self.assertEqual(weigthed_distrubution(1), 0)

    def test_random_choices_receives_expected_weights(self):
        with patch("sIArena.terrain.generator.MazeGenerator.random.choices", return_value=[2]) as choices_mock:
            value = weigthed_distrubution(4, r=3)

        self.assertEqual(value, 2)
        self.assertEqual(choices_mock.call_args.args[0], [0, 1, 2, 3])
        self.assertEqual(choices_mock.call_args.kwargs["weights"], [3, 5, 7, 9])


class TestMaze(unittest.TestCase):
    def test_init_marks_start_tile_visited(self):
        maze = Maze(1, 1, start_point=(0, 0))

        self.assertTrue(maze.tile((0, 0)).visited)

    def test_tile_and_surrounding_coordinates_access_expected_cells(self):
        maze = Maze(1, 1, start_point=(0, 0))

        self.assertIsInstance(maze.tile((0, 0)), Tile)
        self.assertEqual(maze.surrounding_coordinates((0, 0)), [])

        larger_maze = Maze(2, 2, start_point=(0, 0))
        self.assertEqual(set(larger_maze.surrounding_coordinates((0, 0))), {(1, 0), (0, 1)})

    def test_join_tiles_connects_horizontally_and_vertically(self):
        horizontal = Maze(1, 2, start_point=(0, 0))
        horizontal.matrix = [[Tile(), Tile()]]
        horizontal.join_tiles((0, 0), (0, 1))
        self.assertTrue(horizontal.matrix[0][0].right)
        self.assertTrue(horizontal.matrix[0][1].left)

        vertical = Maze(2, 1, start_point=(0, 0))
        vertical.matrix = [[Tile()], [Tile()]]
        vertical.join_tiles((0, 0), (1, 0))
        self.assertTrue(vertical.matrix[0][0].down)
        self.assertTrue(vertical.matrix[1][0].up)

    def test_join_tiles_rejects_non_adjacent_coordinates(self):
        maze = Maze(2, 2, start_point=(0, 0))
        maze.matrix = [[Tile(), Tile()], [Tile(), Tile()]]

        with self.assertRaisesRegex(Exception, "Tiles are not adjacent"):
            maze.join_tiles((0, 0), (1, 1))

    def test_str_returns_ascii_maze(self):
        maze = Maze(1, 1, start_point=(0, 0))

        text = str(maze)

        self.assertIn("+", text)
        self.assertIn("|", text)
