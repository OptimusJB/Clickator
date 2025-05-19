from Screen import resize_screen
import Constants
import pygame
from ListMacroView import list_macro_view
import sys
from MacroView import macro_view
pygame.init()

class Accueil:
    def __init__(self, state):
        self.state = state
        self.work_elements = [macro_view, list_macro_view]

    def run(self):
        clock = pygame.time.Clock()
        boucle = True
        while boucle:
            clock.tick(30)

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