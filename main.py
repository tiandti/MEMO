import tkinter as tk
import queue

# from tkvideo import tkvideo
from PIL import Image, ImageTk
import threading
import argparse
import time


from memo.connectors import Client
from memo.connectors import Server
# from memo.ui import UI


class UI:
	def __init__(self):
		self.event = threading.Event()
		self.image_path = ""

		self.quitEvent = threading.Event()

		self.q = queue.Queue()

		self.thread = threading.Thread(target=self._thread)
		self.thread.start()

	def isRunning(self):
		return not self.quitEvent.isSet()

	def close(self):
		print("UI closing")
		self.quitEvent.set()

	def _thread(self):
		self.root = tk.Tk()
		self.root.bind("<Escape>", lambda x: self.close())
		height = self.root.winfo_screenheight()
		width = self.root.winfo_screenwidth()
		print(f"Screen: {width} x {height} (in pixels)\n")

		# Create a image holder
		self.media = tk.Label(image="", background="black")
		self.media.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

		while not self.quitEvent.isSet():

			self.root.update_idletasks()
			self.root.update()

			if self.q.qsize():
				try:
					image_path = self.q.get_nowait()
					# Check contents of message and do whatever is needed. As a
					# simple example, let's print it (in real life, you would
					# suitably update the GUI's display in a richer fashion).
					# print(msg)
					image = ""
					if image_path != "":
						try:
							raw_image = Image.open(image_path)
							image = ImageTk.PhotoImage(raw_image)
						except FileNotFoundError:
							image = ""
					self.media.configure(image=image)
					self.media.image = image
				except queue.Empty:
					# just on general principles, although we don't expect this
					# branch to be taken in this case, ignore this exception!
					pass

		while self.q.qsize():
			try:
				self.q.get_nowait()
			except queue.Empty:
				# just on general principles, although we don't expect this
				# branch to be taken in this case, ignore this exception!
				pass
		print("UI internal Thread Done")


	def replace(self, image_path):
		if self.isRunning():
			self.q.put(image_path)


def socketTask(ip, port, args, ui):

	if not args.daemon:
		con = Client(ip, port)
		print("1")
		con.send(args.bar.encode())
		print("2")
		msg = con.receive()
		print(f"msg: {msg.decode()}")
	else:
		con = Server(ip, port)
		while ui.isRunning():

			print("Fuck I am here")

			msg = con.receive()
			msg = msg.decode("utf-8")
			print(f"Msg: '{msg}'")

			ui.replace(msg)
			reply = "Done"
			con.send(reply.encode("utf-8"))
	print("3")

def main():
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument('--bar')

	parser.add_argument("-a", "--address",
			    help = "Selects the server ip address or hostname. Default is '127.0.0.1'",
			    default = "127.0.0.1")
	parser.add_argument("-p", "--port",
			    help = "When mode is socket, selects the server port. Default is '5555'",
			    type = int, default = 5555)
	parser.add_argument("-d", "--daemon",
			    help = "Run as a daemon.",
			    action='store_true')
	args = parser.parse_args()

	ip = str(args.address)
	port = int(args.port)
	isDaemon = args.daemon

	if not isDaemon:
		#socketTask(args, None)
		#socketThread = threading.Thread(target=socketTask, args=(ip, port, args, None,))
		#socketThread.start()
		con = Client(ip, port)
		print("1")
		con.send(args.bar.encode())
		print("2")
		msg = con.receive()
		print(f"msg: {msg.decode()}")
		print("3")

		exit(0)
	else:
		ui = UI()
		print("Socket before thread")
		socketThread = threading.Thread(target=socketTask, args=(ip, port, args, ui))
		print("Socket before start")
		socketThread.start()
		print("Socket before join")
		socketThread.join()
		print("Socket end")
	print("main end")

if __name__== "__main__" :
	try:
		main()
	except KeyboardInterrupt:
		print('\nHello user you have pressed ctrl-c button.')
		pass
