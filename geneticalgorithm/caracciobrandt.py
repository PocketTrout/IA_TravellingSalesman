__author__ = "Kilian Brandt and Michael Caraccio"

import csv
import argparse
import random
import math
import time
import copy
import sys
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import pygame

# globals used for GUI drawing
screen_x = 500
screen_y = 500
window = None
screen = None
font = None
isGUIEnabled = False

# ------------------------------------------------------
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
        self._x = self.verifyCoord(x, 0, screen_x)
        self._y = self.verifyCoord(y, 0, screen_y)


    def verifyCoord(self, coord, min, max):
        """ As we know that for the lab, the max size of window is 500x500, verify is new point is correct """
        coord = coord if coord >= min else min
        coord = coord if coord <= max else max
        return coord

    def x(self):
        return self._x

    def y(self):
        return self._y

# global var center point of screen
center = Point(int(screen_x / 2), int(screen_y / 2))

#------------------------------------------------------
# CLASS : Population
#------------------------------------------------------
class Population:
    def __init__(self, listSolutions):
        self._listSolutions = listSolutions
        self._distancesSum = self.calculateDistance()

    def calculateDistance(self):
        """ return the sum of all solutions distances in the population """
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
        # mutate some of the new population
        self.proceedMutation()
        #proceed crossing
        self.proceedCrossOver()
        # some experimentation on elits
        self.elitExperiment()

        for sol in self._listSolutions:
            sol.refreshOwnDistance()

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
        for i in range(int(10 * len(self._listSolutions) / 100), len(self._listSolutions) - 1):
            self._listSolutions[i].mutate()

    def proceedCrossOver(self):
        """ CrossOver some chromosome the population with a fifty percent chance to happen.
            The 5% of elits won't be affected. """
        minSumary = int(len(5 * self._listSolutions) / 100)
        maxSumary = len(self._listSolutions) - 1
        for i in range(minSumary, maxSumary):
            r = random.randint(0, 100)
            if r < 50:
                s = random.randint(minSumary, maxSumary)
                self._listSolutions[i].cross(self._listSolutions[s])

    def elitExperiment(self):
        """ Cross the two elits solutions and replace the two worst in the population with a 20% chance to occur """
        miracle = random.randint(0, 100)
        if miracle < 20 and len(self._listSolutions) > 2:
            sortedSoluces = sorted(self._listSolutions, key=lambda sol: sol.getDistance())
            bestCopy = Solution(sortedSoluces[0].getProblem(), copy.deepcopy(sortedSoluces[0].getPath()))
            secondCopy = Solution(sortedSoluces[1].getProblem(), copy.deepcopy(sortedSoluces[1].getPath()))
            bestCopy.cross(secondCopy)
            self._listSolutions[-1] = bestCopy
            self._listSolutions[-2] = secondCopy

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

    def setFirstAndLast(self):
        """ set as first and last city in the problem, the two cities that are the closest (min distance between those two cities) """
        if len(self._cities) > 2:
            tmpDistance = 10000000  # huge value
            i = 0
            #indices of chosen cities
            chosen1 = 0
            chosen2 = 0
            for city in self._cities:
                j = 0
                for neighbours in self._cities:
                    distance = math.sqrt((neighbours.coords().x() - city.coords().x()) ** 2 + (
                    neighbours.coords().y() - city.coords().y()) ** 2)
                    if distance < tmpDistance and neighbours is not city:
                        tmpDistance = distance
                        chosen1 = i
                        chosen2 = j
                    j += 1
                i += 1
            self._cities[0], self._cities[chosen1] = self._cities[chosen1], self._cities[0]
            self._cities[-1], self._cities[chosen2] = self._cities[chosen2], self._cities[-1]


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
        # if no path is given, but a problem is
        if len(path) == 0:
            # if there is at least 3 cities in it
            if len(problem.getCities()) > 2:
                # a problem has as first and last cities the two nearest one so we shuffle only the middle of the list
                tmpList = problem.getCities()[1:-1]
                random.shuffle(tmpList)
                tmpList.insert(0, problem.getCities()[0])
                tmpList.append(problem.getCities()[-1])
                self._path = tmpList
            else:
                # else just shuffle the cities to create a new solution
                self._path = problem.getCities()
                random.shuffle(self._path)
        else:
            # else keep the given
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

    def getProblem(self):
        return self._problem

    def refreshOwnDistance(self):
        self._distance = self.evalDistancePath()

    def mutate(self):
        """ The mutation simply swap two cities and evaluate the new distance """
        nb = random.randint(1, 3)
        for i in range(0, nb):
            r1 = random.randint(0, len(self._path) - 1)
            r2 = random.randint(0, len(self._path) - 1)
            self._path[r1], self._path[r2] = self._path[r2], self._path[r1]


    def fillPartByCrossing(self, firstPart, secondPart):
        actualListSize = len(firstPart)

        for i in range(0, len(secondPart)):
            # we append all missing element of the solution (cities that aren't yet in the first part)
            # sorted by a function that consider distance to center and distance to the last city of the first part
            # of course there is a part of random, the only cond is that distance to next city have a bigger weight in decision
            a = random.randint(5, 10)
            b = random.randint(15, 20)
            secondPart = sorted(secondPart,
                                key=lambda city: -a * self.distanceBetweenPoints(city.coords(),
                                                                                 center) + b * self.distanceBetweenPoints(
                                    firstPart[actualListSize - 1].coords(), city.coords()))
            firstPart.append(secondPart[0])
            del secondPart[0]
            actualListSize += 1
        return firstPart

    def cross(self, solution):
        """ Cross two solutions to generate new one """
        size = self.getSize()
        # cross only if the two solutions have the same size and the size is bigger than 2
        if size == solution.getSize() and size > 3:
            # cut each solution into two parts that will become the first parts of the two new solutions
            startCityIndex = random.randint(2, size - 2)
            firstPartSelf = self._path[0:startCityIndex - 1]
            firstPartOther = solution._path[startCityIndex:size - 1]
            copySelf = self._path[:]
            copyOther = solution._path[:]
            # build list with the unique elements that aren't not yet in the first part of future solution
            secondPartSelf = [x for x in copyOther if x not in firstPartSelf]
            secondPartOther = [x for x in copySelf if x not in firstPartOther]
            sizeSecondPartSelf = len(secondPartSelf)
            sizeSecondPartOther = len(secondPartOther)

            # if sizes are bigger tha 0
            if sizeSecondPartSelf > 0 and sizeSecondPartOther > 0:
                # call filling algorithm with both parts of each future solutions we built before
                newPathSelf = self.fillPartByCrossing(firstPartSelf, secondPartSelf)
                newPathOther = self.fillPartByCrossing(firstPartOther, secondPartOther)
            else:
                # else create a totally random new solution
                newPathSelf = random.shuffle(self._problem.getCities())
                newPathOther = random.shuffle(solution._problem.getCities())

            self._path = newPathSelf
            solution._path = newPathOther

    def addNextCity(self, city):
        if city not in self._path:
            self._path.append(city)

    def displayPath(self):
        """ print the path in console """
        for city in self._path:
            print(city)

    def distanceBetweenPoints(self, p1, p2):
        """ return the distance between two given points """
        return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)

    def getDistance(self):
        return self._distance

    def getSize(self):
        return len(self._path)


