__author__ = "Kilian Brandt and Michael Caraccio"

#------------------------------------------------------
# CLASS : City
#------------------------------------------------------
class City:
    def __init__(self, point, name):
        self._coords = point
        self._name = name

    def __eq__(self, other):
        return self._coords.x() == other.coords().x() and self._coords.y() == other.coords().y()

    def __hash__(self):
        return hash((self.coords(), self._name))

    def __str__(self):
        return "%s at coordinates (%d, %d)" % (self._name, self._coords.x(), self._coords.y())

    def coords(self):
        return self._coords

    def name(self):
        return self._name

#------------------------------------------------------
# CLASS : File
#------------------------------------------------------
class File:
    def __init__(self, path):
        self._path = path

    def from_file(self):
        citylist = []
        with open(self._path) as f:
            reader = csv.reader(f, delimiter=" ")
            d = list(reader)

        for number in d:
            # print(" %s | %s | %s" % (number[0], number[1], number[2]))
            citylist.append(City(Point(int(number[1]), int(number[2])), number[0]))

        return citylist

#------------------------------------------------------
# CLASS : Point
#------------------------------------------------------
class Point:
    def __init__(self, x, y):
        self._x = self.verifyCoord(x)
        self._y = self.verifyCoord(y)


    def verifyCoord(self, coord):
        coord = coord if coord >= 0 else 0
        coord = coord if coord <= 500 else 500
        return coord

    def x(self):
        return self._x

    def y(self):
        return self._y

#------------------------------------------------------
# CLASS : Population
#------------------------------------------------------
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
        """ create a new generation of solution from the old one with elitism, mutation and crossover"""
        oldGenerationLength = len(self._listSolutions)
        # calculate the number of elits solution that we want to keep (33%)
        numberOfElits = int(0.33 * oldGenerationLength)
        sortedList = sorted(self._listSolutions, key=lambda sol: sol.getDistance())
        newListSolutions = list()
        # fill with some elits
        newListSolutions.extend(self.selectElitism(sortedList, numberOfElits))
        # fill with roulette selection
        newListSolutions.extend([self.selectRoulette(sortedList) for i in range(oldGenerationLength - numberOfElits)])
        # replace solutions list
        self._listSolutions = sorted(newListSolutions, key=lambda sol: sol.getDistance())
        self._distancesSum = self.calculateDistance()
        # mutate some of the new population
        self.proceedMutation()
        #proceed crossing
        self.proceedCrossOver()
        # refresh distances sum
        self._distancesSum = self.calculateDistance()


    def selectRoulette(self, sortedList):
        """ Roulette selection """
        random.seed()
        # get a random number between 0 and the total distance of solution
        r = random.randint(0, int(self._distancesSum))

        # initialize distance counter and index
        distanceCounter = 0
        index = 0
        # we iterate on the reversed list cause the longest distance is the worst solution
        # we want the best solution to have a bigger probability to be chosed so we add the longgest distance first
        # and use an index var to choose the city
        for sol in reversed(sortedList):
            distanceCounter += sol.getDistance()
            if distanceCounter >= r:
                return sortedList[index]
            index += 1

    def selectElitism(self, sortedList, number):
        """ return a list that contains a given number of the best solutions """
        return copy.deepcopy(sortedList[0:number])

    def proceedMutation(self):
        """ Mutate some chromosome. We know list is sorted,
            we are going to keep the 10% bests and mutate the others """
        for i in range(int(len(10 * self._listSolutions) / 100), len(self._listSolutions) - 1):
            self._listSolutions[i].mutate()

    def proceedCrossOver(self):
        """ CrossOver some chromosome the population with a fifty percent chance to happen.
            The 10% of elits won't be affected. """
        minSumary = int(len(10 * self._listSolutions) / 100)
        maxSumary = len(self._listSolutions) - 2
        for i in range(minSumary, maxSumary):
            r = random.randint(0, 100)
            if r < 50:
                s = random.randint(minSumary, maxSumary)
                self._listSolutions[i].cross(self._listSolutions[s])

    def getBestSolution(self):
        """ return the best solution of the population. """
        return sorted(self._listSolutions, key=lambda sol: sol.getDistance())[0]

