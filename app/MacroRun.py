from Screen import resize_screen
import PCControl
from Settings import settings
import Constants
import pygame
pygame.init()

class MacroRun:
    def __init__(self, liste_actions_macro):
        self.liste_actions = liste_actions_macro

    def run(self):
        # attente fin de pression au cas où
        PCControl.wait_for_not_pressed(settings.get_value("bouton lancement macro selectionnée"))

        # blit du fond d'exécution
        resize_screen.fill((0,0,0))
        texte = Constants.police50.render(("macro en cours d'exécution, appuyez sur " + settings.get_value("touche d'arrêt de la macro") + " pour l'arrêter"), True, "white")
        texte_rect = texte.get_rect()
        texte_rect.center = (1920//2, 1080//2)
        resize_screen.blit(texte, texte_rect)