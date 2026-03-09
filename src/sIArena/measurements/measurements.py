import math
import threading
import traceback
from typing import Tuple

from sIArena.terrain.Terrain import Terrain, Path
from sIArena.utils.Timer import Timer

def measure_function(
            search_function,
            terrain: Terrain,
            iterations: int = 1,
            debug: bool = False,
            max_seconds: float = 60*5
        ) -> Tuple[int, float, Path]:
    """
    This function uses a search function to calculate a path from the beginning to the end of a terrain.

    Parameters:
    - search_function: function that receives a Terrain and returns a path
    - terrain: Terrain to look for the path
    - iterations: Number of times the search will be repeated to measure time more accurately
    - debug: Whether to show debug information while
    - max_seconds: Timeout in seconds. If set to 0, no thread is used (direct call).

    Returns:
    - The minimum cost of the path found
    - The average time that the function has elapsed to find it
    """

    # Function to return the result/exception as parameters
    def func_wrapper(func, terrain, result, errors):
        try:
            result.append(func(terrain))
        except Exception as exc:  # pragma: no cover - behavior validated from the caller side
            errors.append((exc, traceback.format_exc()))

    best_path_cost = math.inf
    best_path = None
    times = []

    for i in range(iterations):

        if debug:
            print(f"Running iteration {i}...")

        # List for the result of the function
        result = []
        errors = []

        # Start timer
        timer = Timer()

        if max_seconds == 0:
            # Run directly to expose the original traceback for student debugging.
            path = search_function(terrain)
        else:
            # Thread with timeout
            thread = threading.Thread(target=func_wrapper, args=(search_function, terrain, result, errors,))

            # Start thread
            thread.start()
            thread.join(timeout=max_seconds)

            if thread.is_alive():
                raise TimeoutError(f"Function {search_function.__name__} took more than {max_seconds} seconds to finish.")

            if errors:
                original_error, original_traceback = errors[0]
                raise RuntimeError(
                    f"Error inside user function {search_function.__name__}: "
                    f"{type(original_error).__name__}: {original_error}\n"
                    f"Original traceback (inside user function):\n{original_traceback}"
                ) from original_error

            if len(result) == 0:
                raise RuntimeError(
                    f"Function {search_function.__name__} did not return any path and no exception was captured."
                )

            path = result[0]

        # Store time
        times.append(timer.elapsed_s())

        valid = terrain.why_complete_path(path)
        if not valid[0]:
            raise ValueError(f"Function {search_function.__name__} returned an invalid path: {valid[1]}")

        cost = terrain.get_path_cost(path)
        if cost < best_path_cost:
            best_path_cost = cost
            best_path = path

        if debug:
            print(f"In iteration {i} found path with cost {cost} in {times[-1]} seconds.")
            print()

    return (best_path_cost, sum(times)/iterations, best_path)
