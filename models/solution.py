__author__ = 'kilian.brandtdi'

import random
import math

class Solution:

    def __init__(self, problem, path = list()):
        self._problem = problem
        if len(path) == 0:
            self._path = problem.getCities()
            random.shuffle(self._path)
        else:
            self._path = path
        self._distance = self.evalDistancePath()

    def clone(self):
        return Solution(self._problem,self._path)


    # Calcule toutes les distances possible entre les villes
    def evalDistancePath(self):
        distance = 0
        if self._problem.getSize() > 0:
            for i in range(-1,self._problem.getSize()-1):
                distance += self.distanceBetweenPoints(self._path[i].coords(),self._path[i+1].coords())

        return distance


    def mutate(self):
        #la mutation se charge simplement d'échanger deux villes au hasard
        r1 = random.randint(0,len(self._path)-1)
        r2 = random.randint(0,len(self._path)-1)
        self._path[r1] , self._path[r2] = self._path[r2] , self._path[r1]

        self._distance = self.evalDistancePath()


    def cross(self,solution):
        return 1

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