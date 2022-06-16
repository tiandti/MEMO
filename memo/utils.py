"""General purpose Utilities."""

import os
import platform
import random


def getRandomFile(directory):
	files = []
	for dirpath, _, filenames in os.walk(directory):
		for f in filenames:
			files.append(os.path.join(dirpath, f))
	image_path = random.choice(files)
	return image_path



def isRaspberry():
	"""Get if the target is a Raspberry."""
	rv = True
	if platform.machine() == "x86_64":
		rv = False
	return rv
