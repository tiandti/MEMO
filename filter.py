#!/usr/bin/env python3.9

"""Filter tool."""

from memo.artistic.photo import Photo
import argparse


def arguments():
	"""Command line arguments."""
	parser = argparse.ArgumentParser(description='Memo kiosk client/server')
	parser.add_argument("-i", "--image",
	                    help="Selects an image.",
	                    required=True)
	parser.add_argument("-f", "--filter",
	                    help="Selects the server ip address or hostname. Default is '127.0.0.1'",
	                    default="normal")

	args = parser.parse_args()
	filterType = str(args.filter)
	image = str(args.image)
	return image, filterType

def main():
	"""Application starts here."""
	image_path, filterType = arguments()
	print(f"Filter: {filterType}")

	photo = Photo(image_path)

	if filterType == "hockney":
		background_photo = photo.copy()
		photo.as_hockney(100, False)
		background_photo.as_test()
		background_photo.merge(photo)
		photo = background_photo
	elif filterType == "gray":
		photo.as_gray()
	elif filterType == "swirl":
		photo.swirl(5, 100, 1)
	elif filterType == "rag":
		photo.as_rag()
	else:
		photo.as_test()

	photo.show()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('\nExiting.')
