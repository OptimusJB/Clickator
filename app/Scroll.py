from Screen import resize_screen
import Constants
import pygame
import sys
from AskText import AskText
import PCControl
from Switch import Switch
pygame.init()
class Scroll:
    def __init__(self, liste_valeurs):
        self.nom = "Scroll"
        self.charged = False
        self.valeurs = liste_valeurs    # très probablement une liste de str
        # de la forme [haut/bas, longueur]

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
        self.liste_elements = [Switch((1500, 120), "direction", ["haut", "bas"], self.valeurs[0]),   # la liste doit être dans le bon ordre
        AskText((1500, 220), "longueur", self.valeurs[1], int)]

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
        def check_exit():
            """
            permet de rafraichir avec pygame.event.get(), tout en
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # liste de la forme [haut/bas, longueur]
        direction = self.valeurs[0]
        longueur = int(self.valeurs[1])

        if direction == "bas":
            longueur = -1 * longueur

        PCControl.scroll(longueur)