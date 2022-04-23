#!/usr/bin/env python3.9

from memo.connectors import Client
from memo.connectors import Server
from memo.ui import UI
from memo.app import App

import threading
import argparse
import time
import sys


def init(arg):
	con = arg["connection"]
	print("Init")
	time.sleep(1)
	return ("on")

def on(arg):
	# con = Client()
	con = arg["connection"]
	image = "./media/hockney.png"
	print(f"on - {image}")
	con.send(image.encode())
	time.sleep(1)
	return ("off")

def off(arg):
	con = arg["connection"]
	image = "./media/hockney2.jpg"
	print(f"off - {image}")
	con.send(image.encode())
	time.sleep(1)
	return ("on")

def exit(arg):
	print("exit")
	time.sleep(1)
	return ("exit")

def main():
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
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

	if isDaemon and ip != '127.0.0.1':
		print("[ERROR] Can not run daemon in a remote ip")
		sys.exit(1)

	if isDaemon:
		con = Server(port)
		ui = UI()
		while ui.isRunning():

			msg = con.receive()
			if msg:
				msg = msg.decode("utf-8")
				print(f"[DEBUG]: Msg = '{msg}'")

				# Change the photo to the ui
				ui.replace(msg)

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

		exit(0)
	print("main end")

if __name__== "__main__" :
	try:
		main()
	except KeyboardInterrupt:
		print('\nHello user you have pressed ctrl-c button.')
		pass
