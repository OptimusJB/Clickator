from Screen import resize_screen
import Constants
import pygame
from AskText import AskText
import PCControl
from Settings import settings
from Switch import Switch
pygame.init()
class Mouvement:
    def __init__(self, liste_valeurs):
        self.nom = "Mouvement"
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
        self.liste_elements = [Switch((1500, 120), "type mouvement", ["coordonnées", "image"], self.valeurs[0]), # la liste doit être dans le bon ordre
                               AskText((1500, 220), "x", self.valeurs[1], int),
                               AskText((1500, 320), "y", self.valeurs[2], int),
                               AskText((1500, 420), "chemin image", self.valeurs[3], str),
                               Switch((1500, 520), "coordonnées aléatoire", ["oui", "non"], self.valeurs[4]),
                               AskText((1500, 620), "dispersion si aléatoire (en ms)", self.valeurs[5], int),
                               AskText((1500, 720), "temps de mouvement", self.valeurs[6], int)]


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

        # check de la pression du bouton
        if PCControl.check_pressed(settings.get_value("bouton changement coordonnées")):
            # changement des coordonnées
            mouse_pos = PCControl.get_mouse_pos()
            self.valeurs[1] = str(mouse_pos[0])
            self.valeurs[2] = str(mouse_pos[1])
            # PCControl.wait_for_not_pressed(settings.get_value("bouton changement coordonnées"))

            # mise à jour de l'affichage
            self.liste_elements[1].valeur = str(self.valeurs[1])
            self.liste_elements[2].valeur = str(self.valeurs[2])
            self.liste_elements[1].maj_location()
            self.liste_elements[2].maj_location()
            return "changement"  # retourne vers MacroView pour la sauvegarde

    def listen_entry(self, event):

        for element in self.liste_elements: # switch ou asktext
            assert self.liste_elements.count(element) == 1, "deux éléments ont le même nom"
            if element.listen_entry(event) == "changement":
                index_element = self.liste_elements.index(element)
                # potentiels changements de la valeur à faire ici

                self.valeurs[index_element] = element.valeur
                return "changement" # retourne vers MacroView pour la sauvegarde