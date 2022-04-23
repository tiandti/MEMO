#!/usr/bin/env python3.9

from memo.connectors import Client
from memo.connectors import Server
from memo.ui import UI

import threading
import argparse
import time


def socketTask(ip, port, args, ui):

	if not args.daemon:
		con = Client(ip, port)
		print("1")
		con.send(args.bar.encode())
		print("2")
		msg = con.receive()
		print(f"msg: {msg.decode()}")
	else:
		con = Server(ip, port)
		while ui.isRunning():

			print("BUG: TODO fix")

			msg = con.receive()
			msg = msg.decode("utf-8")
			print(f"Msg: '{msg}'")

			ui.replace(msg)
			reply = "Done"
			con.send(reply.encode("utf-8"))
	print("3")

def main():
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument('--bar',
			    help = "Media path.",
			    default = "")
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

	if not isDaemon:
		#socketTask(args, None)
		#socketThread = threading.Thread(target=socketTask, args=(ip, port, args, None,))
		#socketThread.start()
		con = Client(ip, port)
		con.send(args.bar.encode())
		msg = con.receive()
		print(f"msg: {msg.decode()}")

		exit(0)
	else:
		ui = UI()
		print("Socket before thread")
		socketThread = threading.Thread(target=socketTask, args=(ip, port, args, ui))
		print("Socket before start")
		socketThread.start()
		print("Socket before join")
		socketThread.join()
		print("Socket end")
	print("main end")

if __name__== "__main__" :
	try:
		main()
	except KeyboardInterrupt:
		print('\nHello user you have pressed ctrl-c button.')
		pass
