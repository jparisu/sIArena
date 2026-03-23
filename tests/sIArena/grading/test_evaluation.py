from pathlib import Path
import unittest

from sIArena.grading import GraderTestSuite
from sIArena.path_finding import a_star, dijkstra


ROOT = Path(__file__).resolve().parents[3]
GRADER_PATH = ROOT / "resources" / "graders" / "IA_practica_0.yaml"


class TestGraderEvaluation(unittest.TestCase):
    def test_suite_caches_terrain_cases_and_evaluates_successfully(self):
        suite = GraderTestSuite.from_yaml(GRADER_PATH)

        evaluation = suite.evaluate_function(dijkstra)

        self.assertEqual(len(suite.terrain_cases), 20)
        self.assertEqual(len(evaluation.case_results), 20)
        self.assertTrue(all(case_result.success for case_result in evaluation.case_results))
        self.assertTrue(all(case_result.optimal for case_result in evaluation.case_results))

    def test_evaluate_function_captures_solver_failures_without_aborting(self):
        suite = GraderTestSuite.from_yaml(GRADER_PATH)

        def failing_solver(current_terrain):
            _ = current_terrain
            return []

        evaluation = suite.evaluate_function(failing_solver)

        self.assertEqual(len(evaluation.case_results), 20)
        self.assertTrue(all(not case_result.success for case_result in evaluation.case_results))
        self.assertTrue(all(case_result.error_type == "ValueError" for case_result in evaluation.case_results))

    def test_a_star_is_supported_as_a_function_under_test(self):
        suite = GraderTestSuite.from_yaml(GRADER_PATH)

        evaluation = suite.evaluate_function(a_star)

        self.assertTrue(all(case_result.success for case_result in evaluation.case_results))
