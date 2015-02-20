__author__ = 'kilian.brandtdi'

class Problem:
    def __init__(self, cities):
        if type(cities) is list:
            self._cities = cities
        else:
            self._cities = [].extend(cities)

    def addCities(self, cities):
        self._cities.append(cities)

    def getSize(self):
        return len(self._cities)

    def getCities(self):
        return self._cities