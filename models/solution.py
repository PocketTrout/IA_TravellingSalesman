__author__ = "Kilian Brandt and Michael Caraccio"

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


    # Calcule toutes les distances possible entre les villes
    def evalDistancePath(self):
        distance = 0
        if self._problem.getSize() > 0:
            for i in range(-1,self._problem.getSize()-1):
                distance += self.distanceBetweenPoints(self._path[i].coords(),self._path[i+1].coords())

        return distance


    def mutate(self):
        #la mutation se charge simplement d'échanger deux villes au hasard qui peuvent être les mêmes (sans effet)
        r1 = random.randint(0,len(self._path)-1)
        r2 = random.randint(0,len(self._path)-1)
        self._path[r1] , self._path[r2] = self._path[r2] , self._path[r1]

        self._distance = self.evalDistancePath()

    def cross(self,solution):
        size = self.getSize()
        if size == solution.getSize() and size > 2:
            startCityIndex = random.randint(2,size-2)
            firstPartSelf = self._path[0:startCityIndex-1]
            firstPartOther = solution._path[startCityIndex:size-1]
            copySelf = self._path[:]
            copyOther = solution._path[:]
            secondPartSelf = [x for x in copyOther if x not in firstPartSelf]
            secondPartOther = [x for x in copySelf if x not in firstPartOther]
            sizeSecondPartSelf = len(secondPartSelf)
            sizeSecondPartOther = len(secondPartOther)

            if sizeSecondPartSelf > 0 and sizeSecondPartOther > 0:
                actualListSize = len(firstPartSelf)
                for i in range(0,len(secondPartSelf)):
                    secondPartSelf = sorted(secondPartSelf, key=lambda city: self.distanceBetweenPoints(firstPartSelf[actualListSize - 1].coords(), city.coords()))
                    firstPartSelf.append(secondPartSelf[0])
                    del secondPartSelf[0]
                    actualListSize += 1

                actualListSize = len(firstPartOther)
                for i in range(0,len(secondPartOther)):
                    secondPartOther = sorted(secondPartOther, key=lambda city: self.distanceBetweenPoints(firstPartOther[actualListSize - 1].coords(), city.coords()))
                    firstPartOther.append(secondPartOther[0])
                    del secondPartOther[0]
                    actualListSize += 1

            self._path = firstPartSelf
            solution._path = firstPartOther

    def getDistancesToCitiesList(self,city, others):
        if len(others) > 0:
            result = list()
            for neighbour in others:
                result.append([self.distanceBetweenPoints(city.coords(),neighbour.coords()),neighbour])

            return sorted(result, key=lambda dist: dist[0])

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


    def getSize(self):
        return len(self._path)