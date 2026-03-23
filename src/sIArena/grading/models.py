from dataclasses import dataclass, field
from pathlib import Path as FilePath
from typing import Any, Callable, Dict, Optional, Tuple

from sIArena.terrain.Terrain import NoPathTerrain, Path


@dataclass(frozen=True)
class AssignmentSpec:
    id: str
    notebook_function: str = "path_finding"
    author_from: str = "file_stem"
    author_pattern: Optional[str] = None


@dataclass(frozen=True)
class TimeLimits:
    max_seconds: Optional[float] = None
    min_seconds: Optional[float] = None


@dataclass(frozen=True)
class TerrainTestSpec:
    id: str
    generator_name: str
    seeds: Tuple[int, ...]
    parameters: Dict[str, Any]
    terrain_type_name: str = "Terrain"
    cost_function_name: Optional[str] = None
    oracle_name: Optional[str] = None
    time_limits: TimeLimits = field(default_factory=TimeLimits)


@dataclass(frozen=True)
class GraderConfig:
    version: int
    assignment: AssignmentSpec
    tests: Tuple[TerrainTestSpec, ...]


@dataclass(frozen=True)
class TerrainCase:
    test_id: str
    seed: int
    generator_name: str
    terrain_type_name: str
    terrain: NoPathTerrain

    @property
    def label(self) -> str:
        return f"{self.test_id}[seed={self.seed}]"


@dataclass(frozen=True)
class TerrainEvaluationResult:
    terrain_case: TerrainCase
    function_name: str
    success: bool
    elapsed_seconds: Optional[float]
    path_cost: Optional[int]
    path: Optional[Path]
    oracle_name: Optional[str]
    oracle_cost: Optional[int]
    oracle_path: Optional[Path]
    optimal: Optional[bool]
    within_time_limits: Optional[bool]
    comments: Optional[str] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class FunctionEvaluationResult:
    function_name: str
    test_results: Tuple["TestEvaluationResult", ...]
    case_results: Tuple[TerrainEvaluationResult, ...]
    comments: Optional[str] = None


@dataclass(frozen=True)
class TestEvaluationResult:
    test_id: str
    average_time_seconds: Optional[float]
    average_path_cost: Optional[float]
    optimality_ratio: float
    comments: Optional[str] = None


@dataclass(frozen=True)
class NotebookSubmission:
    notebook_path: FilePath
    file_name: str
    author: str
    function_name: str
    cell_index: int
    source_code: str
    search_function: Callable


@dataclass(frozen=True)
class NotebookEvaluationResult:
    submission: NotebookSubmission
    function_result: Optional[FunctionEvaluationResult]
    comments: Optional[str]
    load_error_type: Optional[str] = None
    load_error_message: Optional[str] = None


@dataclass(frozen=True)
class SubmissionGrade:
    file_name: str
    author: str
    test_results: Tuple[TestEvaluationResult, ...]
    optimality_percentage: float
    comments: Optional[str] = None


@dataclass(frozen=True)
class BatchEvaluationResult:
    assignment_id: str
    zip_file_name: str
    submission_grades: Tuple[SubmissionGrade, ...]