#------------------------------------------------------
# CLASS : Problem
#------------------------------------------------------
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

#------------------------------------------------------
# CLASS : Solution
#------------------------------------------------------
class Solution:
    def __init__(self, problem, path=list()):
        self._problem = problem
        if len(path) == 0:
            self._path = problem.getCities()
            random.shuffle(self._path)
        else:
            self._path = path
        self._distance = self.evalDistancePath()

    def evalDistancePath(self):
        """ Calculate the total path distance (sum of all distances between cities """
        distance = 0
        if self._problem.getSize() > 0:
            # starts from -1 cause we have to close the loop (distance between the first and the last city
            for i in range(-1, self._problem.getSize() - 1):
                distance += self.distanceBetweenPoints(self._path[i].coords(), self._path[i + 1].coords())

        return distance

    def getPath(self):
        return self._path


    def mutate(self):
        """ The mutation simply swap two cities and evaluate the new distance """
        r1 = random.randint(0, len(self._path) - 1)
        r2 = random.randint(0, len(self._path) - 1)
        self._path[r1], self._path[r2] = self._path[r2], self._path[r1]

        self._distance = self.evalDistancePath()

    def cross(self, solution):
        """ Cross two solutions to generate new one """
        size = self.getSize()
        if size == solution.getSize() and size > 2:
            startCityIndex = random.randint(2, size - 2)
            firstPartSelf = self._path[0:startCityIndex - 1]
            firstPartOther = solution._path[startCityIndex:size - 1]
            copySelf = self._path[:None]
            copyOther = solution._path[:None]
            secondPartSelf = [x for x in copyOther if x not in firstPartSelf]
            secondPartOther = [x for x in copySelf if x not in firstPartOther]
            sizeSecondPartSelf = len(secondPartSelf)
            sizeSecondPartOther = len(secondPartOther)

            if sizeSecondPartSelf > 0 and sizeSecondPartOther > 0:
                actualListSize = len(firstPartSelf)
                for i in range(0, len(secondPartSelf)):
                    secondPartSelf = sorted(secondPartSelf, key=lambda city: self.distanceBetweenPoints(
                        firstPartSelf[actualListSize - 1].coords(), city.coords()))
                    firstPartSelf.append(secondPartSelf[0])
                    del secondPartSelf[0]
                    actualListSize += 1

                actualListSize = len(firstPartOther)
                for i in range(0, len(secondPartOther)):
                    secondPartOther = sorted(secondPartOther, key=lambda city: self.distanceBetweenPoints(
                        firstPartOther[actualListSize - 1].coords(), city.coords()))
                    firstPartOther.append(secondPartOther[0])
                    del secondPartOther[0]
                    actualListSize += 1

            self._path = firstPartSelf
            solution._path = firstPartOther

    def getDistancesToCitiesList(self, city, others):
        if len(others) > 0:
            result = list()
            for neighbour in others:
                result.append([self.distanceBetweenPoints(city.coords(), neighbour.coords()), neighbour])

            return sorted(result, key=lambda dist: dist[0])

    def addNextCity(self, city):
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


