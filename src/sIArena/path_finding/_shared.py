from __future__ import annotations

import heapq
import math
from typing import Callable, Dict

from sIArena.terrain.Terrain import (
    Coordinate,
    MultipleDestinationTerrain,
    Path,
    SequentialDestinationTerrain,
    Terrain,
)


Heuristic = Callable[[Terrain, Coordinate, Coordinate], float]
SegmentSolver = Callable[[Coordinate, Coordinate], Path]


def reconstruct_path(
    came_from: Dict[Coordinate, Coordinate], current: Coordinate
) -> Path:
    path: Path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def shortest_path(
    terrain: Terrain,
    start: Coordinate,
    goal: Coordinate,
    heuristic: Heuristic,
) -> Path:
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
            return reconstruct_path(came_from, current)

        for neighbor in terrain.get_neighbors(current):
            tentative_g = current_g + terrain.get_cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(terrain, neighbor, goal)
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

    raise ValueError(f"No path found from {start} to {goal}")


def extend_path(base_path: Path, segment: Path) -> Path:
    if len(segment) == 0:
        raise ValueError("Path segment cannot be empty")
    if len(base_path) == 0:
        return list(segment)
    if base_path[-1] != segment[0]:
        raise ValueError(
            f"Cannot merge segment starting at {segment[0]} into path ending at {base_path[-1]}"
        )
    return base_path + segment[1:]


def build_complete_path(terrain: Terrain, solve_segment: SegmentSolver) -> Path:
    destinations = terrain.get_destinations()
    if not destinations:
        raise ValueError("Terrain must define at least one destination")

    current = terrain.origin
    full_path: Path = [current]

    if isinstance(terrain, MultipleDestinationTerrain):
        remaining = set(destinations)

        while remaining:
            best_goal = None
            best_segment = None
            best_cost = math.inf

            for goal in sorted(remaining):
                segment = solve_segment(current, goal)
                cost = terrain.get_path_cost(segment)
                if cost < best_cost:
                    best_goal = goal
                    best_segment = segment
                    best_cost = cost

            if best_goal is None or best_segment is None:
                raise ValueError(f"No path found from {current} to the remaining destinations")

            full_path = extend_path(full_path, best_segment)
            current = best_goal
            remaining.remove(best_goal)

        return full_path

    ordered_destinations = list(destinations)

    for goal in ordered_destinations:
        segment = solve_segment(current, goal)
        full_path = extend_path(full_path, segment)
        current = goal

    return full_path
