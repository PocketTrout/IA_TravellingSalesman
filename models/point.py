__author__ = 'kilian.brandtdi'

class Point:

    def __init__(self, x, y):
        self._x = self.verifyCoord(x)
        self._y = self.verifyCoord(y)


    def verifyCoord(self, coord):
        coord = coord if coord >= 0 else 0
        coord = coord if coord <= 500 else 500
        return coord

    def x(self):
        return self._x

    def y(self):
        return self._y