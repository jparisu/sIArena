from pathlib import Path
import unittest

from sIArena.grading import load_grader_config
from sIArena.grading.config import parse_grader_config


ROOT = Path(__file__).resolve().parents[3]
GRADER_PATH = ROOT / "resources" / "graders" / "IA_practica_0.yaml"


class TestGraderConfig(unittest.TestCase):
    def test_load_grader_config(self):
        config = load_grader_config(GRADER_PATH)

        self.assertEqual(config.version, 1)
        self.assertEqual(config.assignment.id, "IA_practica_0")
        self.assertEqual(config.assignment.notebook_function, "path_finding")
        self.assertEqual(len(config.tests), 4)

        trivial_test = config.tests[0]
        self.assertEqual(trivial_test.id, "trivial")
        self.assertEqual(trivial_test.generator_name, "FocusedGenerator")
        self.assertEqual(trivial_test.seeds, (43, 44, 45, 46, 47))
        self.assertEqual(trivial_test.parameters["origin"], (0, 0))
        self.assertEqual(trivial_test.parameters["destination"], (4, 4))
        self.assertEqual(trivial_test.time_limits.max_seconds, 60.0)

    def test_parse_multiple_and_sequential_destinations_and_cost_function(self):
        config = parse_grader_config(
            {
                "version": 1,
                "assignment": {"id": "demo"},
                "defaults": {"cost_function": "default_cost_function"},
                "tests": [
                    {
                        "id": "multi",
                        "generator": "MazeGenerator",
                        "terrain_type": "MultipleDestinationTerrain",
                        "seeds": [7],
                        "parameters": {
                            "n": 3,
                            "m": 3,
                            "destination": [[0, 2], [2, 2]],
                        },
                    },
                    {
                        "id": "seq",
                        "generator": "FocusedGenerator",
                        "terrain_type": "SequentialDestinationTerrain",
                        "seeds": [8],
                        "parameters": {
                            "n": 4,
                            "m": 4,
                            "destination": [[0, 1], [3, 3]],
                        },
                    },
                ],
            }
        )

        self.assertEqual(config.tests[0].parameters["destination"], {(0, 2), (2, 2)})
        self.assertEqual(config.tests[0].cost_function_name, "default_cost_function")
        self.assertEqual(config.tests[1].parameters["destination"], [(0, 1), (3, 3)])

    def test_parse_no_path_terrain(self):
        config = parse_grader_config(
            {
                "version": 1,
                "assignment": {"id": "demo"},
                "tests": [
                    {
                        "id": "nop",
                        "generator": "PerlinGenerator",
                        "terrain_type": "NoPathTerrain",
                        "seeds": [1],
                        "parameters": {
                            "n": 2,
                            "m": 3,
                            "min_height": 0,
                            "max_height": 9,
                        },
                    }
                ],
            }
        )

        self.assertEqual(config.tests[0].terrain_type_name, "NoPathTerrain")

    def test_rejects_unsupported_parameter_and_invalid_no_path_fields(self):
        with self.assertRaisesRegex(ValueError, "Unsupported generator parameters"):
            parse_grader_config(
                {
                    "version": 1,
                    "assignment": {"id": "demo"},
                    "tests": [
                        {
                            "id": "bad",
                            "generator": "FocusedGenerator",
                            "seeds": [1],
                            "parameters": {"n": 2, "m": 2, "foo": 3, "destination": [1, 1]},
                        }
                    ],
                }
            )

        with self.assertRaisesRegex(ValueError, "NoPathTerrain does not support the 'destination' parameter"):
            parse_grader_config(
                {
                    "version": 1,
                    "assignment": {"id": "demo"},
                    "tests": [
                        {
                            "id": "bad-nopath",
                            "generator": "FocusedGenerator",
                            "terrain_type": "NoPathTerrain",
                            "seeds": [1],
                            "parameters": {"n": 2, "m": 2, "destination": [1, 1]},
                        }
                    ],
                }
            )
