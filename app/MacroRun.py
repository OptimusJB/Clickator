from ReturnStart import ReturnStart

import sys
from Screen import resize_screen
import PCControl
from Settings import settings
import Constants
import time
import pygame
pygame.init()

class MacroRun:
    def __init__(self, liste_actions_macro):
        self.liste_actions = liste_actions_macro

    def run(self):
        def check_exit():
            """
            permet de rafraichir avec pygame.event.get(), tout en
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # attente fin de pression au cas où
        PCControl.wait_for_not_pressed(settings.get_value("bouton lancement macro selectionnée"))

        # blit du fond d'exécution
        resize_screen.fill((0,0,0))
        texte = Constants.police50.render(("macro en cours d'exécution, appuyez sur " + settings.get_value("touche d'arrêt de la macro") + " pour l'arrêter"), True, "white")
        texte_rect = texte.get_rect()
        texte_rect.center = (1920//2, 1080//2)
        resize_screen.blit(texte, texte_rect)
        resize_screen.flip()

        # exécution des actions
        index_action = -1
        while index_action < len(self.liste_actions) - 1 and len(self.liste_actions) > 0:   # test au cas où la macro est vide
            resize_screen.flip()

            index_action = index_action + 1
            action = self.liste_actions[index_action]
            check_exit()
            action.run()

            if PCControl.check_pressed(settings.get_value("touche d'arrêt de la macro")):
                break
            if type(action) == ReturnStart:
                index_action = -1
                continue

            time.sleep(int(settings.get_value("temps entre les actions (em ms)"))/1000)

        PCControl.wait_for_not_pressed(settings.get_value("touche d'arrêt de la macro"))
        #PCControl.release_all_keys()