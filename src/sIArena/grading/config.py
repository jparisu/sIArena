import inspect
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

import yaml

from sIArena.grading.models import (
    AssignmentSpec,
    GraderConfig,
    TerrainTestSpec,
    TimeLimits,
)
from sIArena.grading.terrain_loader import (
    COST_FUNCTION_REGISTRY,
    GENERATOR_REGISTRY,
    TERRAIN_REGISTRY,
)


Coordinate = Tuple[int, int]
SUPPORTED_GENERATOR_PARAMETER_NAMES = tuple(
    inspect.signature(next(iter(GENERATOR_REGISTRY.values())).generate_random_terrain).parameters
)


def load_grader_config(path: Union[str, Path]) -> GraderConfig:
    with Path(path).open("r", encoding="utf-8") as stream:
        raw_config = yaml.safe_load(stream)
    return parse_grader_config(raw_config)


def parse_grader_config(raw_config: Mapping[str, Any]) -> GraderConfig:
    if not isinstance(raw_config, Mapping):
        raise TypeError("Grader configuration must be a mapping")

    version = int(raw_config.get("version", 1))
    assignment = _parse_assignment(raw_config.get("assignment", {}))
    defaults = raw_config.get("defaults", {})
    tests = raw_config.get("tests", [])

    if not isinstance(defaults, Mapping):
        raise TypeError("defaults must be a mapping")
    if not isinstance(tests, Sequence):
        raise TypeError("tests must be a sequence")

    parsed_tests = tuple(parse_test_spec(raw_test, defaults) for raw_test in tests)
    return GraderConfig(version=version, assignment=assignment, tests=parsed_tests)


def parse_test_spec(
    raw_test: Mapping[str, Any], defaults: Optional[Mapping[str, Any]] = None
) -> TerrainTestSpec:
    if not isinstance(raw_test, Mapping):
        raise TypeError("Each test specification must be a mapping")

    inherited_defaults = defaults or {}
    test_id = str(raw_test["id"])
    generator_name = str(raw_test["generator"])
    terrain_type_name = str(raw_test.get("terrain_type", inherited_defaults.get("terrain_type", "Terrain")))
    cost_function_name = raw_test.get("cost_function", inherited_defaults.get("cost_function"))
    oracle_name = raw_test.get("oracle", inherited_defaults.get("oracle"))
    seeds = _parse_seeds(raw_test["seeds"])
    parameters = _normalize_parameters(raw_test["parameters"], terrain_type_name)
    time_limits = _parse_time_limits(raw_test.get("time_limits"), inherited_defaults.get("time_limits"))
    _validate_generator_name(generator_name)
    _validate_terrain_type_name(terrain_type_name)
    _validate_cost_function_name(cost_function_name)
    _validate_parameters(parameters, terrain_type_name)

    return TerrainTestSpec(
        id=test_id,
        generator_name=generator_name,
        seeds=seeds,
        parameters=parameters,
        terrain_type_name=terrain_type_name,
        cost_function_name=cost_function_name,
        oracle_name=oracle_name,
        time_limits=time_limits,
    )


def _parse_assignment(raw_assignment: Mapping[str, Any]) -> AssignmentSpec:
    if not isinstance(raw_assignment, Mapping):
        raise TypeError("assignment must be a mapping")

    return AssignmentSpec(
        id=str(raw_assignment.get("id", "")),
        notebook_function=str(raw_assignment.get("notebook_function", "path_finding")),
        author_from=str(raw_assignment.get("author_from", "file_stem")),
        author_pattern=raw_assignment.get("author_pattern"),
    )


def _parse_time_limits(
    raw_time_limits: Optional[Mapping[str, Any]],
    default_time_limits: Optional[Mapping[str, Any]] = None,
) -> TimeLimits:
    merged: Dict[str, Any] = {}
    if isinstance(default_time_limits, Mapping):
        merged.update(default_time_limits)
    if isinstance(raw_time_limits, Mapping):
        merged.update(raw_time_limits)

    max_seconds = merged.get("max_seconds")
    min_seconds = merged.get("min_seconds")
    return TimeLimits(
        max_seconds=float(max_seconds) if max_seconds is not None else None,
        min_seconds=float(min_seconds) if min_seconds is not None else None,
    )


