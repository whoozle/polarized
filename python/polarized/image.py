from block import Block

class Image(object):
    def __init__(self, w, h):
        self.width, self.height = w, h
        self.bw, self.bh = (w + 7) / 8, (h + 7) / 8
        self.__blocks = []
        for i in xrange(0, self.bw * self.bh):
            self.__blocks.append(Block())