#!/usr/bin/env python3.9

"""Memo application."""

from memo.connectors import Server
from memo.ui import UI
from memo.app import App

import argparse
import time
import sys


dt = 0.5


def init(arg):
	"""Init state."""
	print("Init")
	time.sleep(dt)
	return ("on")

def on(arg):
	"""On state."""
	con = arg["connection"]
	image = "./media/hockney.png"
	print(f"on - {image}")
	con.send(image.encode())
	time.sleep(dt)
	return ("off")

def off(arg):
	"""Off state."""
	con = arg["connection"]
	image = "./media/hockney2.jpg"
	print(f"off - {image}")
	con.send(image.encode())
	time.sleep(dt)
	return ("on")

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
				ui.replace(msg)

				# Acknowledge to the client
				reply = "Done"
				con.send(reply.encode("utf-8"))
	else:
		sm = App(ip, port)
		sm.set_start("init")

		sm.add_state("init", init)
		sm.add_state("on", on)
		sm.add_state("off", off)
		sm.add_state("exit", exit, end_state=True)
		while True:
			sm.run()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
