from abc import ABC
from abc import abstractmethod
# from dataclasses import dataclass
import zmq


class IConnection(ABC):

	@abstractmethod
	def send(self, data):
		"""Send data"""

	@abstractmethod
	def send(self, data):
		"""Receive data"""


class Client(IConnection):
	def __init__(self, ip="127.0.0.1", port="5555"):
		print(f"Starting client {ip}:{port}")
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		connectionStr = f"tcp://{ip}:{port}"
		print(f"connectionStr = '{connectionStr}'")
		self.socket.connect(connectionStr)
		print("Done")

	def send(self, data):
		print(f"Sending {data}")
		self.socket.send(data)
		print(f"Sending finished")

	def receive(self):
		data = self.socket.recv()
		print(f"Receiced {data}")
		return data
		print(f"Receive finished")


class Server(IConnection):
	def __init__(self, ip="127.0.0.1", port="5555"):
		print(f"Starting server {ip}:{port}")
		context = zmq.Context()
		self.socket = context.socket(zmq.REP)
		connectionStr = f"tcp://{ip}:{port}"
		print(f"connectionStr = '{connectionStr}'")
		self.socket.bind(connectionStr)
		print("Done")

	def send(self, data):
		print(f"Sending {data}")
		self.socket.send(data)

	def receive(self):
		data = self.socket.recv()
		print(f"Receiced {data}")
		return data


if __name__== "__main__" :
	pass
