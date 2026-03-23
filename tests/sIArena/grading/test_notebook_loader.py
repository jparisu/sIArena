import json
from pathlib import Path
import tempfile
import unittest

from sIArena.grading import GraderTestSuite, NotebookFunctionLoader, load_grader_config


ROOT = Path(__file__).resolve().parents[3]
GRADER_PATH = ROOT / "resources" / "graders" / "IA_practica_0.yaml"


def _write_notebook(path: Path, cell_sources):
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source,
            }
            for source in cell_sources
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")


class TestNotebookLoader(unittest.TestCase):
    def test_load_submission_extracts_callable_function(self):
        config = load_grader_config(GRADER_PATH)
        loader = NotebookFunctionLoader(config.assignment)

        with tempfile.TemporaryDirectory() as tmp_dir:
            notebook_path = Path(tmp_dir) / "alice.ipynb"
            _write_notebook(
                notebook_path,
                [
                    [
                        "from sIArena.path_finding import dijkstra\n",
                        "\n",
                        "def path_finding(terrain):\n",
                        "    return dijkstra(terrain)\n",
                    ]
                ],
            )

            submission = loader.load_submission(notebook_path)

        self.assertEqual(submission.file_name, "alice.ipynb")
        self.assertEqual(submission.author, "alice")
        self.assertEqual(submission.function_name, "path_finding")
        self.assertEqual(submission.cell_index, 0)
        self.assertTrue(callable(submission.search_function))

    def test_suite_can_evaluate_notebook_submission(self):
        suite = GraderTestSuite.from_yaml(GRADER_PATH)

        with tempfile.TemporaryDirectory() as tmp_dir:
            notebook_path = Path(tmp_dir) / "bob.ipynb"
            _write_notebook(
                notebook_path,
                [
                    [
                        "from sIArena.path_finding import dijkstra\n",
                        "\n",
                        "def path_finding(terrain):\n",
                        "    return dijkstra(terrain)\n",
                    ]
                ],
            )

            notebook_result = suite.evaluate_notebook(notebook_path)

        self.assertEqual(notebook_result.submission.author, "bob")
        self.assertIsNotNone(notebook_result.function_result)
        self.assertTrue(all(result.success for result in notebook_result.function_result.case_results))
        self.assertEqual(len(notebook_result.function_result.test_results), 4)
        self.assertIsNone(notebook_result.comments)

    def test_suite_captures_notebook_loading_errors_in_comments(self):
        suite = GraderTestSuite.from_yaml(GRADER_PATH)

        with tempfile.TemporaryDirectory() as tmp_dir:
            notebook_path = Path(tmp_dir) / "charlie.ipynb"
            _write_notebook(
                notebook_path,
                [["def another_name(terrain):\n", "    return []\n"]],
            )

            notebook_result = suite.evaluate_notebook(notebook_path)

        self.assertIsNone(notebook_result.function_result)
        self.assertIn("Function path_finding was not found", notebook_result.comments)
        self.assertEqual(notebook_result.load_error_type, "ValueError")
