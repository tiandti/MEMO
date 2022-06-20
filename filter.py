#!/usr/bin/env python3.9

"""Filter tool."""

from memo.artistic.photo import Photo
from memo.camera import Camera
import argparse
import os
import time


def arguments():
	"""Command line arguments."""
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument("-i", "--image",
	                    help="Selects an image.",
	                    required=False)
	parser.add_argument("-f", "--filter",
	                    help="Selects the filter to apply.",
	                    default="normal")
	parser.add_argument("-o", "--output_dir",
	                    help="Selects the output directory.",
	                    default="/tmp/memo/")

	args = parser.parse_args()
	filterType = str(args.filter)
	image = str(args.image)
	output_dir = str(args.output_dir)
	return image, filterType, output_dir


def main():
	"""Application starts here."""
	image_path, filterType, out_path = arguments()
	camera = Camera()
	print(f"Filter: {filterType}")

	print(f"Image: {image_path}")

	photo = None
	if image_path == "None":
		photo = camera.takePhoto()
	else:
		photo = Photo(image_path)
	print(type(photo))
	print(photo)
	# photo.save("original.jpg")

	if filterType == "hockney":
		background_photo = photo.copy()
		photo.as_hockney(100, False)
		background_photo.as_cc()
		background_photo.merge(photo)
		photo = background_photo
	elif filterType == "ghost":
		print("Will take a far photo")
		time.sleep(1.5)
		rightPhoto = camera.takePhoto()
		print("Will take the near photo")
		time.sleep(1.5)
		leftPhoto = camera.takePhoto()
		print("Done")
		photo.as_ghost(left=leftPhoto, right=rightPhoto)
	elif filterType == "gray":
		photo.as_gray()
	elif filterType == "swirl":
		photo.swirl(5, 100, 1)
	elif filterType == "rag":
		photo.as_rag()
	else:
		photo.as_cc()

	# Test serialisation
	serialized_image = photo.serialise()
	photo = Photo.deserialise(serialized_image)

	if not os.path.exists(out_path):
		os.mkdir(out_path)
	filename = filterType + "_" + time.strftime("%Y%m%d-%H%M%S") + ".jpeg"

	photo.save(os.path.join(out_path + filename))
	photo.show()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