#------------------------------------------------------
# Methodes de resolution
#------------------------------------------------------
def ga_solve(file=None, gui=True, maxtime=0, cities=list()):
    """ Solve the travelling salesman problem using a genetic algorithm """
    initializationTime = -time.time()
    citiesList = []
    # choose the right data input
    if file != None:
        # Import cities from file
        file_import = File(file)
        # put cities in a list
        citiesList = file_import.from_file()
    elif len(cities) > 0:
        citiesList = cities
    else:
        print("No data input !")
        return

    random.seed()
    # create a problem from the cities
    problem = Problem(citiesList)
    problem.setFirstAndLast()


    # Generate the initial population with a size random size between 60 and 80
    popSize = random.randint(60, 80)
    initialPopulation = generateInitialPopulation(problem, popSize)

    # if the GUI is enabled
    if isGUIEnabled:
        # ask the best solution for drawing it
        sol = initialPopulation.getBestSolution()
        draw(sol)
        # Refresh
        pygame.display.flip()

    initializationTime += time.time()
    totalTime = initializationTime
    averageIterationTime = 0

    # start the algorithm
    i = 0
    sameResultsCounter = 0
    lastResult = 0
    # here is a list that will save the lasts results given to calculate an average and stop looping if no improvement is detected
    while sameResultsCounter < 100 and (maxtime == 0 or ((totalTime + averageIterationTime) <= float(maxtime))):
        startTime = time.time()
        initialPopulation.newGeneration()
        sol = initialPopulation.getBestSolution()
        result = sol.getDistance()

        # if the best solution is still the same
        if result == lastResult:
            sameResultsCounter += 1  # increment counter
        else:
            sameResultsCounter = 0
            # Display the new best solution (cities) on screen
            draw(sol)

        i += 1
        lastResult = result  # save the result
        endTime = time.time()
        lastIterationTime = endTime - startTime
        averageIterationTime = (averageIterationTime * (i - 1) + lastIterationTime) / i  # update average time
        totalTime += lastIterationTime  # increment time counter

    bestSolution = initialPopulation.getBestSolution()
    return bestSolution.getDistance(), [city.name() for city in bestSolution.getPath()]


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

    return Population(listSolutions)


