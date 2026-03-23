import unittest
from unittest.mock import patch

from sIArena.utils.Timer import Timer


class TestTimer(unittest.TestCase):
    def test_init_sets_baseline_fields(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        self.assertEqual(timer.start, 100.0)
        self.assertIsNone(timer.pause_time)
        self.assertEqual(timer.accumulated, 0.0)
        self.assertIsNone(timer.paused)

    def test_enter_returns_self(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        self.assertIs(timer.__enter__(), timer)

    def test_exit_prints_elapsed_time(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        with patch.object(timer, "elapsed", return_value=1.25, create=True):
            with patch("builtins.print") as print_mock:
                timer.__exit__(None, None, None)

        print_mock.assert_called_once_with("TIMER: 1.25")

    def test_elapsed_s_uses_current_time_when_not_paused(self):
        with patch("sIArena.utils.Timer.time.time", side_effect=[100.0, 103.5]):
            timer = Timer()
            timer.accumulated = 1.5

            elapsed = timer.elapsed_s()

        self.assertEqual(elapsed, 5.0)

    def test_elapsed_s_uses_pause_time_when_paused(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        timer.paused = True
        timer.pause_time = 106.0
        timer.accumulated = 2.0

        self.assertEqual(timer.elapsed_s(), 8.0)

    def test_elapsed_ms_scales_seconds(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        with patch.object(timer, "elapsed_s", return_value=1.75):
            self.assertEqual(timer.elapsed_ms(), 1750.0)

    def test_pause_sets_pause_state_using_two_time_reads(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        with patch("sIArena.utils.Timer.time.time", side_effect=[110.0, 115.0]):
            timer.pause()

        self.assertEqual(timer.pause_time, 110.0)
        self.assertEqual(timer.accumulated, 5.0)
        self.assertTrue(timer.paused)

    def test_resume_restores_running_state(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        timer.pause_time = 110.0
        timer.paused = True

        with patch("sIArena.utils.Timer.time.time", return_value=118.0):
            timer.resume()

        self.assertEqual(timer.start, 108.0)
        self.assertIsNone(timer.pause_time)
        self.assertFalse(timer.paused)

    def test_reset_uses_current_pause_state_instead_of_argument(self):
        with patch("sIArena.utils.Timer.time.time", return_value=100.0):
            timer = Timer()

        timer.paused = True
        with patch("sIArena.utils.Timer.time.time", return_value=200.0):
            timer.reset(paused=False)

        self.assertEqual(timer.start, 200.0)
        self.assertEqual(timer.pause_time, 200.0)
        self.assertEqual(timer.accumulated, 0.0)
