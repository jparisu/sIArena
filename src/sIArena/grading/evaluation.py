from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from sIArena.grading.config import load_grader_config
from sIArena.grading.models import (
    FunctionEvaluationResult,
    GraderConfig,
    NotebookEvaluationResult,
    NotebookSubmission,
    TerrainCase,
    TerrainEvaluationResult,
    TerrainTestSpec,
    TestEvaluationResult,
    TimeLimits,
)
from sIArena.grading.notebook_loader import NotebookFunctionLoader
from sIArena.grading.terrain_loader import build_terrain_case
from sIArena.measurements.measurements import measure_function
from sIArena.path_finding import a_star, dijkstra


ORACLE_REGISTRY: Dict[str, Callable] = {
    "a_star": a_star,
    "dijkstra": dijkstra,
}


class GraderTestSuite:
    def __init__(self, config: GraderConfig):
        self.config = config
        self.notebook_loader = NotebookFunctionLoader(self.config.assignment)
        self._prepared_cases: List[Tuple[TerrainTestSpec, TerrainCase]] = []
        for test_spec in self.config.tests:
            for seed in test_spec.seeds:
                self._prepared_cases.append((test_spec, build_terrain_case(test_spec, seed)))
        self._oracle_cache: Dict[Tuple[int, str], Tuple[int, object]] = {}

    @classmethod
    def from_yaml(cls, path) -> "GraderTestSuite":
        return cls(load_grader_config(path))

    @property
    def terrain_cases(self) -> Tuple[TerrainCase, ...]:
        return tuple(terrain_case for _, terrain_case in self._prepared_cases)

    def evaluate_function(
        self,
        search_function: Callable,
        iterations: int = 1,
        debug: bool = False,
    ) -> FunctionEvaluationResult:
        function_name = getattr(search_function, "__name__", search_function.__class__.__name__)
        case_results = tuple(
            self._evaluate_case(search_function, function_name, test_spec, terrain_case, iterations, debug)
            for test_spec, terrain_case in self._prepared_cases
        )
        return FunctionEvaluationResult(
            function_name=function_name,
            test_results=_aggregate_test_results(case_results),
            case_results=case_results,
            comments=_aggregate_comments(case_results),
        )

    def evaluate_notebook(
        self,
        notebook_path,
        iterations: int = 1,
        debug: bool = False,
    ) -> NotebookEvaluationResult:
        notebook_path = Path(notebook_path)
        try:
            submission = self.notebook_loader.load_submission(notebook_path)
        except Exception as exc:
            fallback_submission = NotebookSubmission(
                notebook_path=notebook_path,
                file_name=notebook_path.name,
                author=self.notebook_loader.derive_author(notebook_path),
                function_name=self.config.assignment.notebook_function,
                cell_index=-1,
                source_code="",
                search_function=lambda terrain: terrain,
            )
            message = _extract_last_error_line(str(exc))
            return NotebookEvaluationResult(
                submission=fallback_submission,
                function_result=None,
                comments=message,
                load_error_type=type(exc).__name__,
                load_error_message=str(exc),
            )

        function_result = self.evaluate_function(
            submission.search_function,
            iterations=iterations,
            debug=debug,
        )
        comments = function_result.comments
        return NotebookEvaluationResult(
            submission=submission,
            function_result=function_result,
            comments=comments,
        )

    def _evaluate_case(
        self,
        search_function: Callable,
        function_name: str,
        test_spec: TerrainTestSpec,
        terrain_case: TerrainCase,
        iterations: int,
        debug: bool,
    ) -> TerrainEvaluationResult:
        if terrain_case.terrain.get_destinations() is None:
            return TerrainEvaluationResult(
                terrain_case=terrain_case,
                function_name=function_name,
                success=False,
                elapsed_seconds=None,
                path_cost=None,
                path=None,
                oracle_name=None,
                oracle_cost=None,
                oracle_path=None,
                optimal=None,
                within_time_limits=None,
                comments=_extract_last_error_line(
                    "Terrain has no destinations, so path-finding evaluation is not supported."
                ),
                error_type="UnsupportedTerrainError",
                error_message="Terrain has no destinations, so path-finding evaluation is not supported.",
            )

        oracle_name = test_spec.oracle_name or "dijkstra"
        oracle_cost, oracle_path = self._get_oracle_result(terrain_case, oracle_name)
        timeout_seconds = test_spec.time_limits.max_seconds or 0

        try:
            path_cost, elapsed_seconds, path = measure_function(
                search_function,
                terrain_case.terrain,
                iterations=iterations,
                debug=debug,
                max_seconds=timeout_seconds,
            )
        except Exception as exc:
            return TerrainEvaluationResult(
                terrain_case=terrain_case,
                function_name=function_name,
                success=False,
                elapsed_seconds=None,
                path_cost=None,
                path=None,
                oracle_name=oracle_name,
                oracle_cost=oracle_cost,
                oracle_path=oracle_path,
                optimal=False,
                within_time_limits=False,
                comments=_extract_last_error_line(str(exc)),
                error_type=type(exc).__name__,
                error_message=str(exc),
            )

        return TerrainEvaluationResult(
            terrain_case=terrain_case,
            function_name=function_name,
            success=True,
            elapsed_seconds=elapsed_seconds,
            path_cost=path_cost,
            path=path,
            oracle_name=oracle_name,
            oracle_cost=oracle_cost,
            oracle_path=oracle_path,
            optimal=(path_cost == oracle_cost),
            within_time_limits=_is_within_time_limits(elapsed_seconds, test_spec.time_limits),
            comments=None,
        )

    def _get_oracle_result(
        self,
        terrain_case: TerrainCase,
        oracle_name: str,
    ) -> Tuple[int, object]:
        cache_key = (id(terrain_case.terrain), oracle_name)
        if cache_key not in self._oracle_cache:
            oracle_function = resolve_oracle(oracle_name)
            oracle_cost, _, oracle_path = measure_function(
                oracle_function,
                terrain_case.terrain,
                max_seconds=0,
            )
            self._oracle_cache[cache_key] = (oracle_cost, oracle_path)
        return self._oracle_cache[cache_key]


