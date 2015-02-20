__author__ = 'kilian.brandtdi'

from models.solution import Solution
from models.problem import Problem
from models.population import Population
from models.file import File
import time
import math


#TODO write solve function
def ga_solve(file=None, gui=True, maxtime=0):
    # Importation des villes depuis un fichier
    file_import = File(file)
    # Stockage des villes dans une liste
    citiesFromFile = file_import.from_file()
    problem = Problem(citiesFromFile)
    initializationTime = -time.time()
    initialPopulation = generateInitialPopulation(problem, 60)
    initializationTime += time.time()
    i = 0
    lastResults = [0,0,0,0,0,0,0,0,0,0]
    totalTime = initializationTime;
    averageIterationTime = 0
    while i < 50000 and (totalTime + averageIterationTime) <= maxtime*1.03: #we add 3% to maxtime because we can pass time by 5% maximum
        startTime = time.time()
        initialPopulation.newGeneration()
        result = initialPopulation.getBestSolution().getDistance()
        lastResults[i%10] = result
        if i >= 10:
             averageLastResult = calculateAverage(lastResults)
             if math.fabs(result - averageLastResult) < 1:
                 break
        i += 1

        endTime = time.time()
        lastIterationTime = endTime - startTime
        averageIterationTime = (averageIterationTime * (i - 1) + lastIterationTime) / i
        totalTime += lastIterationTime


    print("Solution trouvée, distance: %f"%initialPopulation.getBestSolution().getDistance())
    print("Temps d'exécution: %f s"%totalTime)


def calculateAverage(list):
    size = len(list)
    if size > 0:
        sum = 0
        for i in range(0,size):
            sum += list[i]

        return sum / size
    return 0

def generateInitialPopulation(problem, size):
    listSolutions = []
    for i in range(size):
        listSolutions.append(Solution(problem))

    listSolutions[0].cross(listSolutions[1])
    return Population(listSolutions)


if __name__ == "__main__":
    ga_solve("../extern/pb010.txt",False,10)