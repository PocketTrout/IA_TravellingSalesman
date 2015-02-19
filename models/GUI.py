__author__ = 'michaelcaraccio'

import pygame
from models.city import City
from models.point import Point
from models.problem import Problem
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE


def initScreen():

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    return screen, window, font

def draw(problem):
    screen.fill(0)
    citylist = problem.getCities()

    # On affiche chaque ville sur l'écran
    for city in citylist:
        pos = city.coords()
        pygame.draw.circle(screen, city_color, (pos.x(), pos.y()), city_radius)
        myfont = pygame.font.Font(None, 20)

        # Création du label contenant le nom de la ville
        label = myfont.render(city.name(), 1, (100, 20, 20), None)

        # Affichage du label
        screen.blit(label, (pos.x() + 10, pos.y() - 6))
    text = font.render("Nombre: %i" % problem.getSize(), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

if __name__ == "__main__":

    # Quelques paramètres
    screen_x = 500
    screen_y = 500
    city_color = [10, 10, 200]  # blue
    city_radius = 3
    font_color = [255, 255, 255]  # white

    # Initialisation de la fenêtre, window et font
    screen, window, font = initScreen()

    city1 = City(Point(200, 300), "1")
    city2 = City(Point(300, 400), "2")
    city3 = City(Point(333, 50), "3")
    problem = Problem([city1, city2, city3])

    #TODO Il faut encore tracer les lignes !

    # Demande d'affichage de toutes les villes sur l'écran
    draw(problem)

    # Refresh de l'écran
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == KEYDOWN:
            pygame.quit()
            break