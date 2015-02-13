__author__ = 'kilian.brandtdi'

from models.point import Point
from models.city import City

import math

#TODO write class
class Solution:

    def __init__(self, problem):
        self._problem = problem
        self._path = []

    # Calcul toutes les distances possible entre les villes
    def length_evaluation(self, list_points):

        all_distances = []

        for x in list_points:
            for y in list_points:
                if x.name() != y.name():
                    two_cities_distance = (x.name(), y.name(), self.length(x.coords(), y.coords()))
                    all_distances.append(two_cities_distance)

        # Je les tries de la plus petite distance à la plus grande
        all_distances = sorted(all_distances, key=lambda student: student[2])

        #print(all_distances)
        return all_distances

    def mutate(self,solution):
        a = 0

    def get_dist_key(self, x):
        return x[2]

    def addNextCity(self,city):
        if city not in self._path:
            self._path.append(city)

    def displayPath(self):
        for city in self._path:
            print(city)

    def length(self, p1, p2):
        return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)