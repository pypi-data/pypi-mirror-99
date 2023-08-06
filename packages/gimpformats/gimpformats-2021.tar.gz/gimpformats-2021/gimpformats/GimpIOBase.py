#!/usr/bin/env python3
"""A specialized binary file base for Gimp files
"""
from __future__ import annotations

import struct

from binaryiotools import IO

from .GimpParasites import GimpParasite
from .GimpVectors import GimpVector


class GimpIOBase:
	"""A specialized binary file base for Gimp files"""

	COLOR_MODES = ["RGB", "Grayscale", "Indexed"]
	UNITS = ["Inches", "Millimeters", "Points", "Picas"]
	UNITS_TO_MM = [25.4, 1, 127 / 360.0, 127 / 30.0]
	COMPOSITE_MODES = ["Union", "Clip to backdrop", "Clip to layer", "Intersection"]
	COMPOSITE_SPACES = ["RGB (linear)", "RGB (perceptual)", "LAB"]
	TAG_COLORS = ["None", "Blue", "Green", "Yellow", "Orange", "Brown", "Red", "Violet", "Gray"]
	COMPRESSION_MODES = ["None", "RLE", "Zlib", "Fractal"]

	BLEND_MODES = [
		"Normal (legacy)",
		"Dissolve (legacy)",
		"Behind (legacy)",
		"Multiply (legacy)",
		"Screen (legacy)",
		"Old broken Overlay",
		"Difference (legacy)",
		"Addition (legacy)",
		"Subtract (legacy)",
		"Darken only (legacy)",
		"Lighten only (legacy)",
		"Hue (HSV) (legacy)",
		"Saturation (HSV) (legacy)",
		"Color (HSL) (legacy)",
		"Value (HSV) (legacy)",
		"Divide (legacy)",
		"Dodge (legacy)",
		"Burn (legacy)",
		"Hard Light (legacy)",
		"Soft light (legacy)",
		"Grain extract (legacy)",
		"Grain merge (legacy)",
		"Color erase (legacy)",
		"Overlay",
		"Hue (LCH)",
		"Chroma (LCH)",
		"Color (LCH)",
		"Lightness (LCH)",
		"Normal",
		"Behind",
		"Multiply",
		"Screen",
		"Difference",
		"Addition",
		"Substract",
		"Darken only",
		"Lighten only",
		"Hue (HSV)",
		"Saturation (HSV)",
		"Color (HSL)",
		"Value (HSV)",
		"Divide",
		"Dodge",
		"Burn",
		"Hard light",
		"Soft light",
		"Grain extract",
		"Grain merge",
		"Vivid light",
		"Pin light",
		"Linear light",
		"Hard mix",
		"Exclusion",
		"Linear burn",
		"Luma/Luminance darken only",
		"Luma/Luminance lighten only",
		"Luminance",
		"Color erase",
		"Erase",
		"Merge",
		"Split",
		"Pass through",
	]

	PROP_END: int = 0
	PROP_COLORMAP = 1
	PROP_ACTIVE_LAYER = 2
	PROP_ACTIVE_CHANNEL = 3
	PROP_SELECTION = 4
	PROP_FLOATING_SELECTION = 5
	PROP_OPACITY = 6
	PROP_MODE = 7
	PROP_VISIBLE = 8
	PROP_LINKED = 9
	PROP_LOCK_ALPHA = 10
	PROP_APPLY_MASK = 11
	PROP_EDIT_MASK = 12
	PROP_SHOW_MASK = 13
	PROP_SHOW_MASKED = 14
	PROP_OFFSETS = 15
	PROP_COLOR = 16
	PROP_COMPRESSION = 17
	PROP_GUIDES = 18
	PROP_RESOLUTION = 19
	PROP_TATTOO = 20
	PROP_PARASITES = 21
	PROP_UNIT = 22
	PROP_PATHS = 23
	PROP_USER_UNIT = 24
	PROP_VECTORS = 25
	PROP_TEXT_LAYER_FLAGS = 26
	PROP_OLD_SAMPLE_POINTS = 27
	PROP_LOCK_CONTENT = 28
	PROP_GROUP_ITEM = 29
	PROP_ITEM_PATH = 30
	PROP_GROUP_ITEM_FLAGS = 31
	PROP_LOCK_POSITION = 32
	PROP_FLOAT_OPACITY = 33
	PROP_COLOR_TAG = 34
	PROP_COMPOSITE_MODE = 35
	PROP_COMPOSITE_SPACE = 36
	PROP_BLEND_SPACE = 37
	PROP_FLOAT_COLOR = 38
	PROP_SAMPLE_POINTS = 39
	PROP_NUM_PROPS = 40

	def __init__(self, parent):
		self.parent = parent
		self.parasites: list[GimpParasite] = []
		self.guidelines: list[tuple[bool, int]] = []
		self.itemPath: str | None = None
		self.vectors: list[GimpVector] = []
		self.colorMap: list[tuple[int, int, int]] = []
		self.userUnits: GimpUserUnits | None = None
		self.samplePoints: list[tuple[int, int]] = []
		self.selected: bool = False
		self.isSelection: bool = False
		self.selectionAttachedTo: str | None = None
		self.blendMode: int = 0  # one of self.BLEND_MODES
		self.visible: bool = False
		self.isLinked: bool = False
		self.lockAlpha: bool = False
		self.applyMask: bool = False
		self.editingMask: bool = False
		self.showMask: bool = False
		self.showMasked: bool = False
		self.xOffset: int = 0
		self.yOffset: int = 0
		self.compression: int = 0  # one of self.COMPRESSION_MODES
		self.horizontalResolution = None
		self.verticalResolution = None
		self.uniqueId = None
		self.units: int = 0  # one of self.UNITS
		self.textLayerFlags = None
		self.locked = None
		self.isGroup = None
		self.groupItemFlags: int = 0
		self.positionLocked: bool = False
		self.opacity: float = 1.0
		self.colorTag: int = 0  # one of self.TAG_COLORS
		self.compositeMode: int = 0  # one of self.COMPOSITE_MODES
		self.compositeSpace: int = 0  # one of self.COMPOSITE_SPACES
		self.blendSpace = None
		self.color = None
		self.vectorsVersion: int = 0
		self.activeVectorIndex: int = 0
		self.paths = []

	def getBlendMode(self) -> str:
		"""return the blend mode as a string."""
		return self.BLEND_MODES[self.blendMode]

	def getCompression(self) -> str:
		"""return the compression as a string."""
		return self.COMPRESSION_MODES[self.compression]

	def getUnits(self) -> str:
		"""return the units as a string."""
		return self.UNITS[self.units]

	def getTagColours(self):
		"""return the tag colours as a string."""
		return self.TAG_COLORS[self.colorTag]

	def getCompositeModes(self):
		"""return the composite mode as a string."""
		return self.COMPOSITE_MODES[abs(self.compositeMode)]

	def getCompositeSpaces(self):
		"""return the composite spaces as a string."""
		return self.COMPOSITE_SPACES[abs(self.compositeSpace)]

	@property
	def _POINTER_SIZE(self) -> int:
		"""
		Determine the size of the "pointer" datatype
		based on the document version

		NOTE: prior to version 11, it was 32-bit,
			since then it is 64-bit, thus supporting
			larger image files
		"""
		if self.doc.version >= 11:
			return 64
		return 32

	def _pointerDecode(self, ioBuf: IO) -> int:
		if self._POINTER_SIZE == 64:
			return ioBuf.u64
		return ioBuf.u32

	def _pointerEncode(self, ptr: int, ioBuf: IO | None = None) -> bytearray:
		if ioBuf is None:
			ioBuf = IO()
		if self._POINTER_SIZE == 64:
			ioBuf.u64 = ptr
		else:
			ioBuf.u32 = ptr
		return ioBuf.data

	@property
	def doc(self):
		"""
		Get the main document object
		"""
		item = self
		while item.parent != item:
			item = item.parent
		return item

	@property
	def root(self):
		"""
		Get the root of the file object tree
		(Which is the same as self.doc)
		"""
		return self.doc

	@property
	def tattoo(self):
		"""
		This is the gimp nomenclature for the item's unique id
		"""
		return self.uniqueId

	@tattoo.setter
	def tattoo(self, tattoo):
		"""
		This is the gimp nomenclature for the item's unique id
		"""
		self.uniqueId = tattoo

	def _parasitesDecode(self, data: bytearray) -> int:
		"""
		decode list of parasites
		"""
		index: int = 0
		while index < len(data):
			parasite = GimpParasite()
			index = parasite.decode(data, index)
			self.parasites.append(parasite)
		return index

	def _parasitesEncode(self):
		"""
		encode list of parasites
		"""
		ioBuf = IO()
		for parasite in self.parasites:
			ioBuf.addBytes(parasite.encode())
		return ioBuf.data

	def _guidelinesDecode(self, data):
		"""
		decode guidelines
		"""
		index: int = 0
		while index < len(data):
			position = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			isVertical = struct.unpack(">B", data[index])[0] == 2
			index += 1
			self.guidelines.append((isVertical, position))

	def _itemPathDecode(self, data):
		"""
		decode item path
		"""
		index: int = 0
		path = []
		while index < len(data):
			p = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			path.append(p)
		self.itemPath = path

	def _vectorsDecode(self, data):
		"""
		decode vectors
		"""
		index: int = 0
		self.vectorsVersion = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		self.activeVectorIndex = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		numPaths = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		for _ in range(numPaths):
			gimpV = GimpVector(self)
			gimpV.decode(data)
			self.vectors.append(gimpV)

	@property
	def activeVector(self):
		"""
		get the vector that is currently active
		"""
		return self.vectors[self.activeVectorIndex]

	@property
	def expanded(self) -> bool:
		"""
		is the group layer expanded
		"""
		return self.groupItemFlags & 0x00000001 > 0

	@expanded.setter
	def expanded(self, expanded):
		"""
		is the group layer expanded
		"""
		if expanded:
			self.groupItemFlags |= 0x00000001
		else:
			self.groupItemFlags &= ~0x00000001

	def _colormapDecode_(self, data, index=None):
		"""
		:param data: can be bytes or an IO object

		decode colormap/palette
		"""
		ioObj = None
		if isinstance(data, IO):
			ioObj = data
			index = data.index
			data = data.data
		_ = struct.unpack(">I", data[0:4])[0]  # number of colors
		index += 4
		colors = []
		while index < len(data):
			r = data[index]
			index += 1
			g = data[index]
			index += 1
			b = data[index]
			index += 1
			colors.append((r, g, b))
		self.colorMap = colors
		if ioObj is not None:
			ioObj.index = index

	def _userUnitsDecode_(self, data):
		"""
		decode a set of user-defined measurement units
		"""
		u = GimpUserUnits()
		# u.decode(data)
		u.decode(data)
		self.userUnits = u

	def _samplePointsDecode_(self, data):
		"""
		decode a series of points
		"""
		index: int = 0
		samplePoints = []
		while index < len(data):
			x = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			y = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			samplePoints.append((x, y))
		self.samplePoints = samplePoints

	def _propertyDecode(self, propertyType, data):
		"""
		decode a single property

		Many properties are in the form
		propertyType: one of PROP_
		lengthOfData: 4
		data: varies but is often ioBuf.32 or ioBuf.boolean
		"""
		ioBuf = IO(data, boolSize=32)
		# print('DECODING PROPERTY',propertyType,len(data))
		if propertyType == self.PROP_COLORMAP:
			self._colormapDecode_(ioBuf)
		elif propertyType == self.PROP_ACTIVE_LAYER:
			self.selected = True
		elif propertyType == self.PROP_ACTIVE_CHANNEL:
			self.selected = True
		elif propertyType == self.PROP_SELECTION:
			self.isSelection = True
		elif propertyType == self.PROP_FLOATING_SELECTION:
			self.selectionAttachedTo = ioBuf.u32
		elif propertyType == self.PROP_OPACITY:
			self.opacity = ioBuf.u32
		elif propertyType == self.PROP_MODE:
			self.blendMode = ioBuf.u32
		elif propertyType == self.PROP_VISIBLE:
			self.visible = ioBuf.boolean
		elif propertyType == self.PROP_LINKED:
			self.isLinked = ioBuf.boolean
		elif propertyType == self.PROP_LOCK_ALPHA:
			self.lockAlpha = ioBuf.boolean
		elif propertyType == self.PROP_APPLY_MASK:
			self.applyMask = ioBuf.boolean
		elif propertyType == self.PROP_EDIT_MASK:
			self.editingMask = ioBuf.boolean
		elif propertyType == self.PROP_SHOW_MASK:
			self.showMask = ioBuf.boolean
		elif propertyType == self.PROP_SHOW_MASKED:
			self.showMasked = ioBuf.boolean
		elif propertyType == self.PROP_OFFSETS:
			self.xOffset = ioBuf.i32
			self.yOffset = ioBuf.i32
		elif propertyType == self.PROP_COLOR:
			r = ioBuf.byte
			g = ioBuf.byte
			b = ioBuf.byte
			self.color = [r, g, b]
		elif propertyType == self.PROP_COMPRESSION:
			self.compression = ioBuf.byte
		elif propertyType == self.PROP_GUIDES:
			self._guidelinesDecode(data)
		elif propertyType == self.PROP_RESOLUTION:
			self.horizontalResolution = ioBuf.float32
			self.verticalResolution = ioBuf.float32
		elif propertyType == self.PROP_TATTOO:
			self.uniqueId = data.hex()
		elif propertyType == self.PROP_PARASITES:
			self._parasitesDecode(data)
		elif propertyType == self.PROP_UNIT:
			self.units = ioBuf.u32
		elif propertyType == self.PROP_PATHS:
			_numPaths = ioBuf.u32
			"""
			for _ in range(numPaths):
				nRead, path = self._pathDecode_(data[index:])
				self.paths.append(path)
				index += nRead
			"""
		elif propertyType == self.PROP_USER_UNIT:
			self._userUnitsDecode_(data)
		elif propertyType == self.PROP_VECTORS:
			pass
			# self._vectorsDecode_(data)
		elif propertyType == self.PROP_TEXT_LAYER_FLAGS:
			if isinstance(data, bytes):
				self.textLayerFlags = int.from_bytes(data, byteorder="big")
			else:
				self.textLayerFlags = int(data)
		elif propertyType == self.PROP_OLD_SAMPLE_POINTS:
			raise Exception("ERR: old sample points structure not supported")
		elif propertyType == self.PROP_LOCK_CONTENT:
			self.locked = ioBuf.boolean
		elif propertyType == self.PROP_GROUP_ITEM:
			self.isGroup = True
		elif propertyType == self.PROP_ITEM_PATH:
			self._itemPathDecode(data)
		elif propertyType == self.PROP_GROUP_ITEM_FLAGS:
			self.groupItemFlags = ioBuf.u32
		elif propertyType == self.PROP_LOCK_POSITION:
			self.positionLocked = ioBuf.boolean
		elif propertyType == self.PROP_FLOAT_OPACITY:
			self.opacity = ioBuf.float32
		elif propertyType == self.PROP_COLOR_TAG:
			self.colorTag = ioBuf.u32
		elif propertyType == self.PROP_COMPOSITE_MODE:
			self.compositeMode = ioBuf.i32
		elif propertyType == self.PROP_COMPOSITE_SPACE:
			self.compositeSpace = ioBuf.i32
		elif propertyType == self.PROP_BLEND_SPACE:
			self.blendSpace = ioBuf.u32
		elif propertyType == self.PROP_FLOAT_COLOR:
			r = ioBuf.float32
			g = ioBuf.float32
			b = ioBuf.float32
			self.color = [r, g, b]
		elif propertyType == self.PROP_SAMPLE_POINTS:
			self._samplePointsDecode_(data)
		else:
			raise Exception("Unknown property id " + str(propertyType))
		return ioBuf.index

	def _propertyEncode(self, propertyType):
		"""
		encode a single property

		Many properties are in the form
		propertyType: one of PROP_
		lengthOfData: 4
		data: varies but is often ioBuf.32 or ioBuf.boolean

		If the property is the same as the default, or not specified, returns empty array
		"""
		ioBuf = IO(boolSize=32)
		if propertyType == self.PROP_COLORMAP:
			if self.colorMap is not None and self.colorMap:
				pass
				ioBuf.u32 = self.PROP_COLORMAP
				# ioBuf.addBytes(self._colormapEncode_())
		elif propertyType == self.PROP_ACTIVE_LAYER:
			if self.selected is not None and self.selected:
				ioBuf.u32 = self.PROP_ACTIVE_LAYER
		elif propertyType == self.PROP_ACTIVE_CHANNEL:
			if self.selected is not None and self.selected:
				ioBuf.u32 = self.PROP_ACTIVE_LAYER
		elif propertyType == self.PROP_SELECTION:
			if self.isSelection is not None and self.isSelection:
				ioBuf.u32 = self.PROP_SELECTION
		elif propertyType == self.PROP_FLOATING_SELECTION:
			if self.selectionAttachedTo is not None:
				ioBuf.u32 = self.PROP_FLOATING_SELECTION
				ioBuf.u32 = self.selectionAttachedTo
		elif propertyType == self.PROP_OPACITY:
			if self.opacity is not None and not isinstance(self.opacity, float):
				ioBuf.u32 = self.PROP_OPACITY
				ioBuf.u32 = self.opacity
		elif propertyType == self.PROP_MODE:
			if self.blendMode is not None:
				ioBuf.u32 = self.PROP_MODE
				ioBuf.u32 = self.blendMode
		elif propertyType == self.PROP_VISIBLE:
			if self.visible is not None:
				ioBuf.u32 = self.PROP_VISIBLE
				ioBuf.boolean = self.visible
		elif propertyType == self.PROP_LINKED:
			if self.isLinked is not None and self.isLinked:
				ioBuf.u32 = self.PROP_LINKED
				ioBuf.boolean = self.isLinked
		elif propertyType == self.PROP_LOCK_ALPHA:
			if self.lockAlpha is not None and self.lockAlpha:
				ioBuf.u32 = self.PROP_LOCK_ALPHA
				ioBuf.boolean = self.lockAlpha
		elif propertyType == self.PROP_APPLY_MASK:
			if self.applyMask is not None:
				ioBuf.u32 = self.PROP_APPLY_MASK
				ioBuf.boolean = self.applyMask
		elif propertyType == self.PROP_EDIT_MASK:
			if self.editingMask is not None and self.editingMask:
				ioBuf.u32 = self.PROP_EDIT_MASK
				ioBuf.boolean = self.editingMask
		elif propertyType == self.PROP_SHOW_MASK:
			if self.showMask is not None and self.showMask:
				ioBuf.u32 = self.PROP_SHOW_MASK
				ioBuf.boolean = self.showMask
		elif propertyType == self.PROP_SHOW_MASKED:
			if self.showMasked is not None:
				ioBuf.u32 = self.PROP_SHOW_MASKED
				ioBuf.boolean = self.showMasked
		elif propertyType == self.PROP_OFFSETS:
			if self.xOffset is not None and self.yOffset is not None:
				ioBuf.u32 = self.PROP_OFFSETS
				ioBuf.i32 = self.xOffset
				ioBuf.i32 = self.yOffset
		elif propertyType == self.PROP_COLOR:
			if (
				self.color is not None
				and not isinstance(self.color[0], float)
				and not isinstance(self.color[1], float)
				and not isinstance(self.color[2], float)
			):
				ioBuf.u32 = self.PROP_COLOR
				ioBuf.byte = self.color[0]
				ioBuf.byte = self.color[1]
				ioBuf.byte = self.color[2]
		elif propertyType == self.PROP_COMPRESSION:
			if self.compression is not None:
				ioBuf.u32 = self.PROP_COMPRESSION
				ioBuf.u32 = self.compression
		elif propertyType == self.PROP_GUIDES:
			if self.guidelines is not None and self.guidelines:
				pass
				# ioBuf.u32 = self.PROP_GUIDES
				# ioBuf.addBytes(self._guidelinesEncode_())
		elif propertyType == self.PROP_RESOLUTION:
			if self.horizontalResolution is not None and self.verticalResolution is not None:
				ioBuf.u32 = self.PROP_RESOLUTION
				ioBuf.u32 = int(self.horizontalResolution)
				ioBuf.i32 = int(self.verticalResolution)
		elif propertyType == self.PROP_TATTOO:
			if self.uniqueId is not None:
				ioBuf.u32 = int(self.uniqueId, 16)
		elif propertyType == self.PROP_PARASITES:
			if self.parasites is not None and self.parasites:
				ioBuf.u32 = self.PROP_PARASITES
				ioBuf.addBytes(self._parasitesEncode())
		elif propertyType == self.PROP_UNIT:
			if self.units is not None:
				ioBuf.u32 = self.PROP_UNIT
				ioBuf.u32 = self.units
		elif propertyType == self.PROP_PATHS:
			if self.paths is not None and self.paths:
				# ioBuf.u32 = self.PROP_PATHS
				# ioBuf.u32 = len(self.paths)
				"""
				for path in self.paths:
					ioBuf.append(self._pathEncode_(path))
				"""
		elif propertyType == self.PROP_USER_UNIT:
			if self.userUnits is not None:
				pass
				# ioBuf.u32 = self.PROP_USER_UNIT
				# ioBuf.addBytes(self._userUnitsEncode_())
		elif propertyType == self.PROP_VECTORS:
			if self.vectors is not None and self.vectors:
				pass
				# ioBuf.u32 = self.PROP_VECTORS
				# ioBuf.addBytes(self._vectorsEncode_())
		elif propertyType == self.PROP_TEXT_LAYER_FLAGS:
			if self.textLayerFlags is not None:
				ioBuf.u32 = self.PROP_TEXT_LAYER_FLAGS
				ioBuf.u32 = self.textLayerFlags
		elif propertyType == self.PROP_OLD_SAMPLE_POINTS:
			pass
		elif propertyType == self.PROP_LOCK_CONTENT:
			if self.locked is not None and self.locked:
				ioBuf.u32 = self.PROP_LOCK_CONTENT
				ioBuf.boolean = self.locked
		elif propertyType == self.PROP_GROUP_ITEM:
			if self.isGroup is not None and self.isGroup:
				ioBuf.u32 = self.PROP_GROUP_ITEM
		elif propertyType == self.PROP_ITEM_PATH:
			if self.itemPath is not None:
				pass
				# ioBuf.u32 = self.PROP_ITEM_PATH
				# ioBuf.addBytes(self._itemPathEncode_())
		elif propertyType == self.PROP_GROUP_ITEM_FLAGS:
			if self.groupItemFlags is not None:
				ioBuf.u32 = self.PROP_GROUP_ITEM_FLAGS
				ioBuf.u32 = self.groupItemFlags
		elif propertyType == self.PROP_LOCK_POSITION:
			if self.positionLocked is not None and self.positionLocked:
				ioBuf.u32 = self.PROP_LOCK_POSITION
				ioBuf.boolean = self.positionLocked
		elif propertyType == self.PROP_FLOAT_OPACITY:
			if self.opacity is not None and isinstance(self.opacity, float):
				ioBuf.u32 = self.PROP_FLOAT_OPACITY
				ioBuf.float32 = self.opacity
		elif propertyType == self.PROP_COLOR_TAG:
			if self.colorTag is not None:
				ioBuf.u32 = self.PROP_COLOR_TAG
				ioBuf.u32 = self.colorTag
		elif propertyType == self.PROP_COMPOSITE_MODE:
			if self.compositeMode is not None:
				ioBuf.u32 = self.PROP_COMPOSITE_MODE
				ioBuf.i32 = self.compositeMode
		elif propertyType == self.PROP_COMPOSITE_SPACE:
			if self.compositeSpace is not None:
				ioBuf.u32 = self.PROP_COMPOSITE_SPACE
				ioBuf.i32 = self.compositeSpace
		elif propertyType == self.PROP_BLEND_SPACE:
			if self.blendSpace is not None:
				ioBuf.u32 = self.PROP_BLEND_SPACE
				ioBuf.u32 = self.blendSpace
		elif propertyType == self.PROP_FLOAT_COLOR:
			if (
				self.color is not None
				and isinstance(self.color[0], float)
				and isinstance(self.color[1], float)
				and isinstance(self.color[2], float)
			):
				ioBuf.u32 = self.PROP_FLOAT_COLOR
				ioBuf.float32 = self.color[0]
				ioBuf.float32 = self.color[1]
				ioBuf.float32 = self.color[2]
		elif propertyType == self.PROP_SAMPLE_POINTS:
			if self.samplePoints is not None and self.samplePoints:
				pass
				# ioBuf.u32 = self.PROP_SAMPLE_POINTS
				# self.addBytes(self._samplePointsEncode_())
		else:
			raise Exception("Unknown property id " + str(propertyType))
		return ioBuf.data

	def _propertiesDecode(self, ioBuf: IO):
		"""Decode a list of properties"""
		while True:
			try:
				propertyType = ioBuf.u32
				dataLength = ioBuf.u32
			except struct.error:  # end of data, so that's that.
				break
			if propertyType == 0:
				break
			self._propertyDecode(propertyType, ioBuf.getBytes(dataLength))
		return ioBuf.index

	def _propertiesEncode(self):
		"""Encode a list of properties"""
		ioBuf = IO()
		for propertyType in range(1, self.PROP_NUM_PROPS):
			moData = self._propertyEncode(propertyType)
			if moData:
				ioBuf.addBytes(moData)
		return ioBuf.data

	def __repr__(self, indent: str = ""):
		"""Get a textual representation of this object"""
		ret: list[str] = []
		if self.itemPath is not None:
			ret.append("Item Path: " + str(self.itemPath))
		if self.selected is not None:
			ret.append("Selected: " + str(self.selected))
		if self.isSelection is not None:
			ret.append("is Selection: " + str(self.isSelection))
		if self.selectionAttachedTo is not None:
			ret.append("Selection Attached To: " + str(self.selectionAttachedTo))
		if self.blendMode is not None:
			ret.append("Blend Mode: " + self.getBlendMode())
		if self.visible is not None:
			ret.append("Visible: " + str(self.visible))
		if self.isLinked is not None:
			ret.append("Linked: " + str(self.isLinked))
		if self.lockAlpha is not None:
			ret.append("Alpha Locked: " + str(self.lockAlpha))
		if self.applyMask is not None:
			ret.append("Apply Mask: " + str(self.applyMask))
		if self.editingMask is not None:
			ret.append("Editing Mask: " + str(self.editingMask))
		if self.showMask is not None:
			ret.append("Show Mask: " + str(self.showMask))
		if self.showMasked is not None:
			ret.append("Show Masked: " + str(self.showMasked))
		if self.xOffset is not None:
			ret.append("Offset: " + str(self.xOffset) + " x " + str(self.yOffset))
		if self.compression is not None:
			ret.append("Compression: " + self.getCompression())
		if self.horizontalResolution is not None:
			res = str(self.horizontalResolution) + "ppi x " + str(self.verticalResolution) + "ppi"
			ret.append("Resolution: " + res)
		if self.uniqueId is not None:
			ret.append("Unique ID (tattoo): " + str(self.uniqueId))
		if self.units is not None:
			ret.append("Units: " + self.getUnits())
		if self.textLayerFlags is not None:
			ret.append("Text Layer Flags: " + str(self.textLayerFlags))
		if self.locked is not None:
			ret.append("Locked: " + str(self.locked))
		if self.isGroup is not None:
			ret.append("Is Group: " + str(self.isGroup))
		if self.groupItemFlags is not None:
			ret.append("Group Items Flag: " + str(self.groupItemFlags))
		if self.positionLocked is not None:
			ret.append("Position Locked: " + str(self.positionLocked))
		if self.opacity is not None:
			ret.append("Opacity: " + str(self.opacity))
		if self.colorTag is not None:
			ret.append("Tag Color: " + self.getTagColours())
		if self.compositeMode is not None:
			auto = "Auto " if self.compositeMode < 0 else ""  # negative values are "Auto"
			ret.append("Composite Mode: " + auto + self.getCompositeModes())
		if self.compositeSpace is not None:
			auto = "Auto " if self.compositeSpace < 0 else ""  # negative values are "Auto"
			ret.append("Composite Space: " + auto + self.getCompositeSpaces())
		if self.blendSpace is not None:
			ret.append("Blend Space: " + str(self.blendSpace))
		if self.color is not None:
			ret.append(
				"Color: ("
				+ str(self.color[0])
				+ ","
				+ str(self.color[1])
				+ ","
				+ str(self.color[2])
				+ ")"
			)
		if self.userUnits is not None:
			ret.append("User Units: ")
			ret.append(self.userUnits.__repr__(indent + "\t"))
		if self.parasites:
			ret.append("Parasites: ")
			for item in self.parasites:
				ret.append(item.__repr__(indent + "\t"))
		if self.guidelines:
			ret.append("Guidelines: ")
			for item in self.guidelines:
				ret.append(item.__repr__())
		if self.samplePoints:
			ret.append("Sample Points: ")
			for item in self.samplePoints:
				ret.append("(" + str(item[0]) + "," + str(item[1]) + ")")
		if self.vectors:
			ret.append("Vectors: ")
			for item in self.vectors:
				ret.append(item.__repr__(indent + "\t"))
		if self.colorMap:
			ret.append("Color Map: ")
			for i in range(len(self.colorMap)):
				color = self.colorMap[i]
				ret.append(
					i + ": (" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")"
				)
		return indent + (("\n" + indent).join(ret))


