from __future__ import annotations

import heapq
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


def solve_single_destination(
    terrain: Terrain,
    solve_segment: SegmentSolver,
) -> Path:
    return solve_segment(terrain.origin, terrain.destination)


def solve_sequential_destinations(
    terrain: SequentialDestinationTerrain,
    solve_segment: SegmentSolver,
) -> Path:
    destinations = terrain.get_destinations()
    if not destinations:
        raise ValueError("Terrain must define at least one destination")

    current = terrain.origin
    full_path: Path = [current]

    for goal in destinations:
        segment = solve_segment(current, goal)
        full_path = extend_path(full_path, segment)
        current = goal

    return full_path


def solve_multiple_destinations(
    terrain: MultipleDestinationTerrain,
    solve_segment: SegmentSolver,
) -> Path:
    destinations = terrain.get_destinations()
    if not destinations:
        raise ValueError("Terrain must define at least one destination")

    ordered_destinations = sorted(destinations)
    segment_paths: Dict[tuple[Coordinate, Coordinate], Path] = {}
    segment_costs: Dict[tuple[Coordinate, Coordinate], float] = {}
    relevant_points = [terrain.origin] + ordered_destinations

    for start in relevant_points:
        for goal in ordered_destinations:
            if start == goal:
                continue
            segment = solve_segment(start, goal)
            segment_paths[(start, goal)] = segment
            segment_costs[(start, goal)] = float(terrain.get_path_cost(segment))

    destination_count = len(ordered_destinations)
    best_cost_by_state: Dict[tuple[int, int], float] = {}
    predecessor_by_state: Dict[tuple[int, int], int | None] = {}

    for destination_index, destination in enumerate(ordered_destinations):
        mask = 1 << destination_index
        best_cost_by_state[(mask, destination_index)] = segment_costs[
            (terrain.origin, destination)
        ]
        predecessor_by_state[(mask, destination_index)] = None

    full_mask = (1 << destination_count) - 1
    for mask in range(1, full_mask + 1):
        for destination_index, destination in enumerate(ordered_destinations):
            if not mask & (1 << destination_index):
                continue

            previous_mask = mask ^ (1 << destination_index)
            if previous_mask == 0:
                continue

            best_cost = float("inf")
            best_predecessor = None

            for previous_index, previous_destination in enumerate(ordered_destinations):
                if not previous_mask & (1 << previous_index):
                    continue

                candidate_cost = best_cost_by_state[
                    (previous_mask, previous_index)
                ] + segment_costs[(previous_destination, destination)]
                if candidate_cost < best_cost:
                    best_cost = candidate_cost
                    best_predecessor = previous_index

            best_cost_by_state[(mask, destination_index)] = best_cost
            predecessor_by_state[(mask, destination_index)] = best_predecessor

    end_index = min(
        range(destination_count),
        key=lambda destination_index: best_cost_by_state[(full_mask, destination_index)],
    )

    order_indices = []
    mask = full_mask
    current_index = end_index
    while True:
        order_indices.append(current_index)
        previous_index = predecessor_by_state[(mask, current_index)]
        if previous_index is None:
            break
        mask ^= 1 << current_index
        current_index = previous_index
    order_indices.reverse()

    full_path: Path = [terrain.origin]
    visited_destinations = set()
    current = terrain.origin

    for destination_index in order_indices:
        goal = ordered_destinations[destination_index]
        if goal in visited_destinations:
            continue
        segment = segment_paths[(current, goal)]
        full_path = extend_path(full_path, segment)
        current = goal
        for coordinate in segment:
            if coordinate in destinations:
                visited_destinations.add(coordinate)

    return full_path
