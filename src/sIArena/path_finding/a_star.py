from __future__ import annotations

import math

from sIArena.path_finding._shared import build_complete_path, shortest_path
from sIArena.terrain.Terrain import Coordinate, Path, Terrain


def _minimum_step_cost(terrain: Terrain) -> float:
    minimum = math.inf

    for row in range(terrain.n):
        for column in range(terrain.m):
            current = (row, column)
            for neighbor in terrain.get_neighbors(current):
                minimum = min(minimum, terrain.get_cost(current, neighbor))

    if minimum == math.inf:
        return 0.0
    return float(minimum)


def heuristic(terrain: Terrain, current: Coordinate, goal: Coordinate) -> float:
    minimum_step_cost = _minimum_step_cost(terrain)
    return minimum_step_cost * (
        abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    )


def a_star(terrain: Terrain) -> Path:
    minimum_step_cost = _minimum_step_cost(terrain)

    def bounded_heuristic(
        current_terrain: Terrain, current: Coordinate, goal: Coordinate
    ) -> float:
        _ = current_terrain
        return minimum_step_cost * (
            abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        )

    return build_complete_path(
        terrain,
        lambda start, goal: shortest_path(terrain, start, goal, bounded_heuristic),
    )
