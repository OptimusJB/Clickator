from Screen import resize_screen
from Save import save
import Constants
import pygame
pygame.init()

class MacroView:
    def __init__(self):
        self.rect_dimensions = pygame.rect.Rect(20 + 500 + 40, 100, 500, 1080 - 100 - 40)
        self.nom_macro = None
        self.charged = False
        self.liste_actions = []  # liste d'objets (sans extension)
        self.rects_actions = []

        self.y = 0
        self.y_offset = 0


        self.cache_haut = pygame.rect.Rect(20 + 500 + 40, 0, 500, 100)
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

    def charger_macro(self):
        assert self.nom_macro != None, "nom macro pas encore initialisé"
        self.liste_actions = save.load_sauvegarde(self.nom_macro)
        self.charged = True
    
    def blit(self):
        self.rects_actions = []
        if self.nom_macro == None:
            return None
        
        resize_screen.draw_rect(Constants.saumon, self.rect_dimensions, 50)

        # blit actions
        self.y = 150
        for action in self.liste_actions:
            texte = action.nom
            if len(texte) > 22:
                texte = texte[:22] + "..."

            texte = Constants.police30.render(texte, True , Constants.beige)
            texte_rect = texte.get_rect()
            texte_rect.width += 20
            texte_rect.height += 20
            texte_rect.center = (self.rect_dimensions.centerx, self.y + self.y_offset)

            if texte_rect.colliderect(self.rect_affichage):
                # changement de couleur si la souris est dessus
                color = Constants.saumon2
                if texte_rect.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
                    color = Constants.orange
                resize_screen.draw_rect(color, texte_rect, 20)
                resize_screen.blit(texte, (texte_rect.x + 10, texte_rect.y + 10))

            self.rects_macros.append(texte_rect)

            self.y = self.y + 100

        # blit du cache
        resize_screen.draw_rect(Constants.beige, self.cache_haut)

        # blit éléments titre macro
        resize_screen.blit(self.surface_titre, self.rect_titre.topleft)
        texte = Constants.police40.render(self.nom_macro, True, "white")
        texte_rect = texte.get_rect()
        texte_rect.center = self.rect_titre.center
        resize_screen.blit(texte, texte_rect.topleft)
    
    def listen_entry(self, event):
        if self.nom_macro == None:
            return None

        if not self.charged:
            self.charger_macro()
            self.blit() # pour mettre à jour self.rects_macros

macro_view = MacroView()