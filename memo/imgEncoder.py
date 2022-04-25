"""Image encoding/decoding."""

from PIL import Image
import skimage
import base64
import skimage.io
import io


def encodeImg(image) -> str:
	"""Convert image to bytes."""
	with io.BytesIO() as output_bytes:
		PIL_image = Image.fromarray(skimage.img_as_ubyte(image))
		PIL_image.save(output_bytes, 'JPEG')  # Note JPG is not a vaild type here
		bytes_data = output_bytes.getvalue()

	# encode bytes to base64 string
	base64_str = str(base64.b64encode(bytes_data), 'utf-8')
	return base64_str


def decodeImg(base64_string):
	"""Convert bytes to image."""
	if isinstance(base64_string, bytes):
		base64_string = base64_string.decode("utf-8")

	imgdata = base64.b64decode(base64_string)
	img = skimage.io.imread(imgdata, plugin='imageio')
	return img


if __name__ == "__main__":
	import imageio

	image_in = imageio.imread("media/hockney.png", pilmode='RGB')
	data = encodeImg(image_in)
	image_out = decodeImg(data)
	imageio.imwrite("output/out.jpg", image_out)
