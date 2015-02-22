__author__ = "Kilian Brandt and Michael Caraccio"

class City:

    def __init__(self, point, name):
        self._coords = point
        self._name = name

    def __eq__(self, other):
        return self._coords.x() == other.coords().x() and self._coords.y() == other.coords().y()

    def __hash__(self):
        return hash((self.coords(), self._name))

    def __str__(self):
        return "%s at coordinates (%d, %d)" % (self._name, self._coords.x(), self._coords.y())

    def coords(self):
        return self._coords

    def name(self):
        return self._name