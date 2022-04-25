"""Finite state machine."""

from abc import ABC

class FSM(ABC):
	"""Finite state machine."""

	def __init__(self):
		"""Initialise the FSM."""
		self.handlers = {}
		self.startState = None
		self.endStates = []
		self.inRunAtLeastOnce = False
		self.handler = None

	def add_state(self, name, handler, end_state=0):
		"""Add a state to the FSM."""
		name = name.upper()
		self.handlers[name] = handler
		if end_state:
			self.endStates.append(name)

	def set_start(self, name):
		"""Set the starting state to the FSM."""
		self.startState = name.upper()

	def run(self, arg):
		"""Run the FSM."""
		if self.inRunAtLeastOnce is False:
			try:
				self.handler = self.handlers[self.startState]
			except Exception:
				raise Exception("must call .set_start() before .run()")
			if not self.endStates:
				raise Exception("at least one state must be an end_state")
			self.inRunAtLeastOnce = True

		newState = self.handler(arg)
		if newState.upper() in self.endStates:
			print("reached ", newState)
		else:
			self.handler = self.handlers[newState.upper()]


if __name__ == "__main__":
	pass
