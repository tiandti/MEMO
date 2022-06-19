"""User interface."""

from memo.artistic.photo import Photo
from PIL import ImageTk
import tkinter as tk
import threading
import queue


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
		print("UI: Closing")
		self.quitEvent.set()

	def _thread(self):
		"""Thread function that will handle the user interface."""
		self.root = tk.Tk()
		self.root.attributes('-fullscreen', self.fullscreen)
		self.root.bind("<Escape>", lambda x: self.close())
		height = self.root.winfo_screenheight()
		width = self.root.winfo_screenwidth()
		print(f"UI: Screen: {width} x {height} (in pixels)\n")

		# Create an image holder with a text
		self.message = tk.StringVar()
		self.media = tk.Label(image="", fg='white', font=("Arial", 48, "bold"), textvariable=self.message, compound='center', background="black")
		self.media.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
		self.message.set("")

		while not self.quitEvent.isSet():

			self.root.update_idletasks()
			self.root.update()

			if self.q.qsize():
				try:
					obj = self.q.get_nowait()

					if obj is None:
						print("UI: Clear image")
						self.media.configure(image="")
						self.media.image = ""
					elif isinstance(obj, Photo):
						print(f"UI: Change image: {obj}")
						if obj.image:
							image = ImageTk.PhotoImage(obj.image)
							self.media.configure(image=image)
							self.media.image = image
						else:
							pass
					elif isinstance(obj, str):
						print(f"UI: Change label: {obj}")
						self.message.set(obj)
					else:
						print(f"UI: Unknown instance: '{type(obj)}'")
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

	def replace(self, obj):
		"""Replace the object in the user interface."""
		if self.isRunning():
			self.q.put(obj)


if __name__ == "__main__":
	pass
