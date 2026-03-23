from __future__ import annotations

from sIArena.path_finding._shared import (
    shortest_path,
    solve_multiple_destinations,
    solve_sequential_destinations,
    solve_single_destination,
)
from sIArena.terrain.Terrain import (
    Coordinate,
    MultipleDestinationTerrain,
    Path,
    SequentialDestinationTerrain,
    Terrain,
)


def heuristic(terrain: Terrain, current: Coordinate, goal: Coordinate) -> float:
    manhattan_distance = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    height_gain = max(0, terrain[goal] - terrain[current])
    return float(manhattan_distance + height_gain)


def _solve_standard_terrain(terrain: Terrain) -> Path:
    return solve_single_destination(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, heuristic),
    )


def _solve_sequential_destination_terrain(
    terrain: SequentialDestinationTerrain,
) -> Path:
    return solve_sequential_destinations(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, heuristic),
    )


def _solve_multiple_destination_terrain(
    terrain: MultipleDestinationTerrain,
) -> Path:
    return solve_multiple_destinations(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, heuristic),
    )


def a_star(terrain: Terrain) -> Path:
    if isinstance(terrain, MultipleDestinationTerrain):
        return _solve_multiple_destination_terrain(terrain)
    if isinstance(terrain, SequentialDestinationTerrain):
        return _solve_sequential_destination_terrain(terrain)
    return _solve_standard_terrain(terrain)
