#!/usr/bin/env python3.9

"""Memo application."""

from memo.artistic.photo import Photo
from memo.imgEncoder import encodeImg
from memo.connectors import Server
from memo.fst.fst import fst
from memo.ui import UI
from memo.app import App
from memo.timer import Timer
import argparse
import time
import sys
import imageio
import random
import os
import codecs
import pickle


image = None


def getRandomFile(directory):
	files = []
	for dirpath, _, filenames in os.walk(directory):
		for f in filenames:
			files.append(os.path.join(dirpath, f))
	image_path = random.choice(files)
	return image_path


def init(arg):
	"""Init state."""
	time.sleep(0.01)
	return ("idle")


def idle(arg):
	"""Idle state."""
	time.sleep(2)
	return ("take_photo")


def take_photo(arg):
	"""Take photo state."""
	con = arg["connection"]
	global image

	image_path = getRandomFile("media/faces")
	print(f"Taking photo of person - {image_path}... ")

	image = Photo(image_path)
	serialized_image = image.serialise()

	con.send(serialized_image)
	time.sleep(2)

	return ("filter_photo")


def filter_photo(arg):
	"""Filter photo state."""
	con = arg["connection"]
	global image

	background_photo = image.copy()
	image.as_hockney(100, False)
	background_photo.as_test()
	background_photo.merge(image)
	image = background_photo
	serialized_image = image.serialise()

	con.send(serialized_image)
	time.sleep(5)

	return ("acknoledge")


def filter_photo_old(arg):
	"""Filter photo state."""
	con = arg["connection"]

	image_in = imageio.imread(image, pilmode='RGB')
	fstModel = getRandomFile("models/")
	print(f"Calculating filter '{fstModel}'... Please wait...")
	image_out = fst(image_in, fstModel)
	print("Filter ready")

	data = encodeImg(image_out)
	con.send(data.encode())
	time.sleep(0.01)
	con.send("OK".encode())
	time.sleep(0.01)

	time.sleep(10)

	return ("acknoledge")


def acknoledge(arg):
	"""Acknoledge state."""
	print("Please press a button to reset...")
	input()
	print("")
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
		sm.add_state("take_photo", take_photo)
		sm.add_state("filter_photo", filter_photo)
		sm.add_state("acknoledge", acknoledge)
		sm.add_state("exit", exit, end_state=True)
		while True:
			sm.run()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
