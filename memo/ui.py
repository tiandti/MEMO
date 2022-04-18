import tkinter as tk
# from tkvideo import tkvideo
from PIL import Image, ImageTk
import threading
import queue


class UI:
	def __init__(self):
		self.event = threading.Event()
		self.image_path = ""
		self.running = False

		self.quitEvent = threading.Event()

		self.q = queue.Queue()

		self.thread = threading.Thread(target=self._thread)
		self.thread.start()

	def isRunning(self):
		return self.running

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

		self.running = True

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
		self.q = None
		self.running = False
		print("Done")


	def replace(self, image_path):
		if self.q:
			self.q.put(image_path)


if __name__== "__main__" :
	pass
