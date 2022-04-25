#!/usr/bin/env python3.9

"""Memo application."""

from memo.imgEncoder import encodeImg
from memo.connectors import Server
from memo.fst.fst import fst
from memo.ui import UI
from memo.app import App
import argparse
import time
import sys
import imageio


image = "media/hockney.png"

def init(arg):
	"""Init state."""
	print("Init")
	return ("take_photo")


def take_photo(arg):
	"""Take photo state."""
	con = arg["connection"]
	print("Taking photo of person... ")

	image_out = imageio.imread(image, pilmode='RGB')
	data = encodeImg(image_out)
	con.send("IMG".encode())
	time.sleep(0.01)
	con.send(data.encode())
	time.sleep(0.01)
	con.send("OK".encode())
	time.sleep(0.01)

	return ("filter_photo")


def filter_photo(arg):
	"""Filter photo state."""
	con = arg["connection"]
	print("Calculating filter")

	image_in = imageio.imread(image, pilmode='RGB')
	image_out = fst(image_in, "models/scream.ckpt")

	data = encodeImg(image_out)
	con.send("IMG".encode())
	time.sleep(0.01)
	con.send(data.encode())
	time.sleep(0.01)
	con.send("OK".encode())
	time.sleep(0.01)

	return ("acknoledge")


def acknoledge(arg):
	"""Acknoledge state."""
	print("Please press a button to reset...")
	test = input()
	return ("init")


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


def receiveImage(con, timeout=10):
	"""Receive an image."""
	byteImage = ""
	flag = True
	while flag:
		msg = con.receive()
		if msg:
			msg = msg.decode("utf-8")
			if msg == "OK":
				flag = False
			else:
				byteImage += msg
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

			msg = con.receive()
			if msg:
				# Change the photo to the ui
				msg = msg.decode("utf-8")

				if msg == "IMG":
					byteImage = receiveImage(con)
					byteImage
					ui.replace(byteImage)

				# Acknowledge to the client
				reply = "Done"
				con.send(reply.encode("utf-8"))
	else:
		sm = App(ip, port)
		sm.set_start("init")

		sm.add_state("init", init)
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
