import re
from pathlib import Path
from typing import Optional, Union

from sIArena.grading.models import AssignmentSpec, NotebookSubmission
from sIArena.utils.notebook_utils import find_function_cells, load_notebook


class NotebookFunctionLoader:
    def __init__(self, assignment: AssignmentSpec):
        self.assignment = assignment

    def load_submission(self, notebook_path: Union[str, Path]) -> NotebookSubmission:
        notebook_path = Path(notebook_path)
        notebook = load_notebook(notebook_path)
        matching_cells = find_function_cells(notebook, self.assignment.notebook_function)

        if len(matching_cells) == 0:
            raise ValueError(
                f"Function {self.assignment.notebook_function} was not found in {notebook_path.name}"
            )
        if len(matching_cells) > 1:
            raise ValueError(
                f"Function {self.assignment.notebook_function} appears in multiple notebook cells in {notebook_path.name}"
            )

        cell_index, source_code = matching_cells[0]
        search_function = self._compile_function(source_code, notebook_path)
        return NotebookSubmission(
            notebook_path=notebook_path,
            file_name=notebook_path.name,
            author=self.derive_author(notebook_path),
            function_name=self.assignment.notebook_function,
            cell_index=cell_index,
            source_code=source_code,
            search_function=search_function,
        )

    def _compile_function(self, source_code: str, notebook_path: Path):
        namespace = {"__builtins__": __builtins__}
        try:
            exec(source_code, namespace)
        except Exception as exc:
            raise RuntimeError(
                f"Could not execute the notebook cell defining {self.assignment.notebook_function} in {notebook_path.name}: "
                f"{type(exc).__name__}: {exc}"
            ) from exc

        search_function = namespace.get(self.assignment.notebook_function)
        if search_function is None or not callable(search_function):
            raise ValueError(
                f"The notebook cell in {notebook_path.name} did not define a callable {self.assignment.notebook_function}"
            )
        return search_function

    def derive_author(self, notebook_path: Union[str, Path]) -> str:
        notebook_path = Path(notebook_path)
        if self.assignment.author_from != "file_stem":
            raise ValueError(
                f"Unsupported author extraction mode: {self.assignment.author_from}"
            )

        file_stem = notebook_path.stem
        if self.assignment.author_pattern is None:
            return file_stem

        match = re.search(self.assignment.author_pattern, file_stem)
        if match is None:
            return file_stem
        if "author" in match.groupdict():
            return match.group("author")
        return match.group(0)