#------------------------------------------------------
# GUI methods
#------------------------------------------------------

def initGUI():
    """ Init the window """
    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Travelling Salesman')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    return window, screen, font, True


def draw(item):
    """
    Draw a path on the GUI
    :param item: Can be a list of cities or a solution object
    """
    if isGUIEnabled:
        listCities = []
        if type(item) is Solution:
            listCities = item.getPath()
        else:
            listCities = item

        screen.fill(0)
        pointlist = []
        # We draw each city on screen
        city_color, text_color = [0, 255, 0]  # Green
        city_radius = 5

        for city in listCities:
            pos = city.coords()
            # Points array for drawing lines between cities
            pointlist.append((pos.x(), pos.y()))
            pygame.draw.circle(screen, city_color, (pos.x(), pos.y()), city_radius)
            # Create the label with the name of the city
            label = font.render(city.name(), 1, text_color, None)
            # Draw the label
            screen.blit(label, (pos.x() + 10, pos.y() - 6))

        # Don't forget to set the first element as the last too (close the loop)
        if len(pointlist) > 0:
            pointlist.append((pointlist[0]))
            # Draw the lines between cities
            pygame.draw.lines(screen, 0xffffff, False, [p for p in pointlist], 2)

        #draw the number of cities
        font_color = [255, 255, 255]  # white
        text = font.render("Number: %i" % len(listCities), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()


def drawEndMessage():
    if isGUIEnabled:
        #draw the number of cities
        font_color = [150, 40, 200]  # violet
        text = font.render("Solving complete !", True, font_color)
        textRect = text.get_rect(centerx=screen.get_width() / 2, centery=screen.get_height() / 2)
        screen.blit(text, textRect)
        pygame.display.flip()


if __name__ == "__main__":

    # ----------------------------------------------
    # Parse the command line given parameters
    # ----------------------------------------------
    parser = argparse.ArgumentParser(description='Example with long option names')
    parser.add_argument('filename', type=argparse.FileType('r'),
                        help="The file that contains cities",
                        nargs="?")
    parser.add_argument('--nogui', action='store_const', dest='gui',
                        const='1',
                        help='Disable the GUI')
    parser.add_argument('--maxtime', action='store', dest='maxtime', type=int,
                        help='Set the maximum execution time')

    # get all parameters
    args = parser.parse_args()

    # initialize with default values
    parameterMaxtime = 0
    parameterGui = True
    collecting = False

    if args.maxtime != None:
        parameterMaxtime = args.maxtime

    if args.gui != None:
        parameterGui = False

    if args.filename == None:
        filename = None
        collecting = True
    else:
        filename = args.filename.name

    # -------------------------------
    # Initialisation de la GUI
    # -------------------------------
    if parameterGui:
        window, screen, font, isGUIEnabled = initGUI()

    # if no file given and gui enabled, ask points to user with mouse selection
    cities = []
    counter = 0
    while collecting and isGUIEnabled:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                cities.append(City(Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), "V%d" % counter))
                counter += 1
                draw(cities)

    # call the solving method
    try:
        distance, path = ga_solve(filename, parameterGui, float(parameterMaxtime), cities)
        if isGUIEnabled:
            drawEndMessage()
        print("Solution found : %f" % distance)
    except TypeError:
        print("Cannot solve this problem, an error occured !")

    # loop to handle quit event or keyboard keydown event (interrupt and quit)
    while isGUIEnabled:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == KEYDOWN:
            pygame.quit()
            break