from models.city import City

__author__ = 'kilian.brandtdi'

from models.city import City
from models.solution import Solution
from models.point import Point
from models.problem import Problem

#TODO write solve function
def ga_solve(file=None, gui=True, maxtime=0):
    return 0


if __name__ == "__main__":
    city1 = City(Point(2,3),"1")
    city2 = City(Point(3,4),"2")
    city3 = City(Point(5,6),"3")
    problem = Problem([city1,city2,city3])
    soluce = Solution(problem)
    soluce.addNextCity(city1)
    soluce.addNextCity(city2)
    soluce.addNextCity(city3)
    soluce.addNextCity(city3)
    soluce.displayPath()