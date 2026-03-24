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


def _zero_heuristic(
    terrain: Terrain, current: Coordinate, goal: Coordinate
) -> float:
    _ = terrain
    _ = current
    _ = goal
    return 0.0


def _solve_standard_terrain(terrain: Terrain) -> Path:
    return solve_single_destination(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, _zero_heuristic),
    )


def _solve_sequential_destination_terrain(
    terrain: SequentialDestinationTerrain,
) -> Path:
    return solve_sequential_destinations(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, _zero_heuristic),
    )


def _solve_multiple_destination_terrain(
    terrain: MultipleDestinationTerrain,
) -> Path:
    return solve_multiple_destinations(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, _zero_heuristic),
    )


def dijkstra(terrain: Terrain) -> Path:
    if isinstance(terrain, MultipleDestinationTerrain):
        return _solve_multiple_destination_terrain(terrain)
    if isinstance(terrain, SequentialDestinationTerrain):
        return _solve_sequential_destination_terrain(terrain)
    return _solve_standard_terrain(terrain)
