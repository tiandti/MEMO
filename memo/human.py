#!/usr/bin/env python3.9

"""Filter tool."""

import RPi.GPIO as GPIO

# pip install RPi.GPIO
def isHumanDetected():
	pin = 14
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.IN)
	if GPIO.input(pin) != 0:
		return False
	else:
		return True

def main():
	"""Application starts here."""
	isDetected = isHumanDetected()
	

	print(f"Human: {isDetected}")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
