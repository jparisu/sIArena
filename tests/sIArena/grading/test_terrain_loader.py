from pathlib import Path
import unittest

from sIArena.grading import build_terrain_case, build_terrain_cases, load_grader_config
from sIArena.grading.config import parse_grader_config
from sIArena.terrain.Terrain import (
    MultiEndpointTerrain,
    MultipleDestinationTerrain,
    NoPathTerrain,
    SequentialDestinationTerrain,
    Terrain,
    default_cost_function,
)


ROOT = Path(__file__).resolve().parents[3]
GRADER_PATH = ROOT / "resources" / "graders" / "IA_practica_0.yaml"


class TestTerrainLoader(unittest.TestCase):
    def test_build_terrain_case(self):
        config = load_grader_config(GRADER_PATH)

        terrain_case = build_terrain_case(config.tests[0], 43)

        self.assertEqual(terrain_case.label, "trivial[seed=43]")
        self.assertEqual(terrain_case.generator_name, "FocusedGenerator")
        self.assertEqual(terrain_case.terrain_type_name, "Terrain")
        self.assertIsInstance(terrain_case.terrain, Terrain)
        self.assertEqual(terrain_case.terrain.origin, (0, 0))
        self.assertEqual(terrain_case.terrain.destination, (4, 4))

    def test_build_terrain_cases(self):
        config = load_grader_config(GRADER_PATH)

        terrain_cases = build_terrain_cases(config)

        self.assertEqual(len(terrain_cases), 20)
        self.assertEqual(terrain_cases[0].label, "trivial[seed=43]")
        self.assertEqual(terrain_cases[-1].label, "mountain[seed=47]")

    def test_build_multiple_and_sequential_destination_terrains(self):
        config = parse_grader_config(
            {
                "version": 1,
                "assignment": {"id": "demo"},
                "tests": [
                    {
                        "id": "multi",
                        "generator": "MazeGenerator",
                        "terrain_type": "MultipleDestinationTerrain",
                        "seeds": [3],
                        "parameters": {
                            "n": 5,
                            "m": 5,
                            "destination": [[0, 4], [4, 4]],
                        },
                    },
                    {
                        "id": "seq",
                        "generator": "FocusedGenerator",
                        "terrain_type": "SequentialDestinationTerrain",
                        "seeds": [5],
                        "parameters": {
                            "n": 5,
                            "m": 5,
                            "destination": [[0, 2], [4, 4]],
                        },
                    },
                ],
            }
        )

        multi_case = build_terrain_case(config.tests[0], 3)
        seq_case = build_terrain_case(config.tests[1], 5)

        self.assertIsInstance(multi_case.terrain, MultipleDestinationTerrain)
        self.assertEqual(multi_case.terrain.get_destinations(), {(0, 4), (4, 4)})
        self.assertIsInstance(seq_case.terrain, SequentialDestinationTerrain)
        self.assertEqual(seq_case.terrain.get_destinations(), [(0, 2), (4, 4)])

    def test_build_multi_endpoint_terrain(self):
        config = parse_grader_config(
            {
                "version": 1,
                "assignment": {"id": "demo"},
                "tests": [
                    {
                        "id": "multi-endpoint",
                        "generator": "FocusedGenerator",
                        "terrain_type": "MultiEndpointTerrain",
                        "seeds": [13],
                        "parameters": {
                            "n": 5,
                            "m": 5,
                            "origin": [[0, 0], [4, 0]],
                            "destination": [[0, 4], [4, 4]],
                        },
                    },
                ],
            }
        )

        terrain_case = build_terrain_case(config.tests[0], 13)

        self.assertIsInstance(terrain_case.terrain, MultiEndpointTerrain)
        self.assertEqual(terrain_case.terrain.get_origins(), {(0, 0), (4, 0)})
        self.assertEqual(terrain_case.terrain.get_destinations(), {(0, 4), (4, 4)})

    def test_build_no_path_terrain_and_named_cost_function(self):
        config = parse_grader_config(
            {
                "version": 1,
                "assignment": {"id": "demo"},
                "defaults": {"cost_function": "default_cost_function"},
                "tests": [
                    {
                        "id": "nop",
                        "generator": "PerlinGenerator",
                        "terrain_type": "NoPathTerrain",
                        "seeds": [11],
                        "parameters": {
                            "n": 3,
                            "m": 4,
                            "abruptness": 0.4,
                        },
                    }
                ],
            }
        )

        terrain_case = build_terrain_case(config.tests[0], 11)

        self.assertIsInstance(terrain_case.terrain, NoPathTerrain)
        self.assertEqual(terrain_case.terrain.size(), (3, 4))
        self.assertIs(terrain_case.terrain.cost_function, default_cost_function)
