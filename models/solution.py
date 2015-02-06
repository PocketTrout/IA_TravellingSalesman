__author__ = 'kilian.brandtdi'

#TODO write class
class Solution:

    def __init__(self, problem):
        self._problem = problem
        self._path = []


    def mutate(self,solution):
        a = 0

    def addNextCity(self,city):
        if city not in self._path:
            self._path.append(city)

    def displayPath(self):
        for city in self._path:
            print(city)