class Palette(object):
	def __init__(self, max_colors):
		self.n = max_colors
		self.colors = set()

	def add_color(self, rgb):
		self.colors.add(rgb)

	def quantize(self):
		print "colors:", len(self.colors)
