import csv
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from sIArena.grading import ZipNotebookGrader, grade_zip_archive_to_csv


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


class TestBatchGrader(unittest.TestCase):
    def test_grade_archive_and_write_csv_report(self):
        grader = ZipNotebookGrader.from_yaml(GRADER_PATH)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            valid_notebook = tmp_path / "alice.ipynb"
            invalid_notebook = tmp_path / "bob.ipynb"

            _write_notebook(
                valid_notebook,
                [
                    [
                        "from sIArena.path_finding import dijkstra\n",
                        "\n",
                        "def path_finding(terrain):\n",
                        "    return dijkstra(terrain)\n",
                    ]
                ],
            )
            _write_notebook(
                invalid_notebook,
                [
                    [
                        "def path_finding(terrain):\n",
                        "    _ = terrain\n",
                        "    return []\n",
                    ]
                ],
            )

            zip_path = tmp_path / "submissions.zip"
            with zipfile.ZipFile(zip_path, "w") as archive:
                archive.write(valid_notebook, arcname=valid_notebook.name)
                archive.write(invalid_notebook, arcname=invalid_notebook.name)

            csv_path = tmp_path / "results.csv"
            batch_result = grade_zip_archive_to_csv(zip_path, GRADER_PATH, csv_path)

            self.assertEqual(batch_result.assignment_id, "IA_practica_0")
            self.assertEqual(len(batch_result.submission_grades), 2)

            grades_by_file = {
                submission_grade.file_name: submission_grade
                for submission_grade in batch_result.submission_grades
            }

            valid_grade = grades_by_file["alice.ipynb"]
            invalid_grade = grades_by_file["bob.ipynb"]

            self.assertEqual(valid_grade.author, "alice")
            self.assertEqual(valid_grade.optimality_percentage, 1.0)
            self.assertIsNone(valid_grade.comments)
            self.assertEqual(invalid_grade.author, "bob")
            self.assertEqual(invalid_grade.optimality_percentage, 0.0)
            self.assertEqual(
                invalid_grade.comments,
                "20x Function path_finding returned an invalid path: Empty path",
            )

            with csv_path.open("r", encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))

        self.assertEqual(len(rows), 2)
        rows_by_file = {row["file_name"]: row for row in rows}

        self.assertEqual(rows_by_file["alice.ipynb"]["author"], "alice")
        self.assertEqual(rows_by_file["alice.ipynb"]["optimality_percentage"], "100.00")
        self.assertEqual(rows_by_file["alice.ipynb"]["comments"], "")
        self.assertEqual(rows_by_file["bob.ipynb"]["author"], "bob")
        self.assertEqual(rows_by_file["bob.ipynb"]["optimality_percentage"], "0.00")
        self.assertEqual(
            rows_by_file["bob.ipynb"]["comments"],
            "20x Function path_finding returned an invalid path: Empty path",
        )
        self.assertEqual(rows_by_file["bob.ipynb"]["trivial_optimality"], "0.00")
        self.assertEqual(rows_by_file["alice.ipynb"]["trivial_optimality"], "100.00")
