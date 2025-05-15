from Screen import resize_screen
import Constants
import pygame
pygame.init()

class Accueil:
    def __init__(self, state):
        self.state = state

    def run(self):
        boucle = True
        while boucle:
            # blit du fond
            resize_screen.fill(Constants.saumon)
            resize_screen.flip()