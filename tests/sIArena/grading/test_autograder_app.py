import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
APP_PATH = ROOT / "apps" / "autograder" / "autograder.py"
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


class TestAutograderApp(unittest.TestCase):
    def test_cli_grades_single_notebook_and_uses_author_prefix(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            notebook_path = tmp_path / "alice_submission.ipynb"
            output_path = tmp_path / "results.csv"

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

            completed = subprocess.run(
                [
                    sys.executable,
                    str(APP_PATH),
                    "--input",
                    str(notebook_path),
                    "--config",
                    str(GRADER_PATH),
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Processed submissions: 1", completed.stdout)
            with output_path.open("r", encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["file_name"], "alice_submission.ipynb")
        self.assertEqual(rows[0]["author"], "alice")
        self.assertEqual(rows[0]["optimality_percentage"], "100.00")
