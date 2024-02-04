import math
import threading
import time
from typing import List, Tuple

from sIArena.terrain.Terrain import Coordinate, Terrain, Path
from sIArena.utils.Timer import Timer

def measure_function(
            search_function,
            terrain: Terrain,
            iterations: int = 1,
            debug: bool = False,
            max_seconds: float = 60*5
        ) -> Tuple[int, float, Path]:
    """
    This function uses a search function to calculate a path from the beggining to the end of a terrain.

    Parameters:
    - search_function: function that receives a Terrain and returns a path
    - terrain: Terrain to look for the path
    - iterations: Number of times the search will be repeated to measure time more accurately
    - debug: Whether to show debug information while

    Returns:
    - The minimum cost of the path found
    - The average time that the function has elapsed to find it
    """

    # Function to return the result as a parameter
    def func_wrapper(func, terrain, result):
        result.append(func(terrain))

    best_path_cost = math.inf
    best_path = None
    times = []

    for i in range(iterations):

        if debug:
            print(f"Running iteration {i}...")

        # List for the result of the function
        result = []

        # Thread with timeout
        thread = threading.Thread(target=func_wrapper, args=(search_function, terrain, result,))

        # Start timer
        timer = Timer()

        # Start thread
        thread.start()
        thread.join(timeout=max_seconds)

        # Store time
        times.append(timer.elapsed_s())

        if thread.is_alive():
            raise TimeoutError(f"Function {search_function.__name__} took more than {max_seconds} seconds to finish.")
        else:
            if len(result) == 0:
                raise ValueError(f"Function {search_function.__name__} finished with an error.")
            else:
                path = result[0]

        if not terrain.is_complete_path(path):
            raise ValueError(f"Found Incorrect path with function {search_function.__name__}: {path}")

        cost = terrain.get_path_cost(path)
        if cost < best_path_cost:
            best_path_cost = cost
            best_path = path

        if debug:
            print(f"In iteration {i} found path with cost {cost} in {times[-1]} seconds.")
            print()

    return (best_path_cost, sum(times)/iterations, best_path)