class GimpUserUnits:
	"""
	user-defined measurement units
	"""

	def __init__(self):
		self.factor: int = 0
		self.numDigits: int = 0
		self.id = ""
		self.symbol = ""
		self.abbrev = ""
		self.sname = ""
		self.pname = ""

	def decode(self, data: bytearray, index: int = 0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index)
		self.factor = ioBuf.float32
		self.numDigits = ioBuf.u32
		self.id = ioBuf.sz754
		self.symbol = ioBuf.sz754
		self.abbrev = ioBuf.sz754
		self.sname = ioBuf.sz754
		self.pname = ioBuf.sz754
		return ioBuf.index

	def encode(self):
		"""
		convert this object to raw bytes
		"""
		ioBuf = IO()
		ioBuf.float32 = self.factor
		ioBuf.u32 = self.numDigits
		ioBuf.sz754 = self.id
		ioBuf.sz754 = self.symbol
		ioBuf.sz754 = self.abbrev
		ioBuf.sz754 = self.sname
		ioBuf.sz754 = self.pname
		return ioBuf.data

	def __repr__(self, indent: str = ""):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append("Factor: " + str(self.factor))
		ret.append("Num Digits: " + str(self.numDigits))
		ret.append("ID: " + str(self.id))
		ret.append("Symbol: " + str(self.symbol))
		ret.append("Abbreviation: " + str(self.abbrev))
		ret.append("Singular Name: " + str(self.sname))
		ret.append("Plural Name: " + str(self.pname))
		return indent + (("\n" + indent).join(ret))
