__author__ = 'kilian.brandtdi'

from models.city import City
from models.solution import Solution
from models.point import Point
from models.problem import Problem
from models.file import File


#TODO write solve function
def ga_solve(file=None, gui=True, maxtime=0):
    return 0

if __name__ == "__main__":
    city1 = City(Point(2, 3), "1")
    city2 = City(Point(3, 4), "2")
    city3 = City(Point(5, 6), "3")
    problem = Problem([city1, city2, city3])
    soluce = Solution(problem)
    soluce.addNextCity(city1)
    soluce.addNextCity(city2)
    soluce.addNextCity(city3)
    soluce.addNextCity(city3)
    soluce.displayPath()

    # Tentative de résolution en utilisant le fichier

    # Importation des villes depuis un fichier
    file_import = File("../extern/pb010.txt")

    # Stockage des villes dans une liste
    citiesFromFile = []
    citiesFromFile = file_import.from_file()

    # Evaluation des distances entre villes pour trouver le meilleur individu (celui qui a la distance la plus
    # petite entre 2 villes
    
    list_length = soluce.length_evaluation(citiesFromFile)
    meilleur_individu = list_length[0]
    print(meilleur_individu)
