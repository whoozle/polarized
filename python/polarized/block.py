from palette import Palette

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cmc

class BinaryBlock(object):
    def __init__(self, data = None, color1 = None, color2 = None):
        self.color1, self.color2 = color1, color2
        if data is None or color1 == color2:
            self.__data = [0 for _ in xrange(0, 64)]
            return

        assert len(data) == 64
        self.__data = []
        lab1 = convert_color(sRGBColor(*color1, is_upscaled = True), LabColor)
        lab2 = convert_color(sRGBColor(*color2, is_upscaled = True), LabColor)
        for rgb in data:
            rgb = sRGBColor(*rgb, is_upscaled = True)
            lab = convert_color(rgb, LabColor)
            d1 = delta_e_cmc(lab, lab1, 1, 1)
            d2 = delta_e_cmc(lab, lab2, 1, 1)
            self.__data.append(d1 / (d1 + d2))
        assert len(self.__data) == 64

    def rms(self, block):
        for c1, c2 in zip(self.__data, block.__data):
            print c1, c2

class Block(object):
    def __init__(self, data = None):
        if data is None:
            data = [(0, 0, 0) for _ in xrange(0, 64)]
        assert len(data) == 64
        self.__data = data

    def set(self, y, x, rgb):
        self.__data[y * 8 + x] = rgb

    def quantize(self, maxColors):
        p = Palette(maxColors)
        for rgb in self.__data:
            p.addColor(rgb)
        return p.quantize()

    def split(self, picker):
        color1, color2 = map(lambda c: picker.getColor(c), self.quantize(2))
        return BinaryBlock(self.__data, color1, color2)
