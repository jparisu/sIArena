from collections import defaultdict
from typing import Callable, Dict, List, Optional, Type

from sIArena.grading.models import GraderConfig, TerrainCase, TerrainTestSpec
from sIArena.terrain.Terrain import (
    MultiEndpointTerrain,
    MultipleDestinationTerrain,
    NoPathTerrain,
    SequentialDestinationTerrain,
    Terrain,
    default_cost_function,
)
from sIArena.terrain.generator.FocusedGenerator import FocusedGenerator
from sIArena.terrain.generator.Generator import TerrainGenerator
from sIArena.terrain.generator.MazeGenerator import MazeGenerator
from sIArena.terrain.generator.PerlinGenerator import PerlinGenerator


GENERATOR_REGISTRY: Dict[str, Type[TerrainGenerator]] = {
    "FocusedGenerator": FocusedGenerator,
    "MazeGenerator": MazeGenerator,
    "PerlinGenerator": PerlinGenerator,
}

TERRAIN_REGISTRY: Dict[str, Type[NoPathTerrain]] = {
    "NoPathTerrain": NoPathTerrain,
    "Terrain": Terrain,
    "MultiEndpointTerrain": MultiEndpointTerrain,
    "MultipleDestinationTerrain": MultipleDestinationTerrain,
    "SequentialDestinationTerrain": SequentialDestinationTerrain,
}

COST_FUNCTION_REGISTRY: Dict[str, Callable[..., int]] = {
    "default_cost_function": default_cost_function,
}


def resolve_generator(generator_name: str) -> TerrainGenerator:
    try:
        return GENERATOR_REGISTRY[generator_name]()
    except KeyError as exc:
        supported = ", ".join(sorted(GENERATOR_REGISTRY))
        raise ValueError(
            f"Unsupported generator '{generator_name}'. Supported generators: {supported}"
        ) from exc


def resolve_terrain_ctor(terrain_type_name: str) -> Type[NoPathTerrain]:
    try:
        return TERRAIN_REGISTRY[terrain_type_name]
    except KeyError as exc:
        supported = ", ".join(sorted(TERRAIN_REGISTRY))
        raise ValueError(
            f"Unsupported terrain type '{terrain_type_name}'. Supported terrain types: {supported}"
        ) from exc


def resolve_cost_function(cost_function_name: Optional[str]) -> Optional[Callable[..., int]]:
    if cost_function_name is None:
        return None
    try:
        return COST_FUNCTION_REGISTRY[cost_function_name]
    except KeyError as exc:
        supported = ", ".join(sorted(COST_FUNCTION_REGISTRY))
        raise ValueError(
            f"Unsupported cost function '{cost_function_name}'. Supported cost functions: {supported}"
        ) from exc


def _build_no_path_terrain_ctor(
    cost_function: Optional[Callable[..., int]],
) -> Callable[..., NoPathTerrain]:
    def terrain_ctor(matrix, origin=None, destination=None, cost_function=cost_function):
        _ = origin
        _ = destination
        if cost_function is None:
            return NoPathTerrain(matrix)
        return NoPathTerrain(matrix, cost_function=cost_function)

    return terrain_ctor


def build_terrain_case(test_spec: TerrainTestSpec, seed: int) -> TerrainCase:
    generator = resolve_generator(test_spec.generator_name)
    cost_function = resolve_cost_function(test_spec.cost_function_name)

    if test_spec.terrain_type_name == "NoPathTerrain":
        terrain_ctor = _build_no_path_terrain_ctor(cost_function)
    else:
        terrain_ctor = resolve_terrain_ctor(test_spec.terrain_type_name)

    terrain_parameters = dict(test_spec.parameters)
    terrain_parameters["seed"] = seed
    terrain_parameters["terrain_ctor"] = terrain_ctor
    if cost_function is not None and test_spec.terrain_type_name != "NoPathTerrain":
        terrain_parameters["cost_function"] = cost_function

    terrain = generator.generate_random_terrain(**terrain_parameters)
    return TerrainCase(
        test_id=test_spec.id,
        seed=seed,
        generator_name=test_spec.generator_name,
        terrain_type_name=test_spec.terrain_type_name,
        terrain=terrain,
    )


def build_terrain_cases(config: GraderConfig) -> List[TerrainCase]:
    terrain_cases: List[TerrainCase] = []
    for test_spec in config.tests:
        for seed in test_spec.seeds:
            terrain_cases.append(build_terrain_case(test_spec, seed))
    return terrain_cases


def build_terrain_cases_by_test(config: GraderConfig) -> Dict[str, List[TerrainCase]]:
    grouped_terrain_cases: Dict[str, List[TerrainCase]] = defaultdict(list)
    for terrain_case in build_terrain_cases(config):
        grouped_terrain_cases[terrain_case.test_id].append(terrain_case)
    return dict(grouped_terrain_cases)
