from collections import namedtuple
from struct import unpack
import logging
import mmap
import numpy as np
from math import floor


class Tile:
	logger = logging.getLogger("Tile")
	headerOffset = None
	TileHeader = namedtuple('TileHeader',
	                        'magic version xsize ysize zsize altitude verticalResolution latitude longitude latSize lonSize '
	                        'density valueOffset creationTime ceiling checksum')

	class CalculatedTileHeader:
		horizontalLayerSize = 0
		horizontalLayerSizeBytes = 0
		horizontalRowSizeBytes = 0
		numberOfGridNodes = 0
		fileLength = 0
		horizontalResolution = 0

	header = None
	calculatedHeader = None
	fp = None
	mm = None
	density = None

	def __init__(self, tileFilename):

		self.fp = open(tileFilename, 'rb')
		self.mm = mmap.mmap(self.fp.fileno(), 0, access=mmap.ACCESS_READ)

		# Read the header
		self.headerOffset = 70
		self.header = self.TileHeader._make(unpack('<8sbIIIhHffffbhIH20s', self.mm[0:70]))
		if self.header.magic != b'DMTRTILE':
			raise RuntimeError("File is not a Dimetor tile!")
		if self.header.version > 2:
			raise RuntimeError("Unsupported Dimetor tile version: {}!".format(self.header.version))

		if self.header.version == 1:
			# Density correction: see Tile.hpp in the C++ version
			if self.header.density == 8:
				self.density = 1
			elif self.header.density == 2:
				self.density = 4
			elif self.header.density == 1:
				self.density = 8
		else:
			self.density = self.header.density

		self.logger.debug("magic = {}".format(self.header.magic))
		self.logger.debug("version = {}".format(self.header.version))
		self.logger.debug("xsize = {}".format(self.header.xsize))
		self.logger.debug("ysize = {}".format(self.header.ysize))
		self.logger.debug("zsize = {}".format(self.header.zsize))
		self.logger.debug("altitude = {}".format(self.header.altitude))
		self.logger.debug("verticalResolution = {}".format(self.header.verticalResolution))
		self.logger.debug("latitude = {}".format(self.header.latitude))
		self.logger.debug("longitude = {}".format(self.header.longitude))
		self.logger.debug("latSize = {}".format(self.header.latSize))
		self.logger.debug("lonSize = {}".format(self.header.lonSize))
		self.logger.debug("density = {}".format(self.header.density))
		self.logger.debug("valueOffset = {}".format(self.header.valueOffset))
		self.logger.debug("creationTime = {}".format(self.header.creationTime))
		self.logger.debug("ceiling = {}".format(self.header.ceiling))
		self.logger.debug("checksum = {}".format(self.header.checksum))

		if self.density != 1 and self.density != 4 and self.density != 8:
			raise RuntimeError("Only node densities of 1, 4 or 8 are currently supported!")
		if self.header.xsize != self.header.ysize:
			raise RuntimeError("xsize and ysize must be the same")

		self.calculatedHeader = self.CalculatedTileHeader()
		self.calculatedHeader.horizontalLayerSize = self.header.xsize * self.header.ysize
		if self.density == 1:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize / 8)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize / 8)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes / 8)
		elif self.density == 4:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize / 2)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize / 2)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes / 2)
		elif self.density == 8:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes)
		elif self.density == 16:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize * 2)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize * 2)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes * 2)
		self.calculatedHeader.horizontalResolution = int(self.header.latSize * 60 * 60 / self.header.xsize)
		self.calculatedHeader.tileBufferLength = self.calculatedHeader.fileLength + self.headerOffset

		self.logger.debug(self.calculatedHeader.horizontalLayerSize)
		self.logger.debug(self.calculatedHeader.horizontalLayerSizeBytes)
		self.logger.debug(self.calculatedHeader.horizontalRowSizeBytes)
		self.logger.debug(self.calculatedHeader.numberOfGridNodes)
		self.logger.debug(self.calculatedHeader.fileLength)
		self.logger.debug(self.calculatedHeader.horizontalResolution)

	def roundHalfUp(self, x):
		floorX = floor(x)
		if(x - floorX >= 0.5):
			return floorX +1
		return floorX

	def findCoordinates(self, lat: float, lon: float) -> (int, int, int):
		"""
		Find the z layer where the node value at the given coordinate is 0 for the first time.
		:param lat:
		:param lon:
		:return:
		"""
		x = self.roundHalfUp((lon - self.header.longitude) * self.header.xsize)
		y = self.roundHalfUp((self.header.latitude - lat) * self.header.ysize)

		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return x, y, z

		return -1, -1, -1

	def getTileCoordinates(self, lat: float, lon: float, altitude: float) -> (int, int, int):
		"""
		Convert WGS 84 coordinates to tile coordinates
		:param lat:
		:param lon:
		:param altitude:
		:return:
		"""
		x = self.roundHalfUp((lon - self.header.longitude) * self.header.xsize)
		y = self.roundHalfUp((self.header.latitude - lat) * self.header.ysize)
		z = self.roundHalfUp((altitude - self.header.altitude) / self.header.verticalResolution)
		return x, y, z

	def getLatLong(self, x: float, y: float) -> (float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:return:
		"""

		lon = self.header.longitude + x / self.header.xsize
		lat = self.header.latitude - y / self.header.ysize
		return lon, lat

	def getLatLongAlt(self, x: int, y: int, z: int) -> (float, float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:param z:
		:return:
		"""
		lon = x / self.header.xsize + self.header.longitude
		lat = self.header.latitude - y / self.header.ysize
		altitude = z * self.header.verticalResolution + self.header.altitude
		return lon, lat, altitude

	def getNode(self, x: int, y: int, z: int):

		if x >= self.header.xsize or y >= self.header.ysize or z >= self.header.zsize or x < 0 or y < 0 or z < 0:
			return None

		if self.density == 1:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + int(
				x / 8)
			bit = x % 8
			return (self.mm[offset + self.headerOffset] & (1 << bit)) >> bit
		elif self.density == 4:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + int(
				x / 2)
			tuple = x % 2
			bufVal = (self.mm[offset + self.headerOffset] & (0xF0 >> (tuple * 4))) >> ((1 - tuple) * 4)
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		elif self.density == 8:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + x
			bufVal = self.mm[offset + self.headerOffset]
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		else:
			raise RuntimeError("Unsupported density")

	def getZElevation(self, x: int, y: int):
		"""
		Calculates the Z elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return z

	def getElevation(self, x: int, y: int):
		"""
		Returns elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		return self.getZElevation(x, y) * self.header.verticalResolution + self.header.altitude

	def __del__(self):

		self.mm.close()
		self.fp.close()

	# TODO: check if getLayerZ is needed
	def getLayerZ(self, z: int):
		"""
		Extract layer points and return as 2D array.
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			column = []
			for y in range(0, self.header.ysize):
				column.append(self.getNode(x, y, z))
			points.append(column)
		return points

	def getTileLayers(self, returnAsList, return2D, *layers):
		"""
        Extract all point values of a layer and return a list of 1D/2D arrays OR a 3D array.
		:return:
		"""

		if self.density != 1:
			raise RuntimeError("Unsupported density")

		bitData = np.unpackbits(self.mm)
		bitData = bitData[self.headerOffset * 8:]

		# unpackbits unpacks the bits in an opposite order so they need to be flipped below.
		bitDataByteOrder = bitData.reshape((len(bitData) // 8, 8))
		bitDataByteOrder = np.flip(bitDataByteOrder, axis=1)
		bitData = bitDataByteOrder.flatten()

		if not layers:
			layers = range(self.header.zsize)

		extractedLayers = []

		for z in layers:
			# Layer extracted as 1D array
			layer = bitData[z * self.header.xsize * self.header.ysize:(z + 1) * self.header.xsize * self.header.ysize]
			if return2D:
				extractedLayers.append(layer.reshape(self.header.xsize, self.header.ysize))
			else:
				extractedLayers.append(layer)

		if returnAsList:
			return extractedLayers
		else:
			return np.asarray(extractedLayers)

	# TODO: check if getNodeLayerZ is needed
	def getNodeLayerZ(self, value: int, z: int):
		"""
		Extract all the points in a layer with a specific value (ex. 0 or 1)
		:param value:
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					points.append([x, y])
		npArray = np.asarray(points)
		return npArray

	# TODO: check if getNodeLayerZset is needed
	def getNodeLayerZset(self, value: int, z: int):
		""""
		Extract all the points in a layer with a specific value (ex. 0 or 1) but return set.
		:param value:
		:param z:
		:return:
		"""
		pSet = set()
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					pSet.add((x, y))
		return pSet

	def getLayerHeight(self, z: int):
		"""
		Get the height of a layer passing the z layer index.
		:param z:
		:return:
		"""
		return self.header.altitude + z * self.header.verticalResolution

	def getLayerFloorAndCeiling(self, z: int) -> (float, float):
		"""
		Get the bottom and top of a layer passing the z layer index.
		:param z:
		:return:
		"""
		height = self.getLayerHeight(z)

		floor = height - 0.5 * self.header.verticalResolution
		ceiling = height + 0.5 * self.header.verticalResolution

		return floor, ceiling

	@staticmethod
	def generateTilespec(latitude, longitude, xsize = 1800, ysize=1800):
		"""
		Generate the tilespec for the tile that contains the location at lat, lon
		:param lat:
		:param lon:
		:return:
		"""
		latLLC = floor(latitude)
		lonLLC = floor(longitude)

		epsilonLat = 1 / (2 * ysize)
		epsilonLong = 1 / (2 * xsize)

		if (latitude - latLLC >= (1 - epsilonLat)):
			latitude += epsilonLat * 1.5

		if (longitude - lonLLC >= (1 - epsilonLong)):
			longitude += epsilonLong * 1.5

		NS = 'n'
		if (latitude < 0):
			NS = 's'
	
		EW = 'e'
		if (longitude < 0):
			EW = 'w'

		NSVal = abs(floor(latitude))
		EWVal = abs(floor(longitude))
		return "%s%02d%s%03d" % (NS, NSVal, EW, EWVal)
