from __future__ import annotations

import heapq
from typing import Dict

from sIArena.terrain.Terrain import Coordinate, Path, Terrain


def heuristic(terrain: Terrain, current: Coordinate, goal: Coordinate) -> float:
    """Admissible heuristic for sIArena terrains."""
    _ = terrain
    _ = current
    _ = goal
    # Safe lower bound for any non-negative edge-cost terrain.
    return 0.0


def _reconstruct_path(came_from: Dict[Coordinate, Coordinate], current: Coordinate) -> Path:
    path: Path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(terrain: Terrain) -> Path:
    start = terrain.origin
    goal = terrain.destination

    if start == goal:
        return [start]

    open_heap = [(heuristic(terrain, start, goal), 0.0, start)]
    came_from: Dict[Coordinate, Coordinate] = {}
    g_score: Dict[Coordinate, float] = {start: 0.0}

    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)

        if current_g > g_score.get(current, float("inf")):
            continue

        if current == goal:
            return _reconstruct_path(came_from, current)

        for neighbor in terrain.get_neighbors(current):
            tentative_g = current_g + terrain.get_cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(terrain, neighbor, goal)
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

    raise ValueError(f"No path found from {start} to {goal}")
