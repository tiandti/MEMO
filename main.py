#!/usr/bin/env python3.9

"""Memo application."""

from memo.camera import takeCameraPhoto
from memo.human import isHumanDetected
from memo.text import Text
from memo.connectors import Server
from memo.ui import UI
from memo.app import App
from memo.timer import Timer
import argparse
import time
import sys
import random
import os
import codecs
import pickle


image = None


#def getRandomFilter(image):
#	filters = ["hockney", "ghost", "crisscross"]
#	filterType = random.choice(filters)
#	print(f"Filter: {filterType}")
#
#	if filterType == "hockney":
#		background_photo = image.copy()
#		image.as_hockney(100, False)
#		background_photo.as_test()  # TODO: Change the internal name
#		background_photo.merge(image)
#		image = background_photo
#	elif filterType == "ghost":
#		# rightPhoto = takeCameraPhoto()
#		# leftPhoto = takeCameraPhoto()
#		rightPhoto = None
#		leftPhoto = None
#		image.as_ghost(left=leftPhoto, right=rightPhoto)
#	elif filterType == "crisscross":
#		image.as_test()  # TODO: Change the internal name
#	else:
#		image.as_test()  # TODO: Change the internal name
#
#	return image


def gui_text(con, txt):
	base64_str = codecs.encode(pickle.dumps(Text(txt)), "base64").decode()
	con.send(base64_str)


def gui_image(con, image):
	serialized_image = image.serialise()
	con.send(serialized_image)


def init(arg):
	"""Init state."""
	con = arg["connection"]
	# gui_image(con, None)
	gui_text(con, "Initializing...")
	time.sleep(5)
	return ("idle")


def idle(arg):
	"""Idle state."""
	con = arg["connection"]
	time.sleep(2)  # For cpu load
	gui_text(con, "")
	if isHumanDetected():
		# jobChoices = ["job_hockney", "job_ghost", "job_cc"]
		# job = random.choice(jobChoices)
		job = "job_hockney"
		return (job)
	else:
		return ("idle")


def job_hockney(arg):
	"""Do the job state."""
	con = arg["connection"]
	global image

	# We wanted to take the photo when the person is close
	gui_text(con, "Please stand at the line")
	time.sleep(4)
	image1 = takeCameraPhoto()

	# We want the person to look at the camere
	gui_text(con, "<-- Please look here")
	time.sleep(1.5)
	image2 = takeCameraPhoto()
	time.sleep(1)
	gui_text(con, "")

	image = random.choice([image1, image2])

	# Do the filter
	background_photo = image.copy()
	image.as_hockney(100, False)
	background_photo.as_test()  # TODO: Change the internal name
	background_photo.merge(image)
	image = background_photo

	# Save
	# TODO: Add mechanism to keep only the last 100? photos
	out_path = "/tmp/memo/"
	if not os.path.exists(out_path):
		os.mkdir(out_path)
	filename = time.strftime("%Y%m%d-%H%M%S") + ".jpeg"
	filepath = os.path.join(out_path + filename)
	image.save(filepath)

	return ("presentation")


def job_ghost(arg):
	"""Do the job state."""
	con = arg["connection"]
	global image

	gui_text(con, "Please take a photo")
	time.sleep(5)
	image = takeCameraPhoto()
	gui_text(con, "Photo is taken")

	gui_image(con, image)
	gui_text(con, "")

	time.sleep(2)

	return ("filter_photo")


def job_cc(arg):
	"""Do the job state."""
	con = arg["connection"]
	global image

	gui_text(con, "Please take a photo")
	time.sleep(5)
	image = takeCameraPhoto()
	gui_text(con, "Photo is taken")

	gui_image(con, image)
	gui_text(con, "")

	time.sleep(2)

	return ("filter_photo")


def presentation(arg):
	"""We show the person his/her memory state."""
	con = arg["connection"]
	global image

	time.sleep(2)
	gui_image(con, image)
	time.sleep(7)
	gui_text(con, "Congratulations!")
	time.sleep(1)
	gui_text(con, "You just got a new memory!")

	return ("overtime")


def overtime(arg):
	"""Person wants to stay longer state."""
	con = arg["connection"]
	time.sleep(2)  # For cpu load
	gui_text(con, "")

	if isHumanDetected():
		return ("overtime")
	else:
		time.sleep(1)
		# gui_image(con, image)  # TODO: Show black
		return ("idle")


def exit(arg):
	"""Exit state."""
	print("exit")
	time.sleep(1)
	return ("exit")


def arguments():
	"""Command line arguments."""
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument("-a", "--address",
	                    help="Selects the server ip address or hostname. Default is '127.0.0.1'",
	                    default="127.0.0.1")
	parser.add_argument("-p", "--port",
	                    help="When mode is socket, selects the server port. Default is '5555'",
	                    type=int, default=5555)
	parser.add_argument("-d", "--daemon",
	                    help="Run as a daemon.",
	                    action='store_true')
	parser.add_argument("-f", "--fullscreen",
	                    help="Run in fullscreen mode. Default is no.",
	                    action='store_true')
	args = parser.parse_args()

	ip = str(args.address)
	port = int(args.port)
	isDaemon = args.daemon
	isFullscreen = args.fullscreen
	return ip, port, isDaemon, isFullscreen


def receive_with_ack(con, timeout=10):
	"""Receive an image."""
	byteImage = ""
	flag = True
	t = Timer()
	t.start()
	while flag:
		msg = con.receive()
		if msg:
			msg = msg.decode("utf-8")
			if msg == "OK":
				flag = False
			else:
				byteImage += msg
		if t.elapsed() > timeout:
			byteImage = ""
			flag = False

	return byteImage


def main():
	"""Application starts here."""
	ip, port, isDaemon, isFullscreen = arguments()

	if isDaemon and ip != '127.0.0.1':
		print("[ERROR] Can not run daemon in a remote ip")
		sys.exit(1)

	if isDaemon:
		con = Server(port)
		ui = UI(isFullscreen)
		while ui.isRunning():
			serializedObj = receive_with_ack(con)
			if serializedObj:
				unpickledObj = pickle.loads(codecs.decode(serializedObj.encode(), "base64"))
				ui.replace(unpickledObj)
	else:
		sm = App(ip, port)
		sm.set_start("init")

		sm.add_state("init", init)
		sm.add_state("idle", idle)
		sm.add_state("job_hockney", job_hockney)
		sm.add_state("job_cc", job_cc)
		sm.add_state("job_ghost", job_ghost)
		sm.add_state("presentation", presentation)
		sm.add_state("overtime", overtime)
		sm.add_state("exit", exit, end_state=True)
		while True:
			sm.run()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
