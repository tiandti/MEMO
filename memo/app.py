"""This is the main application of memo."""

from .connectors import Client
from .fsm import FSM


class App(FSM):
	"""Application that encapsulates a finite state machine and a client socket connection."""

	def __init__(self, ip="127.0.0.1", port="5555"):
		"""Application constructor."""
		self.connection = Client(ip, port)
		super().__init__()

	def run(self):
		"""Run an iteration of the application."""
		d = dict()
		d["connection"] = self.connection
		super().run(d)


if __name__ == "__main__":
	pass
