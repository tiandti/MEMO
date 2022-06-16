#!/usr/bin/env python3

from io import BytesIO
from picamera import PiCamera
from PIL import Image
from memo.artistic.photo import Photo

#sudo apt-get install libatlas-base-dev

# libcamera-jpeg --width 1050 --height 1680 -t 1 -o ~/Desktop/test.jpg
def takeCameraPhoto():
	stream = BytesIO()
	camera = PiCamera()
	camera.resolution = (1680, 1050)
	camera.rotation = 90
	camera.capture(stream, format='jpeg')
	stream.seek(0)
	pil_image = Image.open(stream)
	return Photo(pil_image)
