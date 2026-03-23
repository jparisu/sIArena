import csv
import tempfile
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Optional, Union

from sIArena.grading.config import load_grader_config
from sIArena.grading.evaluation import GraderTestSuite
from sIArena.grading.models import (
    BatchEvaluationResult,
    NotebookEvaluationResult,
    SubmissionGrade,
    TestEvaluationResult,
)
from sIArena.utils.archive_utils import extract_zip_archive, iter_files_with_suffix


class ZipNotebookGrader:
    def __init__(self, suite: GraderTestSuite):
        self.suite = suite

    @classmethod
    def from_yaml(
        cls,
        yaml_path: Union[str, Path],
        author_pattern: Optional[str] = None,
    ) -> "ZipNotebookGrader":
        config = load_grader_config(yaml_path)
        if author_pattern is not None:
            config = replace(
                config,
                assignment=replace(config.assignment, author_pattern=author_pattern),
            )
        return cls(GraderTestSuite(config))

    def evaluate_input(
        self,
        input_path: Union[str, Path],
        iterations: int = 1,
        debug: bool = False,
    ) -> BatchEvaluationResult:
        input_path = Path(input_path)
        if input_path.suffix.lower() == ".zip":
            return self.evaluate_archive(
                input_path,
                iterations=iterations,
                debug=debug,
            )
        if input_path.suffix.lower() == ".ipynb":
            return self.evaluate_notebook(
                input_path,
                iterations=iterations,
                debug=debug,
            )
        raise ValueError(
            f"Unsupported input file type '{input_path.suffix}'. Expected .zip or .ipynb"
        )

    def evaluate_notebook(
        self,
        notebook_path: Union[str, Path],
        iterations: int = 1,
        debug: bool = False,
    ) -> BatchEvaluationResult:
        notebook_path = Path(notebook_path)
        submission_grade = self._build_submission_grade(
            self.suite.evaluate_notebook(
                notebook_path,
                iterations=iterations,
                debug=debug,
            )
        )
        return BatchEvaluationResult(
            assignment_id=self.suite.config.assignment.id,
            zip_file_name=notebook_path.name,
            submission_grades=(submission_grade,),
        )

    def evaluate_archive(
        self,
        zip_path: Union[str, Path],
        iterations: int = 1,
        debug: bool = False,
    ) -> BatchEvaluationResult:
        zip_path = Path(zip_path)

        with tempfile.TemporaryDirectory() as temporary_directory:
            extracted_root = extract_zip_archive(zip_path, temporary_directory)
            notebook_paths = tuple(iter_files_with_suffix(extracted_root, ".ipynb"))
            submission_grades = tuple(
                self._build_submission_grade(
                    self.suite.evaluate_notebook(
                        notebook_path,
                        iterations=iterations,
                        debug=debug,
                    )
                )
                for notebook_path in notebook_paths
            )

        return BatchEvaluationResult(
            assignment_id=self.suite.config.assignment.id,
            zip_file_name=zip_path.name,
            submission_grades=submission_grades,
        )

    def write_csv_report(
        self,
        batch_result: BatchEvaluationResult,
        csv_path: Union[str, Path],
    ) -> Path:
        csv_path = Path(csv_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = self._build_csv_fieldnames()

        with csv_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames)
            writer.writeheader()
            for submission_grade in batch_result.submission_grades:
                writer.writerow(self._build_csv_row(submission_grade))

        return csv_path

    def grade_archive_to_csv(
        self,
        zip_path: Union[str, Path],
        csv_path: Union[str, Path],
        iterations: int = 1,
        debug: bool = False,
    ) -> BatchEvaluationResult:
        batch_result = self.evaluate_input(
            zip_path,
            iterations=iterations,
            debug=debug,
        )
        self.write_csv_report(batch_result, csv_path)
        return batch_result

    def _build_submission_grade(
        self,
        notebook_result: NotebookEvaluationResult,
    ) -> SubmissionGrade:
        if notebook_result.function_result is None:
            test_results = tuple(
                TestEvaluationResult(
                    test_id=test_spec.id,
                    average_time_seconds=None,
                    average_path_cost=None,
                    optimality_ratio=0.0,
                    comments=notebook_result.comments,
                )
                for test_spec in self.suite.config.tests
            )
            return SubmissionGrade(
                file_name=notebook_result.submission.file_name,
                author=notebook_result.submission.author,
                test_results=test_results,
                optimality_percentage=0.0,
                comments=notebook_result.comments,
            )

        function_result = notebook_result.function_result
        return SubmissionGrade(
            file_name=notebook_result.submission.file_name,
            author=notebook_result.submission.author,
            test_results=function_result.test_results,
            optimality_percentage=_compute_optimality_percentage(function_result.test_results),
            comments=notebook_result.comments,
        )

    def _build_csv_fieldnames(self) -> List[str]:
        fieldnames = ["file_name", "author"]
        for test_spec in self.suite.config.tests:
            fieldnames.append(f"{test_spec.id}_time")
            fieldnames.append(f"{test_spec.id}_optimality")
        fieldnames.extend(["optimality_percentage", "comments"])
        return fieldnames

    def _build_csv_row(self, submission_grade: SubmissionGrade) -> Dict[str, object]:
        row: Dict[str, object] = {
            "file_name": submission_grade.file_name,
            "author": submission_grade.author,
            "optimality_percentage": _format_percentage(submission_grade.optimality_percentage),
            "comments": submission_grade.comments or "",
        }

        test_results_by_id = {
            test_result.test_id: test_result for test_result in submission_grade.test_results
        }

        for test_spec in self.suite.config.tests:
            test_result = test_results_by_id.get(test_spec.id)
            row[f"{test_spec.id}_time"] = _format_float(
                None if test_result is None else test_result.average_time_seconds
            )
            row[f"{test_spec.id}_optimality"] = _format_percentage(
                0.0 if test_result is None else test_result.optimality_ratio
            )

        return row


def grade_input_to_csv(
    input_path: Union[str, Path],
    yaml_path: Union[str, Path],
    csv_path: Union[str, Path],
    iterations: int = 1,
    debug: bool = False,
    author_pattern: Optional[str] = None,
) -> BatchEvaluationResult:
    grader = ZipNotebookGrader.from_yaml(
        yaml_path,
        author_pattern=author_pattern,
    )
    return grader.grade_archive_to_csv(
        input_path,
        csv_path,
        iterations=iterations,
        debug=debug,
    )


def grade_zip_archive_to_csv(
    zip_path: Union[str, Path],
    yaml_path: Union[str, Path],
    csv_path: Union[str, Path],
    iterations: int = 1,
    debug: bool = False,
    author_pattern: Optional[str] = None,
) -> BatchEvaluationResult:
    return grade_input_to_csv(
        zip_path,
        yaml_path,
        csv_path,
        iterations=iterations,
        debug=debug,
        author_pattern=author_pattern,
    )


def _compute_optimality_percentage(test_results: tuple[TestEvaluationResult, ...]) -> float:
    if not test_results:
        return 0.0
    return sum(test_result.optimality_ratio for test_result in test_results) / len(test_results)


def _format_float(value: Optional[float]) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def _format_percentage(value: float) -> str:
    return f"{100.0 * value:.2f}"