def _parse_seeds(raw_seeds: Sequence[Any]) -> Tuple[int, ...]:
    if not isinstance(raw_seeds, Sequence) or isinstance(raw_seeds, (str, bytes)):
        raise TypeError("seeds must be a sequence of integers")
    return tuple(int(seed) for seed in raw_seeds)


def _normalize_parameters(
    raw_parameters: Mapping[str, Any], terrain_type_name: str
) -> Dict[str, Any]:
    if not isinstance(raw_parameters, Mapping):
        raise TypeError("parameters must be a mapping")

    parameters = dict(raw_parameters)

    if "origin" in parameters:
        parameters["origin"] = _normalize_coordinate(parameters["origin"])
    if "destination" in parameters:
        parameters["destination"] = _normalize_destination(
            parameters["destination"], terrain_type_name
        )

    return parameters


def _normalize_coordinate(raw_coordinate: Sequence[Any]) -> Coordinate:
    if len(raw_coordinate) != 2:
        raise ValueError(f"Coordinate must have 2 elements: {raw_coordinate}")
    return int(raw_coordinate[0]), int(raw_coordinate[1])


def _normalize_destination(raw_destination: Any, terrain_type_name: str) -> Any:
    if terrain_type_name == "NoPathTerrain":
        return None
    if terrain_type_name == "Terrain":
        return _normalize_coordinate(raw_destination)
    if terrain_type_name == "MultipleDestinationTerrain":
        return {
            _normalize_coordinate(coordinate)
            for coordinate in raw_destination
        }
    if terrain_type_name == "SequentialDestinationTerrain":
        return [
            _normalize_coordinate(coordinate)
            for coordinate in raw_destination
        ]
    raise ValueError(f"Unsupported terrain type: {terrain_type_name}")


def _validate_generator_name(generator_name: str) -> None:
    if generator_name not in GENERATOR_REGISTRY:
        supported = ", ".join(sorted(GENERATOR_REGISTRY))
        raise ValueError(
            f"Unsupported generator '{generator_name}'. Supported generators: {supported}"
        )


def _validate_terrain_type_name(terrain_type_name: str) -> None:
    if terrain_type_name not in TERRAIN_REGISTRY:
        supported = ", ".join(sorted(TERRAIN_REGISTRY))
        raise ValueError(
            f"Unsupported terrain type '{terrain_type_name}'. Supported terrain types: {supported}"
        )


def _validate_cost_function_name(cost_function_name: Optional[str]) -> None:
    if cost_function_name is None:
        return
    if cost_function_name not in COST_FUNCTION_REGISTRY:
        supported = ", ".join(sorted(COST_FUNCTION_REGISTRY))
        raise ValueError(
            f"Unsupported cost function '{cost_function_name}'. Supported cost functions: {supported}"
        )


def _validate_parameters(parameters: Mapping[str, Any], terrain_type_name: str) -> None:
    unsupported = sorted(set(parameters) - set(SUPPORTED_GENERATOR_PARAMETER_NAMES))
    if unsupported:
        raise ValueError(
            f"Unsupported generator parameters in YAML: {', '.join(unsupported)}"
        )

    if "seed" in parameters:
        raise ValueError("seed must be declared in the top-level 'seeds' field, not inside parameters")

    if "terrain_ctor" in parameters:
        raise ValueError("terrain_ctor is controlled by 'terrain_type' and must not appear in parameters")

    if terrain_type_name == "NoPathTerrain":
        if "origin" in parameters:
            raise ValueError("NoPathTerrain does not support the 'origin' parameter")
        if "destination" in parameters:
            raise ValueError("NoPathTerrain does not support the 'destination' parameter")
        return

    if "destination" not in parameters:
        raise ValueError(
            f"{terrain_type_name} requires a 'destination' parameter in grader YAML"
        )
