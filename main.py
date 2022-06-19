#!/usr/bin/env python3.9

"""Memo application."""

from memo.camera import Camera
from memo.human import isHumanDetected
from memo.ui import UI
import argparse
import time
import random
import os


class MemoMachine:
	"""The memo FSM."""

	def __init__(self, changeGuiFuncCB):
		"""Create the object."""
		self.stateFunc = self._initState
		self.changeGuiFunc = changeGuiFuncCB
		self.photo = None
		self.camera = Camera()

	def handle(self):
		"""Handle the finite state machine."""
		if self.stateFunc is not None:
			name = self.stateFunc.__name__
			print("\033[0;31m-------------------------------------------------------")
			print(f"\033[0;31m[FSM]: {name}\033[0m")
			print("")
			self.stateFunc()

	def _initState(self):
		"""Init state."""
		self.changeGuiFunc(None)
		self.changeGuiFunc("Initializing...")
		time.sleep(5)
		self.stateFunc = self._idleState

	def _idleState(self):
		"""Idle state."""
		time.sleep(2)  # For cpu load
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
		time.sleep(4)
		photoFar = self.camera.takePhoto()

		# We want the person to look at the camere
		self.changeGuiFunc("<-- Please look here")
		time.sleep(1.5)
		photoClose = self.camera.takePhoto()
		time.sleep(1)
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
		time.sleep(1)
		rightPhoto = self.camera.takePhoto()

		# We wanted one photo when the person is closer
		self.changeGuiFunc("Please stand at the line")
		time.sleep(3)
		leftPhoto = self.camera.takePhoto()
		time.sleep(1)
		self.changeGuiFunc("")

		# We want the person to look at the camere
		self.changeGuiFunc("<-- Please look here")
		time.sleep(1.5)
		self.photo = self.camera.takePhoto()
		time.sleep(1)
		self.changeGuiFunc("")

		# Do the filter
		self.photo.as_ghost(left=leftPhoto, right=rightPhoto)

		self.stateFunc = self._presentationState

	def _ccFilterState(self):
		"""Do the CrissCross filter state."""
		# We wanted one photo when the person is atthe line
		time.sleep(1)
		self.changeGuiFunc("Please stand at the line")
		time.sleep(6)
		self.photo = self.camera.takePhoto()
		time.sleep(1)
		self.changeGuiFunc("")

		# Do the filter
		self.photo.as_cc()

		self.stateFunc = self._presentationState

	def _presentationState(self):
		"""We show the person his/her memory state."""
		time.sleep(2)
		self.changeGuiFunc(self.photo)
		time.sleep(7)
		self.changeGuiFunc("Congratulations!")
		time.sleep(1)
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
		time.sleep(2)  # For cpu load
		self.changeGuiFunc("")

		if isHumanDetected():
			self.stateFunc = self._overtimeState
		else:
			time.sleep(1)
			self.changeGuiFunc(None)
			self.stateFunc = self._idleState


def arguments():
	"""Command line arguments."""
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument("-f", "--fullscreen",
	                    help="Run in fullscreen mode. Default is no.",
	                    action='store_true')
	args = parser.parse_args()

	isFullscreen = args.fullscreen
	return isFullscreen


def main():
	"""Application starts here."""
	isFullscreen = arguments()
	ui = UI(isFullscreen)
	memo = MemoMachine(ui.replace)
	while ui.isRunning():
		memo.handle()


if __name__ == "__main__":
	while True:
		try:
			main()
		except Exception:
			print('\nRestarting.')