#------------------------------------------------------
# Methodes de resolution
#------------------------------------------------------
def ga_solve(file=None, gui=True, maxtime=0):
    # Import cities from file
    file_import = File(file)
    # put cities in a list
    citiesFromFile = file_import.from_file()
    # create a problem from the cities
    problem = Problem(citiesFromFile)
    initializationTime = -time.time()

    # Generate the initial population with a size of 60 from the problem
    initialPopulation = generateInitialPopulation(problem, 60)
    initializationTime += time.time()

    totalTime = initializationTime
    averageIterationTime = 0

    # ask the best solution for drawing it
    sol = initialPopulation.getBestSolution()
    # Ask to draw all the cities on GUI
    draw(sol._path)

    # Refresh
    pygame.display.flip()

    # start the algorithm
    i = 0
    lastResult = 0
    # here is a list that will save the lasts results given to calculate an average and stop looping if no improvement is detected
    while i < 100 and (maxtime == 0 or (totalTime + averageIterationTime) <= float(maxtime) * 1.03):  #we add 3% to maxtime because we can pass time by 5% maximum
        startTime = time.time()
        initialPopulation.newGeneration()

        sol = initialPopulation.getBestSolution()
        result = sol.getDistance()

        # Display the solution (cities) on screen
        draw(sol.getPath())

        # Refresh
        pygame.display.flip()

        if result == lastResult:
            i += 1
        else:
            i = 0

        lastResult = result
        endTime = time.time()
        lastIterationTime = endTime - startTime
        averageIterationTime = (averageIterationTime * (i - 1) + lastIterationTime) / i
        totalTime += lastIterationTime

    print("Solution found, distance: %f" % initialPopulation.getBestSolution().getDistance())
    print("Execution time: %f s" % totalTime)


def calculateAverage(list):
    """ Calculate the average value from a list """
    size = len(list)
    if size > 0:
        sum = 0
        for i in range(0, size):
            sum += list[i]

        return sum / size
    return 0


def generateInitialPopulation(problem, size):
    """ Create an initial population from a problem with a given size """
    listSolutions = []
    for i in range(size):
        listSolutions.append(Solution(problem))

    listSolutions[0].cross(listSolutions[1])
    return Population(listSolutions)

#------------------------------------------------------
# GUI methods
#------------------------------------------------------
def initScreen():

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Travelling Salesman')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    return screen, window, font

def draw(solution):
    screen.fill(0)
    citylist = solution
    pointlist = []

    # We draw each city on screen
    for city in citylist:
        pos = city.coords()

        # Points array for drawing lines between cities
        pointlist.append((pos.x(), pos.y()))

        pygame.draw.circle(screen, city_color, (pos.x(), pos.y()), city_radius)
        myfont = pygame.font.Font(None, 20)

        # Create the label with the name of the city
        label = myfont.render(city.name(), 1, text_color, None)

        # Draw the label
        screen.blit(label, (pos.x() + 10, pos.y() - 6))


    # Don't forget to set the first element as the last too (close the loop)
    pointlist.append((pointlist[0]))

     # Draw the lines between cities
    pygame.draw.lines(screen, 0xffffffff, False, [p for p in pointlist], 2)

    text = font.render("Number: %i" % len(solution), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


if __name__ == "__main__":

    import argparse
    import csv
    import random
    import math
    import time
    import copy
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
    import pygame

    # ----------------------------------------------
    # Parse the command line given parameters
    # ----------------------------------------------
    parser = argparse.ArgumentParser(description='Example with long option names')

    parser.add_argument('filename', type=argparse.FileType('r'))

    parser.add_argument('--nogui', action='store_const', dest='gui',
                        const='1',
                        help='Disable the GUI')

    parser.add_argument('--maxtime', action='store', dest='maxtime',
                        help='Set the maximum execution time')

    # get all parameters
    args = parser.parse_args()

    # initialize with default values
    parameterMaxtime = 0
    parameterGui = True

    if args.maxtime != None:
        parameterMaxtime = args.maxtime

    if args.gui != None:
        parameterGui = False

    # -------------------------------
    # Initialisation de la GUI
    # -------------------------------
    # Some defaults parameters
    screen_x = 500
    screen_y = 500
    city_color = [0, 255, 0]  # Green
    text_color = [0, 255, 0]  # Green
    city_radius = 5
    font_color = [255, 255, 255]  # white

    # initialize the screen, window and font
    screen, window, font = initScreen()

    # call the solving method
    ga_solve(args.filename.name, parameterGui, parameterMaxtime)

    # loop to handle quit event or keyboard keydown event (interrupt and quit)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == KEYDOWN:
            pygame.quit()
            break