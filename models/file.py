__author__ = "Kilian Brandt and Michael Caraccio"

import csv

from models.city import City
from models.point import Point

class File:

    def __init__(self, path):
       self._path = path

    def from_file(self):
        citylist = []
        with open(self._path) as f:
            reader = csv.reader(f, delimiter=" ")
            d = list(reader)

        for number in d:
            #print(" %s | %s | %s" % (number[0], number[1], number[2]))
            citylist.append(City(Point(int(number[1]), int(number[2])), number[0]))

        return citylist


