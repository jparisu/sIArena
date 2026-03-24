import unittest

from sIArena.path_finding import a_star, dijkstra, heuristic
from sIArena.terrain.Terrain import (
    MultipleDestinationTerrain,
    SequentialDestinationTerrain,
    Terrain,
)


class TestAStarHeuristic(unittest.TestCase):
    def test_heuristic_adds_manhattan_distance_and_required_climb(self):
        terrain = Terrain([[0, 0], [0, 3]])

        self.assertEqual(heuristic(terrain, (0, 0), (1, 1)), 5.0)
        self.assertEqual(heuristic(terrain, (1, 1), (0, 0)), 2.0)

    def test_heuristic_is_consistent_for_neighbor_expansions(self):
        terrain = Terrain(
            [
                [0, 1, 3],
                [2, 2, 1],
                [1, 4, 0],
            ]
        )

        for goal_row in range(terrain.n):
            for goal_column in range(terrain.m):
                goal = (goal_row, goal_column)
                for row in range(terrain.n):
                    for column in range(terrain.m):
                        current = (row, column)
                        current_heuristic = heuristic(terrain, current, goal)

                        for neighbor in terrain.get_neighbors(current):
                            step_cost = terrain.get_cost(current, neighbor)
                            neighbor_heuristic = heuristic(terrain, neighbor, goal)
                            self.assertLessEqual(
                                current_heuristic,
                                step_cost + neighbor_heuristic,
                            )


class TestPathFindingDispatch(unittest.TestCase):
    def test_a_star_solves_sequential_destination_terrain(self):
        terrain = SequentialDestinationTerrain(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            origin=(0, 0),
            destination=[(0, 2), (2, 2)],
        )

        path = a_star(terrain)

        self.assertTrue(terrain.is_complete_path(path))
        self.assertEqual(path[0], terrain.origin)
        self.assertEqual(path[-1], terrain.destinations[-1])

    def test_dijkstra_solves_multiple_destination_terrain(self):
        terrain = MultipleDestinationTerrain(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            origin=(1, 1),
            destination={(0, 0), (2, 2)},
        )

        path = dijkstra(terrain)

        self.assertTrue(terrain.is_complete_path(path))
        self.assertEqual(path[0], terrain.origin)

    def test_multiple_destination_solver_finds_global_optimum(self):
        terrain = MultipleDestinationTerrain(
            [[0, 1, 3], [1, 0, 1], [2, 1, 0]],
            origin=(0, 0),
            destination={(0, 1), (0, 2), (1, 0)},
        )

        a_star_path = a_star(terrain)
        dijkstra_path = dijkstra(terrain)

        self.assertEqual(terrain.get_path_cost(a_star_path), 9)
        self.assertEqual(terrain.get_path_cost(dijkstra_path), 9)
