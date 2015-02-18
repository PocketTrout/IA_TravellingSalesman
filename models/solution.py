__author__ = 'kilian.brandtdi'

from models.point import Point
from models.city import City
from models.problem import Problem

import random

import math

class Solution:

    def __init__(self, problem):
        self._problem = problem
        self._path = problem.getCities()
        random.shuffle(self._path)
        self._distance = self.evalDistancePath()

    # Calcul toutes les distances possible entre les villes
    def evalDistancePath(self):
        distance = 0
        if self._problem.getSize() > 0:
            for i in range(-1,self._problem.getSize()-1):
                distance += self.distanceBetweenPoints(self._path[i].coords(),self._path[i+1].coords())

        return distance


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

    def distanceBetweenPoints(self, p1, p2):
        return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)

    def getDistance(self):
        return self._distance

    def sortedList(self):
        return sorted(self._problem, key=lambda sol: self._path[2])