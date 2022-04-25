"""Network client/server."""

import socket
import selectors
import types
from virtualbus.client import Client as VClient
import queue


class Client:
	"""Network communication as a client."""

	def __init__(self, ip, port):
		"""Initialise the client."""
		self.con = VClient(host=ip, port=port, logging=True)

	def send(self, data):
		"""Send data."""
		self.con.sent(data.decode())

	def receive(self):
		"""Receive data."""
		data = self.con.receive()
		return data


class Server:
	"""Network communication as the server."""

	def __init__(self, port):
		"""Initialise the server."""
		# Assign attributes
		host = 'localhost'
		self.port = port
		self.selector = selectors.DefaultSelector()
		self.data = queue.Queue()

		# Create socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

		# Allow multiple connections
		# self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.socket.bind((host, self.port))
		self.socket.listen()
		print(f"[SERVER]: Listening on '{host}:{self.port}'")

		# Set to non blocking
		self.socket.setblocking(False)

		# Select socket
		self.selector.register(self.socket, selectors.EVENT_READ, data=None)

	def __del__(self):
		"""Deinitialise the server."""
		print("[Server]: Closing")
		self.socket.close()
		self.socket = None

	def send(self, data):
		"""Send data."""
		rv = False
		try:
			self.socket.send(data)
			rv = True
		except BrokenPipeError:
			pass
		return rv

	def sendall(self, data):
		"""Send data to all clients."""
		raise NotImplementedError

	def _accept_wrapper(self, sock):
		conn, addr = sock.accept()  # Should be ready to read
		print(f"[Server]: Accepted connection from {addr}")
		conn.setblocking(False)
		data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.selector.register(conn, events, data=data)

	def _service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(4096)  # Should be ready to read
			if recv_data:
				data.outb += recv_data
				self.data.put(recv_data)
				# print(f"[Server]: Echo {data.outb!r} to {data.addr}")
			else:
				print(f"[Server]: Closing connection to {data.addr}")
				self.selector.unregister(sock)
				sock.close()
		"""
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				# print(f"[Server]: Echoing {data.outb!r} to {data.addr}")
				# sent = sock.send(data.outb)  # Should be ready to write
				# data.outb = data.outb[sent:]
				pass
		"""

	def receive(self):
		"""Receive data."""
		# while True:
		data = None
		events = self.selector.select(timeout=1.0)
		for key, mask in events:
			if key.data is None:
				self._accept_wrapper(key.fileobj)
			else:
				self._service_connection(key, mask)

		length = self.data.qsize()
		if length > 0:
			data = self.data.get()
		return data

	# def isAlive(self):
	# 	return self.socket is not None


if __name__ == "__main__":
	pass
