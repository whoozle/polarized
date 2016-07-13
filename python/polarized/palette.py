from operator import getitem

class Palette(object):
	def __init__(self, max_colors):
		self.n = max_colors
		self.colors = set()

	def add_color(self, rgb):
		self.colors.add(rgb)

	def quantize(self):
		colors = list(self.colors)
		self.__qstep(colors)

	def __qstep(self, colors):
		colors_n = len(colors)
		print "colors:", colors_n
		r1, g1, b1 = 255, 255, 255
		r2, g2, b2 = 0, 0, 0
		for r, g, b in self.colors:
			r1, g1, b1 = min(r, r1), min(g, g1), min(b, b1)
			r2, g2, b2 = max(r, r2), max(g, g2), max(b, b2)

		dr, dg, db = r2 - r1, g2 - g1, b2 - b1
		dm = max(dr, dg, db)
		if dr == dm:
			plane = 0
		elif dg == dm:
			plane = 1
		else:
			plane = 2

		print "sorting by plane", plane
		colors = sorted(colors, key = lambda x: getitem(x, plane), reverse = True)

		next_1 = colors[: colors_n / 2]
		next_2 = colors[colors_n / 2:]
