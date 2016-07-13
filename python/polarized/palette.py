from operator import getitem
import math

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cmc

class Palette(object):

	@staticmethod
	def stepCount(max_colors):
		n = math.trunc(math.log(max_colors, 2))
		if 2 ** n != max_colors:
			raise Exception("max colors must be power of 2")
		return n

	def __init__(self, max_colors):
		self.n = Palette.stepCount(max_colors)
		self.__colors = set()

	def addColor(self, rgb):
		self.__colors.add(rgb)

	def quantize(self):
		colors = list(self.__colors)
		palette = []
		self.__qstep(palette, colors, 0)
		return palette

	def __qstep(self, palette, colors, depth):
		colors_n = len(colors)
		if depth == self.n:
			#print "FINISHING", colors
			r, g, b = zip(*colors)
			r, g, b = sum(r) / colors_n, sum(g) / colors_n, sum(b) / colors_n
			palette.append((r, g, b))
			return
		r1, g1, b1 = 255, 255, 255
		r2, g2, b2 = 0, 0, 0
		for r, g, b in colors:
			r1, g1, b1 = min(r, r1), min(g, g1), min(b, b1)
			r2, g2, b2 = max(r, r2), max(g, g2), max(b, b2)

		dr, dg, db = r2 - r1, g2 - g1, b2 - b1
		#print "ranges: ", dr, dg, db
		dm = max(dr, dg, db)
		if dr == dm:
			plane = 0
		elif dg == dm:
			plane = 1
		else:
			plane = 2

		#print "sorting by plane", plane
		colors = sorted(colors, key = lambda x: getitem(x, plane), reverse = True)

		depth += 1
		next_1 = colors[: colors_n / 2]
		next_2 = colors[colors_n / 2:]
		self.__qstep(palette, next_1, depth)
		self.__qstep(palette, next_2, depth)

class ColorPicker(object):
	def __init__(self, palette):
		self.__colors = []
		for r, g, b in palette:
			rgb = sRGBColor(r, g, b, is_upscaled = True)
			lab = convert_color(rgb, LabColor)
			self.__colors.append((rgb, lab))

	def getColor(self, rgb):
			rgb = sRGBColor(*rgb, is_upscaled = True)
			src = convert_color(rgb, LabColor)
			match_color = None
			match_delta = None
			match_index = None
			index = 0
			for dst_rgb, dst in self.__colors:
				d = delta_e_cmc(src, dst, 1, 1)
				if (match_color is None) or (d < match_delta):
					match_index = index
					match_color = dst_rgb
					match_delta = d
				index += 1
			return match_index, match_color.get_upscaled_value_tuple()

EGA = [
	(0x00, 0x00, 0x00),
	(0x00, 0x00, 0xaa),
	(0x00, 0xaa, 0xaa),
	(0x00, 0xaa, 0xaa),

	(0xaa, 0x00, 0x00),
	(0xaa, 0x00, 0xaa),
	(0xaa, 0x55, 0x00),
	(0xaa, 0xaa, 0xaa),

	(0x55, 0x55, 0x55),
	(0x55, 0x55, 0xff),
	(0x55, 0xff, 0x55),
	(0x55, 0xff, 0xff),

	(0xff, 0x55, 0x55),
	(0xff, 0x55, 0xff),
	(0xff, 0xff, 0x55),
	(0xff, 0xff, 0xff),
]

XTERM = [
	(0x00, 0x00, 0x00),
	(0x55, 0x00, 0x00),
	(0x00, 0x55, 0x00),
	(0x55, 0x55, 0x00),

	(0x00, 0x00, 0x55),
	(0x55, 0x00, 0x55),
	(0x00, 0x55, 0x55),
	(0x55, 0x55, 0x55),

	(0x33, 0x33, 0x33),
	(0xaa, 0x00, 0x00),
	(0x00, 0xaa, 0x00),
	(0xaa, 0xaa, 0x00),

	(0x55, 0x55, 0xaa),
	(0xaa, 0x55, 0xaa),
	(0x55, 0xaa, 0xaa),
	(0xaa, 0xaa, 0xaa),
]
