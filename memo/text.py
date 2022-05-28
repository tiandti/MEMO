"""Text."""


class Text:
	"""Class that represents a text."""

	def __init__(self, txt):
		"""Initialise text."""
		self.txt = txt

	def __str__(self):
		"""Print text."""
		return self.txt
