#!/usr/bin/env python3
"""Pure python implementation of the gimp gtp tool preset format.
"""
from __future__ import annotations

import argparse
from io import BytesIO

import brackettree


class ParenFileValue:
	"""A parentheses-based file format.

	(possibly "scheme" language?)
	"""

	def __init__(self, name=None, value="", children=None):
		self.name = name
		try:
			float(value)
			self.value = value
		except ValueError:
			self.value = '"' + value + '"'
		if value in ("yes", "no"):
			self.value = value
		self.children = children

	def _addValue(self, bufArray):
		if self.name is None:  # first value is the name
			self.name = bufArray
		if bufArray:
			bufArray = "".join(bufArray)
			if bufArray in ("yes", "no"):  # boolean
				self.value.append(bufArray == "yes")
			elif bufArray[0].isdigit():
				self.value.append(float(bufArray))
			elif bufArray[0] == '"':
				self.value.append(bufArray[1:-1])
			else:
				raise Exception('What kind of value is "' + bufArray + '"?')

	def __repr__(self):
		"""Get a textual representation of this object."""
		ret = []
		ret.append("(" + str(self.name))
		ret.append(" " + self.value)
		if self.children is None:
			ret.append(")")
		ret.append("\n")
		if self.children is not None:
			for index, child in enumerate(self.children):
				ret.append("    (" + str(child.name))
				ret.append(" " + child.value + ")")
				if index == len(self.children) - 1:
					ret.append(")")
				ret.append("\n")
		return "".join(ret)


def parenFileDecode(data):
	"""Decode a parentheses-based file format.

	(possibly "scheme" language?)
	"""
	nodes = brackettree.Node(data)
	values = walkTree(nodes.items)
	return values


def walkTree(items):
	"""Walk the tree."""
	values = []
	for item in items:
		if isinstance(item, brackettree.RoundNode):
			if len(item.items) == 1:
				values.append(
					ParenFileValue(
						item.items[0].split(" ")[0].strip(), item.items[0].split(" ")[1].strip()
					)
				)
			if len(item.items) == 2:
				values.append(ParenFileValue(item.items[0].strip(), item.items[1].items[0].strip()))
			elif len(item.items) > 2:
				values.append(
					ParenFileValue(
						item.items[0].strip(),
						item.items[1].items[0].strip(),
						walkTree(item.items[2:]),
					)
				)
	return values


def parenFileEncode(values):
	"""Encode a values tree to a buffer."""
	ret = []
	ret.append("# GIMP tool preset file\n\n")
	ret.append("")
	for val in values:
		if val.name is not None:
			ret.append(str(val))
	ret.append("")
	ret.append("\n# end of GIMP tool preset file\n")
	ret.append("")
	return "".join(ret)


class GimpGtpToolPreset:
	"""Pure python implementation of the gimp gtp tool preset format."""

	def __init__(self, fileName=None):
		self.fileName = None
		self.values = []
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: BytesIO | str):
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		if hasattr(fileName, "read"):
			self.fileName = fileName.name
			f = fileName
		else:
			self.fileName = fileName
			f = open(fileName)
		data = f.read()
		self.decode(data)
		f.close()

	def decode(self, data, index=0):
		"""Decode a byte buffer.

		:param data: data buffer to decode
		"""
		self.values = parenFileDecode(data)
		return index

	def encode(self):
		"""Encode to a byte array."""
		return parenFileEncode(self.values).encode("utf-8")

	def save(self, tofileName=None, toExtension=None):
		"""Save this gimp tool preset to a file."""
		if toExtension is None:
			if tofileName is not None:
				toExtension = tofileName.rsplit(".", 1)
				if len(toExtension) > 1:
					toExtension = toExtension[-1]
				else:
					toExtension = None
		if hasattr(tofileName, "write"):
			file = tofileName
		else:
			file = open(tofileName, "wb")
		file.write(self.encode())
		file.close()

	def __repr__(self, indent=""):
		"""Get a textual representation of this object."""
		ret = []
		for value in self.values:
			ret.append(value.__repr__(indent + "\t"))
		return "\n".join(ret)


if __name__ == "__main__":
	"""CLI Entry Point."""
	parser = argparse.ArgumentParser("gimpGtpToolPreset.py")
	parser.add_argument("xcfdocument", action="store", help="xcf file to act on")
	parser.add_argument("--dump", action="store_true", help="dump info about this file")
	args = parser.parse_args()

	gimpGtpToolPreset = GimpGtpToolPreset(args.xcfdocument)

	if args.dump:
		print(gimpGtpToolPreset)
