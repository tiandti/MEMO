#!/usr/bin/env python3.9

"""Filter tool."""

from .utils import isRaspberry


if isRaspberry():
	import RPi.GPIO as GPIO


# pip install RPi.GPIO
def isHumanDetected():
	if isRaspberry():
		pin = 14
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN)
		if GPIO.input(pin) != 0:
			return False
		else:
			return True
	else:
		input("Virtual sensor: Press a button")
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
