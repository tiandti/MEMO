#!/usr/bin/env python3

from io import BytesIO
from PIL import Image
from memo.artistic.photo import Photo
from .utils import isRaspberry
from .utils import getRandomFile


if isRaspberry():
	# sudo apt-get install libatlas-base-dev
	# libcamera-jpeg --width 1050 --height 1680 -t 1 -o ~/Desktop/test.jpg
	from picamera import PiCamera


class Camera():
	def __init__(self):
		if isRaspberry():
			self.camera = PiCamera()
			self.camera.resolution = (1050, 1680)
			self.camera.rotation = 90
		else:
			self.camera = None

	def __del__(self):
		if self.camera is not None:
			self.camera.close()

	def takePhoto(self):
		if self.camera is not None:
			stream = BytesIO()
			self.camera.capture(stream, format='jpeg')
			stream.seek(0)
			pil_image = Image.open(stream)
			photo = Photo(pil_image)
			return photo
		else:
			image_path = getRandomFile("media/")
			photo = Photo(image_path)
			return photo
