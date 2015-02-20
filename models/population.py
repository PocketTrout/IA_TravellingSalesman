__author__ = 'kilian.brandtdi'

import random
import copy

class Population:

    def __init__(self, listSolutions):
        self._listSolutions = listSolutions
        self._distancesSum = self.calculateDistance()


    def calculateDistance(self):
        if len(self._listSolutions) > 0:
            distanceSum = 0
            for sol in self._listSolutions:
                distanceSum += sol.getDistance()
            return distanceSum
        return 0

    def newGeneration(self):
        oldGenerationLength = len(self._listSolutions)
        numberOfElits = int(0.33 * oldGenerationLength)
        sortedList = sorted(self._listSolutions, key=lambda sol: sol.getDistance())

        newListSolutions = list()
        #fill with some elits
        newListSolutions.extend(self.selectElitism(sortedList, numberOfElits))
        #fill with roulette selection
        newListSolutions.extend([self.selectRoulette(sortedList) for i in range(oldGenerationLength - numberOfElits)])
        #replace solutions list
        self._listSolutions = sorted(newListSolutions, key=lambda sol: sol.getDistance())
        self._distancesSum = self.calculateDistance()
        #mutate some of the new population
        self.proceedMutation()
        #proceed crossing
        self.proceedCrossOver()
        #refresh distances sum
        self._distancesSum = self.calculateDistance()


    def selectRoulette(self, sortedList):
        #début de la roulette
        random.seed()
        r = random.randint(0,int(self._distancesSum))

        distanceCounter = 0
        index = 0
        for sol in reversed(sortedList):
            distanceCounter += sol.getDistance()
            if distanceCounter >= r:
                return sortedList[index]
            index += 1

    def selectElitism(self, sortedList, number):
        return copy.deepcopy(sortedList[0:number])

    def proceedMutation(self):
        r = random.randint(0,1)
        #we know list is sorted, we are going to keep the 10% bests and mute the others
        for i in range(int(len(10 * self._listSolutions) / 100),len(self._listSolutions)-1):
                self._listSolutions[i].mutate()

    def proceedCrossOver(self):
        minSumary = int(len(10 * self._listSolutions) / 100)
        maxSumary = len(self._listSolutions)-2
        for i in range(minSumary,maxSumary):
                r = random.randint(0,100)
                if r < 50:
                    s = random.randint(minSumary,maxSumary)
                    self._listSolutions[i].cross(self._listSolutions[s])

    def getBestSolution(self):
        return sorted(self._listSolutions, key=lambda sol: sol.getDistance())[0]