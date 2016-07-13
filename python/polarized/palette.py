from operator import getitem
import math

class Palette(object):
	def __init__(self, max_colors):
		self.n = math.trunc(math.log(max_colors, 2))
		if 2 ** self.n != max_colors:
			raise Exception("max colors must be power of 2")
		self.__colors = set()

	def add_color(self, rgb):
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
