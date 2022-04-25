"""User interface."""

import tkinter as tk
# from tkvideo import tkvideo
from PIL import Image, ImageTk
import threading
import queue
import imageio

# from memo.fst.utils import get_img

class UI:
	"""User interface."""

	def __init__(self, fullscreen=False):
		"""Initialise the user interface."""
		self.event = threading.Event()
		self.image_path = ""
		self.fullscreen = fullscreen

		self.quitEvent = threading.Event()

		self.q = queue.Queue()

		self.thread = threading.Thread(target=self._thread)
		self.thread.start()

	def isRunning(self):
		"""Check if the user interface is still running."""
		return not self.quitEvent.isSet()

	def close(self):
		"""Close the user interface."""
		print("[UI]: Closing")
		self.quitEvent.set()

	def _thread(self):
		"""Thread function that will handle the user interface."""
		self.root = tk.Tk()
		self.root.attributes('-fullscreen', self.fullscreen)
		self.root.bind("<Escape>", lambda x: self.close())
		height = self.root.winfo_screenheight()
		width = self.root.winfo_screenwidth()
		print(f"[UI]: Screen: {width} x {height} (in pixels)\n")

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
							# 1 - Pillow
							# raw_image = Image.open(image_path)

							# 2 - FST (ImageIO)
							# raw_image = Image.fromarray(get_img(image_path))

							# 3 - ImageIO
							raw_image = Image.fromarray(imageio.imread(image_path, pilmode='RGB'))

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

	def replace(self, image_path):
		"""Replace the image in the user interface."""
		if self.isRunning():
			self.q.put(image_path)


if __name__ == "__main__":
	pass
