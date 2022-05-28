"""Timer."""

import time


class TimerError(Exception):
	"""A custom exception used to report errors in use of Timer class."""


class Timer:
	"""Timer."""

	def __init__(self):
		"""Create a timer."""
		self._start_time = None

	def start(self):
		"""Start the timer."""
		if self._start_time is not None:
			raise TimerError("Timer is running. Use .stop() to stop it")
		self._start_time = time.perf_counter()

	def stop(self):
		"""Stop the timer."""
		self._start_time = None

	def elapsed(self):
		"""Report the elapsed time in seconds."""
		if self._start_time is None:
			raise TimerError("Timer is not running. Use .start() to start it")
		elapsed_time = time.perf_counter() - self._start_time
		return elapsed_time
