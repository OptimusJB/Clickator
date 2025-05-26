import Constants
from Screen import resize_screen
import pygame
pygame.init()

class Switch:
    def __init__(self, pos, texte, valeurs:list, valeur:str):
        # test d'unicité
        for element in valeurs: # switch ou asktext
            assert valeurs.count(element) == 1, "deux éléments ont le même nom"
        
        self.texte = texte
        self.pos = pos
        self.valeurs = valeurs
        self.size = None
        assert valeur in valeurs, "la valeur entrée n'est pas dans la liste de valeurs"
        self.valeur = valeur
        self.maj_location()
    
    def maj_location(self):
        texte = Constants.police30.render(self.texte + " : " + str(self.valeur), True, "white")
        self.size = texte.get_size()
        rect = pygame.rect.Rect(self.pos, (self.size[0] + 20, self.size[1] + 20))
        rect.centerx = 1500
        self.pos = rect.topleft
    
    def get_image(self):
        # cette méthode met également à jour self.size
        texte = Constants.police30.render(self.texte + " : " + str(self.valeur), True, "white")
        self.size = texte.get_size()
        texte_rect = texte.get_rect()
        texte_rect.width += 20
        texte_rect.height += 20
        surface = pygame.surface.Surface(texte_rect.size, pygame.SRCALPHA)

        # changement de couleur si la souris est dessus
        color = Constants.saumon2
        rect = pygame.rect.Rect(self.pos, (self.size[0] + 20, self.size[1] + 20))
        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
            color = Constants.orange
        pygame.draw.rect(surface, color, texte_rect, border_radius=20)
        #print(rect, texte_rect)
        surface.blit(texte, (texte_rect.x + 10, texte_rect.y + 10))
        return surface
    
    def listen_entry(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.rect.Rect(self.pos, (self.size[0] + 20, self.size[1] + 20))
                if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    #self.valeur_base = str((int(self.valeur_base) + 1) % len(self.valeurs))
                    index_valeur = self.valeurs.index(self.valeur)
                    index_valeur = (index_valeur + 1) % len(self.valeurs)
                    self.valeur = self.valeurs[index_valeur]
                    self.maj_location()
                    return "changement"