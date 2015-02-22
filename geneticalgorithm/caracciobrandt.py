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
        oldGenerationLength = len(self._listSolutions)
        numberOfElits = int(0.33 * oldGenerationLength)
        sortedList = sorted(self._listSolutions, key=lambda sol: sol.getDistance())

        newListSolutions = list()
        # fill with some elits
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
        # début de la roulette
        random.seed()
        r = random.randint(0, int(self._distancesSum))

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
        # we know list is sorted, we are going to keep the 10% bests and mute the others
        for i in range(int(len(10 * self._listSolutions) / 100), len(self._listSolutions) - 1):
            self._listSolutions[i].mutate()

    def proceedCrossOver(self):
        minSumary = int(len(10 * self._listSolutions) / 100)
        maxSumary = len(self._listSolutions) - 2
        for i in range(minSumary, maxSumary):
            r = random.randint(0, 100)
            if r < 50:
                s = random.randint(minSumary, maxSumary)
                self._listSolutions[i].cross(self._listSolutions[s])

    def getBestSolution(self):
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


    # Calcule toutes les distances possible entre les villes
    def evalDistancePath(self):
        distance = 0
        if self._problem.getSize() > 0:
            for i in range(-1, self._problem.getSize() - 1):
                distance += self.distanceBetweenPoints(self._path[i].coords(), self._path[i + 1].coords())

        return distance


    def mutate(self):
        # la mutation se charge simplement d'échanger deux villes au hasard qui peuvent être les mêmes (sans effet)
        r1 = random.randint(0, len(self._path) - 1)
        r2 = random.randint(0, len(self._path) - 1)
        self._path[r1], self._path[r2] = self._path[r2], self._path[r1]

        self._distance = self.evalDistancePath()

    def cross(self, solution):
        size = self.getSize()
        if size == solution.getSize() and size > 2:
            startCityIndex = random.randint(2, size - 2)
            firstPartSelf = self._path[0:startCityIndex - 1]
            firstPartOther = solution._path[startCityIndex:size - 1]
            copySelf = self._path[:]
            copyOther = solution._path[:]
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
# Methodes de résolution
#------------------------------------------------------
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
    lastResults = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    totalTime = initializationTime
    averageIterationTime = 0

    sol = initialPopulation.getBestSolution()
    # Demande d'affichage de toutes les villes sur l'écran
    draw(sol._path)

    # Refresh de l'écran
    pygame.display.flip()

    while i < 50000 and (totalTime + averageIterationTime) <= float(maxtime) * 1.03:  #we add 3% to maxtime because we can pass time by 5% maximum
        startTime = time.time()
        initialPopulation.newGeneration()

        result = initialPopulation.getBestSolution().getDistance()

        sol = initialPopulation.getBestSolution()

        # Demande d'affichage de toutes les villes sur l'écran
        draw(sol._path)

        # Refresh de l'écran
        pygame.display.flip()

        lastResults[i % 10] = result
        if i >= 10:
            averageLastResult = calculateAverage(lastResults)
            if math.fabs(result - averageLastResult) < 1:
                break
        i += 1

        endTime = time.time()
        lastIterationTime = endTime - startTime
        averageIterationTime = (averageIterationTime * (i - 1) + lastIterationTime) / i
        totalTime += lastIterationTime

    print("Solution trouvée, distance: %f" % initialPopulation.getBestSolution().getDistance())
    print("Temps d'exécution: %f s" % totalTime)


def calculateAverage(list):
    size = len(list)
    if size > 0:
        sum = 0
        for i in range(0, size):
            sum += list[i]

        return sum / size
    return 0


def generateInitialPopulation(problem, size):
    listSolutions = []
    for i in range(size):
        listSolutions.append(Solution(problem))

    listSolutions[0].cross(listSolutions[1])
    return Population(listSolutions)

#------------------------------------------------------
# Méthodes pour la GUI
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

    # On affiche chaque ville sur l'écran
    for city in citylist:
        pos = city.coords()

        # Tableau de points - Pour la création de ligne
        pointlist.append((pos.x(), pos.y()))

        pygame.draw.circle(screen, city_color, (pos.x(), pos.y()), city_radius)
        myfont = pygame.font.Font(None, 20)

        # Création du label contenant le nom de la ville
        label = myfont.render(city.name(), 1, text_color, None)

        # Affichage du label
        screen.blit(label, (pos.x() + 10, pos.y() - 6))


    # Sans oublier de mettre le premier élément à la dernière position
    pointlist.append((pointlist[0]))

     # On créer les lignes entre les villes
    pygame.draw.lines(screen, 0xffffffff, False, [p for p in pointlist], 2)

    text = font.render("Nombre: %i" % len(solution), True, font_color)
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
    # Parser les paramètres en ligne de commande
    # ----------------------------------------------
    parser = argparse.ArgumentParser(description='Example with long option names')

    parser.add_argument('filename', type=argparse.FileType('r'))

    parser.add_argument('--nogui', action='store_const', dest='gui',
                        const='1',
                        help='Desactive l\'interface graphique')

    parser.add_argument('--maxtime', action='store', dest='maxtime',
                        help='Desactive l\'interface graphique')

    # Récupération des paramètres
    args = parser.parse_args()

    # Paramètres par défaut
    parameterMaxtime = 0
    parameterGui = True

    if args.maxtime != 'None':
        parameterMaxtime = args.maxtime

    if args.gui != 'None':
        parameterGui = False

    # -------------------------------
    # Initialisation de la GUI
    # -------------------------------
    # Quelques paramètres
    screen_x = 500
    screen_y = 500
    city_color = [0, 255, 0]  # Green
    text_color = [0, 255, 0]  # Green
    city_radius = 5
    font_color = [255, 255, 255]  # white

    # Initialisation de la fenêtre, window et font
    screen, window, font = initScreen()


    # Appel de la méthode de résolution
    ga_solve(args.filename.name, parameterGui, parameterMaxtime)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == KEYDOWN:
            pygame.quit()
            break