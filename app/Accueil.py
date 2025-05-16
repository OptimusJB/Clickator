from Screen import resize_screen
import Constants
import pygame
from ListMacroView import list_macro_view
import sys
pygame.init()

class Accueil:
    def __init__(self, state):
        self.state = state
        self.work_elements = [list_macro_view]

    def run(self):
        boucle = True
        while boucle:
            # blit du fond
            resize_screen.fill(Constants.beige)

            for element in self.work_elements:
                element.blit()

            resize_screen.flip()

            for event in pygame.event.get():
                for element in self.work_elements:
                    element.listen_entry(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()