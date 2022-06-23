#!/usr/bin/env python3.9

"""Memo application."""

from tkinter import Tk
from tkinter import Label
from tkinter import StringVar
from tkinter import BOTH
from tkinter import LEFT
from PIL import ImageTk
from memo.artistic.photo import Photo
from memo.camera import Camera
from memo.human import isHumanDetected
import argparse
import time
import random
import os


class UI():
	"""The main UI."""

	def __init__(self, fullscreen=False):
		"""Create the object."""
		self.stateFunc = self._initState
		self.photo = None
		self.camera = Camera()

		"""Create the UI."""
		self.root = Tk()
		self.root.title('Memo')
		self.root.geometry('400x300')
		self.root.config(bg='#5f734c')
		self.root.attributes('-fullscreen', fullscreen)
		self.root.bind("<Escape>", lambda x: self._close())
		height = self.root.winfo_screenheight()
		width = self.root.winfo_screenwidth()
		print(f"UI: Screen: {width} x {height} (in pixels)")

		# Create an image holder with a text
		self.message = StringVar()
		self.media = Label(image="", fg='white', font=("Arial", 48, "bold"), textvariable=self.message, compound='center', background="black")
		self.media.pack(fill=BOTH, side=LEFT, expand=True)
		self.message.set("")

		self.isRunning = True
		self.root.update()

	def run(self):
		"""Run."""
		while self.isRunning:
			if self.stateFunc is not None:
				name = self.stateFunc.__name__
				print("\033[0;31m-------------------------------------------------------")
				print(f"\033[0;31m[FSM]: {name}\033[0m")
				print("")
				self.stateFunc()

			self.root.update()

		# self.root.mainloop()

	def _close(self):
		"""Close the UI."""
		self.changeGuiFunc("Closing...")
		print("UI: closing")
		self.isRunning = False
		# self.root.destroy()

	def _sleep(self, s):
		print(f"UI: Sleep: {s} sec")
		self.root.after(int(1000 * s), None)

	def changeGuiFunc(self, obj):
		"""Change an element in the UI."""
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
		self.root.update()

	def _initState(self):
		"""Init state."""
		self.changeGuiFunc(None)
		self.changeGuiFunc("Initializing...")
		self._sleep(5)
		self.stateFunc = self._idleState

	def _idleState(self):
		"""Idle state."""
		self._sleep(0.5)  # For cpu load
		self.photo = None
		self.changeGuiFunc(None)
		self.changeGuiFunc("")
		if isHumanDetected():
			filterStateChoices = [self._hockneyFilterState, self._ghostFilterState, self._ccFilterState]
			filterState = random.choice(filterStateChoices)
			self.stateFunc = filterState
		else:
			self.stateFunc = self._idleState

	def _hockneyFilterState(self):
		"""Do the Hockney filter state."""
		# We wanted to take the photo when the person is close
		self.changeGuiFunc("Please stand at the line")
		self._sleep(4)
		photoFar = self.camera.takePhoto()

		# We want the person to look at the camere
		self.changeGuiFunc("<-- Please look here")
		self._sleep(1.5)
		photoClose = self.camera.takePhoto()
		self._sleep(1)
		self.changeGuiFunc("")

		self.photo = random.choice([photoFar, photoClose])

		# Do the filter
		background_photo = self.photo.copy()
		self.photo.as_hockney(100, False)
		background_photo.as_cc()
		background_photo.merge(self.photo)
		self.photo = background_photo

		self.stateFunc = self._presentationState

	def _ghostFilterState(self):
		"""Do the Ghost filter state."""
		# We wanted one photo when the person is away
		rightPhoto = self.camera.takePhoto()

		# We wanted one photo when the person is closer
		self.changeGuiFunc("Please stand at the line")
		self._sleep(3)
		leftPhoto = self.camera.takePhoto()
		self._sleep(1)
		self.changeGuiFunc("")

		# We want the person to look at the camere
		self.changeGuiFunc("<-- Please look here")
		self._sleep(1.5)
		self.photo = self.camera.takePhoto()
		self._sleep(1)
		self.changeGuiFunc("")

		# Do the filter. Randomly select 2 photos
		[imageA, imageB] = random.sample([leftPhoto, rightPhoto, self.photo], 2)
		self.photo.as_ghost(left=imageA, right=imageB)

		self.stateFunc = self._presentationState

	def _ccFilterState(self):
		"""Do the CrissCross filter state."""
                # We wanted one photo when the person is away
		rightPhoto = self.camera.takePhoto()

		# We wanted one photo when the person is closer
		self.changeGuiFunc("Please stand at the line")
		self._sleep(3)
		leftPhoto = self.camera.takePhoto()
		self._sleep(1)
		self.changeGuiFunc("")

		# We want the person to look at the camere
		self.changeGuiFunc("<-- Please look here")
		self._sleep(1.5)
		self.photo = self.camera.takePhoto()
		self._sleep(1)
		self.changeGuiFunc("")

		# Do the filter. Randomly select 2 photos
		self.photo = random.choice([self.photo, leftPhoto, rightPhoto])
		self.photo.as_cc()

		self.stateFunc = self._presentationState

	def _presentationState(self):
		"""We show the person his/her memory state."""
		self._sleep(2)
		self.changeGuiFunc(self.photo)
		self._sleep(7)
		self.changeGuiFunc("Congratulations!")
		self._sleep(1)
		self.changeGuiFunc("You just got a new memory!")

		# Save
		# TODO: Add mechanism to keep only the last 100? photos
		out_path = "/tmp/memo/"
		if not os.path.exists(out_path):
			os.mkdir(out_path)
		filename = time.strftime("%Y%m%d-%H%M%S") + ".jpeg"
		filepath = os.path.join(out_path + filename)
		self.photo.save(filepath)

		self.stateFunc = self._overtimeState

	def _overtimeState(self):
		"""Person wants to stay longer state."""
		self._sleep(0.5)  # For cpu load
		self.changeGuiFunc("")

		if isHumanDetected():
			self.stateFunc = self._overtimeState
		else:
			self._sleep(1)
			self.changeGuiFunc(None)
			self.stateFunc = self._idleState


def arguments():
	"""Command line arguments."""
	parser = argparse.ArgumentParser(description='Memo')
	parser.add_argument("-f", "--fullscreen",
	                    help="Run in fullscreen mode. Default is no.",
	                    action='store_true')
	args = parser.parse_args()

	isFullscreen = args.fullscreen
	return isFullscreen


if __name__ == "__main__":
	isFullscreen = arguments()
	app = UI(isFullscreen)
	app.run()
