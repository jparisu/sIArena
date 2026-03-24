import json
from pathlib import Path
import tempfile
import unittest

from sIArena.utils.notebook_utils import (
    find_function_cells,
    find_function_cells_with_parse_errors,
    iter_code_cells,
    load_notebook,
)


class TestNotebookUtils(unittest.TestCase):
    def test_load_notebook_and_iter_code_cells(self):
        notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["# Title\n"]},
                {"cell_type": "code", "source": ["x = 1\n"]},
                {"cell_type": "code", "source": ["def path_finding(terrain):\n", "    return []\n"]},
            ]
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            notebook_path = Path(tmp_dir) / "demo.ipynb"
            notebook_path.write_text(json.dumps(notebook), encoding="utf-8")

            loaded_notebook = load_notebook(notebook_path)

        code_cells = iter_code_cells(loaded_notebook)
        self.assertEqual(len(code_cells), 2)
        self.assertEqual(code_cells[0][0], 1)
        self.assertIn("x = 1", code_cells[0][1])

    def test_find_function_cells_returns_matching_code_cell(self):
        notebook = {
            "cells": [
                {"cell_type": "code", "source": ["def helper():\n", "    return 1\n"]},
                {"cell_type": "code", "source": ["def path_finding(terrain):\n", "    return []\n"]},
            ]
        }

        matching_cells = find_function_cells(notebook, "path_finding")

        self.assertEqual(len(matching_cells), 1)
        self.assertEqual(matching_cells[0][0], 1)

    def test_find_function_cells_with_parse_errors_collects_syntax_failures(self):
        notebook = {
            "cells": [
                {"cell_type": "code", "source": ["def path_finding(terrain):\n", "return []\n"]},
                {"cell_type": "code", "source": ["def helper():\n", "    return 1\n"]},
            ]
        }

        matching_cells, parse_errors = find_function_cells_with_parse_errors(
            notebook, "path_finding"
        )

        self.assertEqual(matching_cells, [])
        self.assertEqual(len(parse_errors), 1)
        self.assertEqual(parse_errors[0].cell_index, 0)
        self.assertEqual(type(parse_errors[0].error).__name__, "IndentationError")
