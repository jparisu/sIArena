import time
import unittest

from sIArena.measurements.measurements import measure_function
from sIArena.path_finding import a_star, dijkstra
from sIArena.terrain.Terrain import MultipleDestinationTerrain
from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator
from sIArena.terrain.generator.MazeGenerator import MazeGenerator
from sIArena.terrain.generator.PerlinGenerator import PerlinGenerator


class TestExerciseIntegration(unittest.TestCase):
    def _run_exercise_flow(self, parameters, path_finding, terrain_ctor=None, max_seconds=5):
        terrains = {}
        for terrain_name, (generator, kwargs) in parameters.items():
            terrain_kwargs = dict(kwargs)
            if terrain_ctor is not None:
                terrain_kwargs["terrain_ctor"] = terrain_ctor
            terrains[terrain_name] = generator.generate_random_terrain(**terrain_kwargs)

        results = {}
        for terrain_name, terrain in terrains.items():
            cost, seconds, path = measure_function(
                path_finding,
                terrain,
                max_seconds=max_seconds,
            )
            self.assertTrue(terrain.is_complete_path(path), terrain_name)
            self.assertEqual(path[0], terrain.origin, terrain_name)
            self.assertGreaterEqual(cost, 0, terrain_name)
            self.assertGreaterEqual(seconds, 0, terrain_name)
            results[terrain_name] = (cost, seconds, path)

        return results

    def test_dijkstra_solves_single_destination_exercise_flow(self):
        parameters = {
            "trivial": [
                FocusedGenerator(),
                {
                    "n": 5,
                    "m": 5,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 0,
                    "min_step": 10,
                    "abruptness": 0.7,
                    "origin": (0, 0),
                    "destination": (4, 4),
                },
            ],
            "tmaze": [
                MazeGenerator(),
                {
                    "n": 5,
                    "m": 5,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 0,
                    "min_step": 1,
                    "abruptness": 0,
                    "origin": (0, 0),
                    "destination": (4, 4),
                },
            ],
        }

        results = self._run_exercise_flow(parameters, dijkstra)
        self.assertEqual(set(results.keys()), set(parameters.keys()))

    def test_a_star_solves_single_destination_exercise_flow(self):
        parameters = {
            "walk": [
                PerlinGenerator(),
                {
                    "n": 20,
                    "m": 20,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 10,
                    "min_step": 2,
                    "abruptness": 0.1,
                    "origin": (0, 1),
                    "destination": (16, 15),
                },
            ],
            "race": [
                FocusedGenerator(),
                {
                    "n": 30,
                    "m": 30,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 10,
                    "min_step": 2,
                    "abruptness": 0.1,
                    "origin": (0, 0),
                    "destination": (29, 29),
                },
            ],
        }

        results = self._run_exercise_flow(parameters, a_star)
        self.assertEqual(set(results.keys()), set(parameters.keys()))

    def test_a_star_solves_multiple_destination_exercise_flow(self):
        parameters = {
            "dodge": [
                MazeGenerator(),
                {
                    "n": 7,
                    "m": 7,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 0,
                    "min_step": 1,
                    "abruptness": 0,
                    "origin": (4, 0),
                    "destination": {(6, 0), (1, 2), (5, 5)},
                },
            ],
            "walk": [
                PerlinGenerator(),
                {
                    "n": 20,
                    "m": 20,
                    "seed": 43,
                    "min_height": 0,
                    "max_height": 10,
                    "min_step": 2,
                    "abruptness": 0.1,
                    "origin": (0, 1),
                    "destination": {(16, 15), (4, 17), (12, 3)},
                },
            ],
        }

        results = self._run_exercise_flow(
            parameters,
            a_star,
            terrain_ctor=MultipleDestinationTerrain,
        )
        self.assertEqual(set(results.keys()), set(parameters.keys()))

    def test_measure_function_rejects_incomplete_exercise_path(self):
        terrain = MazeGenerator().generate_random_terrain(
            n=7,
            m=7,
            seed=43,
            min_height=0,
            max_height=0,
            min_step=1,
            abruptness=0,
            origin=(4, 0),
            destination={(6, 0), (1, 2), (5, 5)},
            terrain_ctor=MultipleDestinationTerrain,
        )

        with self.assertRaisesRegex(ValueError, "does not go through the destination"):
            measure_function(lambda current_terrain: [current_terrain.origin], terrain, max_seconds=0)

    def test_measure_function_rejects_slow_exercise_path_finding(self):
        terrain = FocusedGenerator().generate_random_terrain(
            n=5,
            m=5,
            seed=43,
            min_height=0,
            max_height=0,
            min_step=10,
            abruptness=0.7,
            origin=(0, 0),
            destination=(4, 4),
        )

        def slow_path_finding(current_terrain):
            _ = current_terrain
            time.sleep(0.05)
            return []

        with self.assertRaisesRegex(TimeoutError, "took more than 0.001 seconds"):
            measure_function(slow_path_finding, terrain, max_seconds=0.001)

    def test_measure_function_wraps_internal_exercise_error(self):
        terrain = FocusedGenerator().generate_random_terrain(
            n=5,
            m=5,
            seed=43,
            min_height=0,
            max_height=0,
            min_step=10,
            abruptness=0.7,
            origin=(0, 0),
            destination=(4, 4),
        )

        def failing_path_finding(current_terrain):
            _ = current_terrain
            raise RuntimeError("boom")

        with self.assertRaisesRegex(RuntimeError, "Error inside user function failing_path_finding: RuntimeError: boom"):
            measure_function(failing_path_finding, terrain, max_seconds=1)
