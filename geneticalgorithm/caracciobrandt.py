__author__ = 'kilian.brandtdi'

from models.city import City
from models.solution import Solution
from models.point import Point
from models.problem import Problem
from models.population import Population
from models.file import File


#TODO write solve function
def ga_solve(file=None, gui=True, maxtime=0):
    return 0


def generateInitialPopulation(problem, size):
    listSolutions = []
    for i in range(size):
        listSolutions.append(Solution(problem))

    return Population(listSolutions)


if __name__ == "__main__":
    city1 = City(Point(2, 3), "1")
    city2 = City(Point(3, 4), "2")
    city3 = City(Point(5, 6), "3")
    problem = Problem([city1, city2, city3])
    soluce = Solution(problem)
    soluce.displayPath()

    # Tentative de résolution en utilisant le fichier

    # Importation des villes depuis un fichier
    file_import = File("../extern/pb010.txt")

    # Stockage des villes dans une liste
    citiesFromFile = []
    citiesFromFile = file_import.from_file()
    problem = Problem(citiesFromFile)
    initialPopulation = generateInitialPopulation(problem, 10)
    initialPopulation.newGeneration()

    # Il faut mnt finir la roulette en inversant dans le tableau l'élément séléctionner