from Screen import resize_screen
import Constants
import pygame
from AskText import AskText
from Switch import Switch
pygame.init()

class ReturnStart:
    def __init__(self, liste_valeurs):
        self.nom = "ReturnStart"
        self.charged = False
        self.valeurs = liste_valeurs    # très probablement une liste de str
        # de la forme [type (coordonnées / image), x, y, chemin_image, aléatoire, dispersion si aléatoire, temps_mouvement]
        # tout est en str

        self.rect_dimensions = pygame.rect.Rect(20 + 500 + 40 + 500 + 40, 100, 800, 1080 - 100 - 40)

        self.rect_affichage = self.rect_dimensions.copy()
        self.rect_affichage.height -= 100

        self.rect_titre = self.rect_dimensions.copy()
        self.rect_titre.height = self.rect_dimensions.height - self.rect_affichage.height
        self.rect_titre.y = self.rect_affichage.height + 100

        self.surface_titre = pygame.surface.Surface((self.rect_titre.size), pygame.SRCALPHA)
        rect_surface = self.rect_dimensions.copy()
        rect_surface.y = - self.rect_affichage.height
        rect_surface.x = 0
        pygame.draw.rect(self.surface_titre, Constants.saumon2, rect_surface, border_radius=50)
        self.liste_elements = []


    def blit(self):
        resize_screen.draw_rect(Constants.saumon, self.rect_dimensions, 50)

        # blit éléments titre macro
        resize_screen.blit(self.surface_titre, self.rect_titre.topleft)
        texte = Constants.police40.render(self.nom, True, "white")
        texte_rect = texte.get_rect()
        texte_rect.center = self.rect_titre.center
        resize_screen.blit(texte, texte_rect.topleft)

        # blit éléments
        for element in self.liste_elements:
            resize_screen.blit(element.get_image(), element.pos)

    def listen_entry(self, event):

        for element in self.liste_elements: # switch ou asktext
            assert self.liste_elements.count(element) == 1, "deux éléments ont le même nom"
            if element.listen_entry(event) == "changement":
                index_element = self.liste_elements.index(element)
                # potentiels changements de la valeur à faire ici

                self.valeurs[index_element] = element.valeur
                return "changement" # retourne vers MacroView pour la sauvegarde

    def run(self):
        pass