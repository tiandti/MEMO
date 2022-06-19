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


def takeCameraPhoto():
	if isRaspberry():
		stream = BytesIO()
		camera = PiCamera()
		camera.resolution = (1680, 1050)
		camera.rotation = 90
		camera.capture(stream, format='jpeg')
		stream.seek(0)
		pil_image = Image.open(stream)
		photo = Photo(pil_image)
		camera.close()
		return photo
	else:
		image_path = getRandomFile("media/")
		image = Photo(image_path)
		return image