def resolve_oracle(oracle_name: str) -> Callable:
    try:
        return ORACLE_REGISTRY[oracle_name]
    except KeyError as exc:
        supported = ", ".join(sorted(ORACLE_REGISTRY))
        raise ValueError(
            f"Unsupported oracle '{oracle_name}'. Supported oracles: {supported}"
        ) from exc


def _is_within_time_limits(
    elapsed_seconds: Optional[float], time_limits: TimeLimits
) -> Optional[bool]:
    if elapsed_seconds is None:
        return None
    if time_limits.min_seconds is not None and elapsed_seconds < time_limits.min_seconds:
        return False
    if time_limits.max_seconds is not None and elapsed_seconds > time_limits.max_seconds:
        return False
    return True


def _aggregate_test_results(
    case_results: Tuple[TerrainEvaluationResult, ...]
) -> Tuple[TestEvaluationResult, ...]:
    grouped_case_results: Dict[str, List[TerrainEvaluationResult]] = defaultdict(list)
    for case_result in case_results:
        grouped_case_results[case_result.terrain_case.test_id].append(case_result)

    aggregated_results: List[TestEvaluationResult] = []
    for test_id in sorted(grouped_case_results):
        test_case_results = grouped_case_results[test_id]
        successful_results = [result for result in test_case_results if result.success]
        average_time_seconds = None
        average_path_cost = None
        if successful_results:
            average_time_seconds = sum(
                result.elapsed_seconds for result in successful_results if result.elapsed_seconds is not None
            ) / len(successful_results)
            average_path_cost = sum(
                result.path_cost for result in successful_results if result.path_cost is not None
            ) / len(successful_results)

        optimality_ratio = sum(1 for result in test_case_results if result.optimal) / len(test_case_results)
        comments = _aggregate_comments(tuple(test_case_results))
        aggregated_results.append(
            TestEvaluationResult(
                test_id=test_id,
                average_time_seconds=average_time_seconds,
                average_path_cost=average_path_cost,
                optimality_ratio=optimality_ratio,
                comments=comments,
            )
        )

    return tuple(aggregated_results)


def _aggregate_comments(case_results: Tuple[TerrainEvaluationResult, ...]) -> Optional[str]:
    counts: Dict[str, int] = {}
    for result in case_results:
        if not result.comments:
            continue
        message = _extract_last_error_line(result.comments)
        counts[message] = counts.get(message, 0) + 1

    if not counts:
        return None
    return " | ".join(
        f"{count}x {message}" if count > 1 else message
        for message, count in counts.items()
    )


def _extract_last_error_line(message: str) -> str:
    lines = [line.strip() for line in message.splitlines() if line.strip()]
    if not lines:
        return message.strip()
    return lines[-1]
