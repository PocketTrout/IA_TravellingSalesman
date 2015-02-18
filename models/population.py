__author__ = 'kilian.brandtdi'

from models.solution import Solution


class Population:

    def __init__(self, listSolutions):
        self._listSolutions = listSolutions

    def newGeneration(self):
        oldGenerationLength = len(self._listSolutions)
        numberOfElits = int(0.33 * oldGenerationLength)
        sortedList = sorted(self._listSolutions, key=lambda sol: sol.getDistance())
        newListSolutions = []
        newListSolutions.append(self.selectElitism(sortedList, numberOfElits))
        #newListSolutions.append(self.selectRoulette(sortedList, oldGenerationLength - numberOfElits))
        self.selectRoulette(sortedList)


    def selectRoulette(self, sortedList):
        meanDistance = 0
        maxDistanceSol = sortedList[-1]
        maxDistance = maxDistanceSol.getDistance()
        distanceSum = 0
        for sol in sortedList:
            distanceSum += sol.getDistance()
        print(distanceSum)
        distanceSum =0
        for sol in sortedList:
            distanceSum += maxDistance - sol.getDistance()

        print(distanceSum)



    def selectElitism(self, sortedList, number):
        return sortedList[0:number]
