from .connectors import Client
from .fsm import FSM

class App(FSM):

	def __init__(self, ip="127.0.0.1", port="5555"):
		self.connection = Client(ip, port)
		super().__init__()

	def run(self):
		d = dict()
		d["connection"] = self.connection
		super().run(d)


if __name__== "__main__" :
	pass
