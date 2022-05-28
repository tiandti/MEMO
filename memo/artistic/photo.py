"""Photo manipulation."""

import codecs
import copy
import pickle
import imageio
import random
import numpy as np
from PIL import Image
from skimage import exposure
from skimage.transform import swirl
from skimage import segmentation
from skimage import color
from skimage.future import graph

from .utils import weight_mean_color
from .utils import merge_mean_color


from PIL import ImageOps


class Photo:
	"""Class that represents a photograph."""

	def __init__(self, imagepath):
		"""Initialise a photograph."""
		self.image = imageio.imread(imagepath, pilmode='RGBA')

		# Convert to PIL image
		self.image = Image.fromarray(self.image)

	def __str__(self):
		"""Print photo attributes."""
		s = ""
		if not isinstance(self.image, Image.Image):
			s += "Not a PIL image"
		else:
			s += f" Mode: {self.image.mode}"
			s += f" Size: {self.image.size}"
			# s += f" Palette: {self.image.palette}"
			# s += f" Format: {self.image.format}"
			image = np.array(self.image)
			s += f" Shape: {image.shape}"
		return s

	def copy(self):
		"""Copy the photo."""
		return copy.deepcopy(self)

	def save(self, path):
		"""Save the photo."""
		self.image.convert('RGB').save(path)

	def serialise(self):
		base64_str = codecs.encode(pickle.dumps(self), "base64").decode()
		return base64_str

	def deserialise(base64_str):
		photoObj = pickle.loads(codecs.decode(base64_str.encode(), "base64"))
		return photoObj

	def merge(self, photo):
		"""Merge the photo."""
		w = self.image.size[0]
		h = self.image.size[1]
		image = Image.new("RGBA", (w, h))

		image.paste(self.image, (0, 0), self.image)
		image.paste(photo.image, (0, 0), photo.image)

		self.image = image

	def show(self):
		"""Show the photograph on screen."""
		self.image.show()

	# ---------------------------------------------------------------------
	# Filters
	def as_gray(self):
		"""Turn the photograph into grayscale."""
		image = ImageOps.grayscale(self.image)
		self.image = image.convert("RGBA")

	def swirl(self, rotation=0, strength=10, radius=120):
		"""Swirl a photograph."""
		# https://scikit-image.org/docs/stable/auto_examples/transform/plot_swirl.html#sphx-glr-auto-examples-transform-plot-swirl-py
		image = np.array(self.image)
		swirled_image = swirl(image=image, rotation=rotation, strength=strength, radius=radius)
		self.image = Image.fromarray((swirled_image * 255).astype(np.uint8))

	def as_hockney(self, numberOfBoxes=100, background=True):
		"""Hockney filter."""
		def crop(image, x, y, sizex, sizey):
			box = (x, y, x + sizex, y + sizey)
			cropped_image = image.crop(box)
			return cropped_image

		def paste(image, c, x, y):
			image.paste(c, (x, y))
			return image

		pil_image = self.image
		pil_image_out = None
		if background:
			pil_image_out = pil_image.copy()
		else:
			width = pil_image.size[0]
			height = pil_image.size[1]
			pil_image_out = Image.new("RGBA", (width, height))

		def getRandomBox(pil_image):
			margin = 200
			width = pil_image.size[0]
			height = pil_image.size[1]
			x = random.randrange(0 + margin, width - margin, 15)
			y = random.randrange(0 + margin, height - margin, 15)
			sizex = random.randrange(100, 300, 25)
			sizey = random.randrange(100, 300, 25)
			dx = random.randrange(-50, 50, 10)
			dy = random.randrange(-50, 50, 10)
			return(x, y, sizex, sizey, dx, dy)

		for i in range(numberOfBoxes):
			box = getRandomBox(pil_image)
			x = box[0]
			y = box[1]
			sizex = box[2]
			sizey = box[3]
			dx = x + box[4]
			dy = y + box[5]
			cropped = crop(pil_image, x, y, sizex, sizey)
			paste(pil_image_out, cropped, dx, dy)

		self.image = pil_image_out


	def as_lines(self, step=100, background=True):
		"""Test filter."""
		def crop(image, x, y, sizex, sizey):
			box = (x, y, x + sizex, y + sizey)
			cropped_image = image.crop(box)
			return cropped_image

		def paste(image, c, x, y):
			image.paste(c, (x, y))
			return image

		# pil_image = Image.fromarray(self.image)
		pil_image = self.image
		pil_image_out = None
		height = pil_image.size[1]
		if background:
			pil_image_out = pil_image.copy()
		else:
			width = pil_image.size[0]
			pil_image_out = Image.new("RGBA", (width, height))

		def getRandomLine(pil_image):
			width = pil_image.size[0]
			height = pil_image.size[1]
			x = 0  # random.randrange(0, width, 15)
			y = 0
			sizex = width
			sizey = random.randrange(10, 30, 10)
			dx = 0
			dy = random.randrange(-10, 10, 10)
			return(x, y, sizex, sizey, dx, dy)

		for i in range(0, height, step):
			box = getRandomLine(pil_image)
			x = box[0]
			y = box[1] + i
			sizex = box[2]
			sizey = box[3]
			dx = x + box[4]
			dy = y + box[5]
			print(f"x: {x}, y: {y} | sx: {sizex}, sy: {sizey} | dx: {dx}, dy: {dy}")
			cropped = crop(pil_image, x, y, sizex, sizey)
			paste(pil_image_out, cropped, dx, dy)

		self.image = pil_image_out

	def as_test(self, background=True):
		"""Test filter from Tania."""
		def crop(image, x, y, sizex, sizey):
			box = (x, y, x + sizex, y + sizey)
			cropped_image = image.crop(box)
			return cropped_image

		def paste(image, c, x, y):
			image.paste(c, (x, y))
			return image

		# pil_image = Image.fromarray(self.image)
		pil_image = self.image
		pil_image_out = None
		height = pil_image.size[1]
		if background:
			pil_image_out = pil_image.copy()
		else:
			width = pil_image.size[0]
			pil_image_out = Image.new("RGBA", (width, height))

		def getRandomLine(pil_image):
			width = pil_image.size[0]
			height = pil_image.size[1]
			x = 0  # random.randrange(0, width, 15)
			y = 0
			sizex = width
			sizey = random.randrange(10, 100, 10)
			dx = random.randrange(-50, 50, 10)
			dy = 0
			return(x, y, sizex, sizey, dx, dy)

		for i in range(height):
			box = getRandomLine(pil_image)
			x = box[0]
			y = box[1] + i
			sizex = box[2]
			sizey = box[3]
			dx = x + box[4]
			dy = y + box[5]
			# print(f"x: {x}, y: {y} | sx: {sizex}, sy: {sizey} | dx: {dx}, dy: {dy}")
			cropped = crop(pil_image, x, y, sizex, sizey)
			paste(pil_image_out, cropped, dx, dy)

		self.image = pil_image_out

	def as_rag(self):
		"""
		Construct a Region Adjacency Graph (RAG) and progressively maerge regions that are similar in color.

		Merging two adjacent regions produces a new region with all the pixels from the merged regions.
		Regions are merged until no highly similar region pairs remain.
		"""
		# https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_rag_merge.html#sphx-glr-auto-examples-segmentation-plot-rag-merge-py
		self.image = self.image.convert("RGB")
		image = np.array(self.image)

		labels = segmentation.slic(image, compactness=30, n_segments=400, start_label=1)
		g = graph.rag_mean_color(image, labels)

		labels2 = graph.merge_hierarchical(
			labels, g, thresh=35, rag_copy=False,
			in_place_merge=True,
			merge_func=merge_mean_color,
			weight_func=weight_mean_color)

		out = color.label2rgb(labels2, image, kind='avg', bg_label=0)
		rag_image = segmentation.mark_boundaries(out, labels2, (0, 0, 0))
		self.image = Image.fromarray((rag_image * 255).astype(np.uint8))
		self.image = self.image.convert("RGBA")

	# ---------------------------------------------------------------------
	# Tests
	def filterFunc(self):
		"""TODO."""
		pil_image = Image.fromarray(self.image)
		self.image = np.array(pil_image)
		raise NotImplementedError

	def test(self):
		"""TODO."""
		pil_image = Image.fromarray(self.image)
		self.image = np.array(pil_image)
		raise NotImplementedError

	# ---------------------------------------------------------------------
	# TODO
	# https://pythontic.com/image-processing/pillow/sharpen-filter
