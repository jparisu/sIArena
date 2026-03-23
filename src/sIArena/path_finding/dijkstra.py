from __future__ import annotations

from sIArena.path_finding._shared import build_complete_path, shortest_path
from sIArena.terrain.Terrain import Coordinate, Path, Terrain


def _zero_heuristic(
    terrain: Terrain, current: Coordinate, goal: Coordinate
) -> float:
    _ = terrain
    _ = current
    _ = goal
    return 0.0


def dijkstra(terrain: Terrain) -> Path:
    return build_complete_path(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, _zero_heuristic),
    )
