class Block(object):
    def __init__(self, data = None):
        if data is None:
            data = [(0, 0, 0) for _ in xrange(0, 64)]
        assert len(data) == 64
        self.__data = data

    def set(self, y, x, rgb):
        self.__data[y * 8 + x] = rgb
