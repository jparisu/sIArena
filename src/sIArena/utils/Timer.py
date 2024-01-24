import time

class Timer:
    """Object to measure times of code execution"""
    def __init__(self, start_paused=False):
        """
        Creates a new timer object.

        :param start_paused: If True, the timer will start paused
        """
        self.start = None           # type: float
        self.pause_time = None      # type: float
        self.accumulated = None     # type: float
        self.paused = None          # type: bool

        self.reset(start_paused)


    def __enter__(self):
        """Starts the timer"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Stops the timer and prints the elapsed time"""
        print(f"TIMER: {self.elapsed()}")

    def elapsed_s(self) -> float:
        """Returns the elapsed time in seconds"""
        if self.paused:
            return self.pause_time - self.start + self.accumulated
        else:
            return time.time() - self.start + self.accumulated

    def elapsed_ms(self) -> float:
        """Returns the elapsed time in milliseconds"""
        return self.elapsed_s() * 1000

    def pause(self):
        """Pauses the timer"""
        self.pause_time = time.time()
        self.accumulated += time.time() - self.pause_time
        self.paused = True

    def resume(self):
        """Resumes the timer"""
        self.start += time.time() - self.pause_time
        self.pause_time = None
        self.paused = False

    def reset(self, paused: bool = None):
        """Resets the timer as if it was just created"""
        if paused is None:
            paused = self.paused

        if self.paused:
            self.start = time.time()
            self.pause_time = self.start
            self.accumulated = 0.0
        else:
            self.start = time.time()
            self.pause_time = None
            self.accumulated = 0.0
