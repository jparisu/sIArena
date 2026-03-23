import unittest
from unittest.mock import Mock, patch

from sIArena.measurements.measurements import measure_function


class DummyTerrain:
    def __init__(self, valid=True):
        self.valid = valid

    def why_complete_path(self, path):
        if self.valid:
            return True, "ok"
        return False, "bad path"

    def get_path_cost(self, path):
        return sum(path)


class TestMeasureFunction(unittest.TestCase):
    def test_runs_directly_when_max_seconds_is_zero(self):
        terrain = DummyTerrain()

        with patch("sIArena.measurements.measurements.Timer") as timer_cls:
            timer_cls.return_value.elapsed_s.return_value = 0.25

            cost, elapsed, path = measure_function(
                lambda current_terrain: [1, 2, 3],
                terrain,
                iterations=1,
                max_seconds=0,
            )

        self.assertEqual(cost, 6)
        self.assertEqual(elapsed, 0.25)
        self.assertEqual(path, [1, 2, 3])

    def test_returns_best_path_and_average_time_over_iterations(self):
        terrain = DummyTerrain()
        paths = iter(([2, 2], [1, 1], [3, 3]))

        with patch("sIArena.measurements.measurements.Timer") as timer_cls:
            timer_cls.side_effect = [Mock(elapsed_s=Mock(return_value=1.0)),
                                     Mock(elapsed_s=Mock(return_value=2.0)),
                                     Mock(elapsed_s=Mock(return_value=3.0))]

            cost, elapsed, path = measure_function(
                lambda current_terrain: next(paths),
                terrain,
                iterations=3,
                max_seconds=0,
            )

        self.assertEqual(cost, 2)
        self.assertEqual(elapsed, 2.0)
        self.assertEqual(path, [1, 1])

    def test_wraps_exception_from_threaded_function(self):
        terrain = DummyTerrain()

        def failing_search(current_terrain):
            raise ValueError("boom")

        with self.assertRaisesRegex(RuntimeError, "ValueError: boom"):
            measure_function(failing_search, terrain, max_seconds=1)

    def test_raises_timeout_for_slow_threaded_function(self):
        terrain = DummyTerrain()

        def slow_search(current_terrain):
            import time
            time.sleep(0.05)
            return [1]

        with self.assertRaisesRegex(TimeoutError, "took more than 0.001 seconds"):
            measure_function(slow_search, terrain, max_seconds=0.001)

    def test_raises_when_thread_returns_no_result(self):
        terrain = DummyTerrain()

        class FakeThread:
            def __init__(self, target, args):
                self.target = target
                self.args = args

            def start(self):
                return None

            def join(self, timeout=None):
                return None

            def is_alive(self):
                return False

        with patch("sIArena.measurements.measurements.threading.Thread", FakeThread):
            with self.assertRaisesRegex(RuntimeError, "did not return any path"):
                measure_function(lambda current_terrain: [1], terrain, max_seconds=1)

    def test_raises_for_invalid_path(self):
        terrain = DummyTerrain(valid=False)

        with self.assertRaisesRegex(ValueError, "returned an invalid path: bad path"):
            measure_function(lambda current_terrain: [1, 2], terrain, max_seconds=0)

    def test_debug_prints_iteration_information(self):
        terrain = DummyTerrain()

        with patch("sIArena.measurements.measurements.Timer") as timer_cls:
            timer_cls.return_value.elapsed_s.return_value = 0.5
            with patch("builtins.print") as print_mock:
                measure_function(
                    lambda current_terrain: [1, 1],
                    terrain,
                    iterations=1,
                    debug=True,
                    max_seconds=0,
                )

        printed_lines = [" ".join(str(part) for part in call.args) for call in print_mock.call_args_list]
        self.assertTrue(any("Running iteration 0..." in line for line in printed_lines))
        self.assertTrue(any("found path with cost 2 in 0.5 seconds." in line for line in printed_lines))
