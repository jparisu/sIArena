import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union


Notebook = Dict[str, object]


def load_notebook(path: Union[str, Path]) -> Notebook:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)


def iter_code_cells(notebook: Notebook) -> List[Tuple[int, str]]:
    code_cells: List[Tuple[int, str]] = []
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        if isinstance(source, list):
            source = "".join(source)
        code_cells.append((index, source))
    return code_cells


def find_function_cells(notebook: Notebook, function_name: str) -> List[Tuple[int, str]]:
    matching_cells: List[Tuple[int, str]] = []
    for index, source in iter_code_cells(notebook):
        try:
            module = ast.parse(source)
        except SyntaxError:
            continue

        for node in module.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                matching_cells.append((index, source))
                break

    return matching_cells
