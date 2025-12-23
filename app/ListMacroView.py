from Screen import resize_screen
import Constants
import os
import pygame
import Chiffrement
from TextZone import TextZone
from MacroView import macro_view
pygame.init()

class ListMacroView:
    def __init__(self):
        self.charged = False
        self.liste_macros = []  # liste de str (sans extension)
        self.rects_macros = []

        self.y = 0
        self.y_offset = 0

        # création des rects de dimensions
        self.rect_dimensions = pygame.rect.Rect(20, 100, 500, 1080 - 100 - 40)
        self.cache_haut = pygame.rect.Rect(20, 0, 500, 100)

        self.rect_affichage = self.rect_dimensions.copy()
        self.rect_affichage.height -= 200

        # création cache création macro
        self.rect_creation = self.rect_dimensions.copy()
        self.rect_creation.height = self.rect_dimensions.height - self.rect_affichage.height
        self.rect_creation.y = self.rect_affichage.height + 100

        self.surface_creation = pygame.surface.Surface((self.rect_creation.size), pygame.SRCALPHA)
        rect_surface = self.rect_dimensions.copy()
        rect_surface.y = - self.rect_affichage.height
        rect_surface.x = 0
        pygame.draw.rect(self.surface_creation, Constants.saumon2, rect_surface, border_radius=50)

        # création macro
        self.texte_creation = TextZone(Constants.police40)
        self.rect_texte_creation = pygame.rect.Rect(self.rect_creation.left + 20, self.rect_creation.top + 20, self.rect_affichage.width - 40, 80)
        self.texte_creation.set_rect(self.rect_texte_creation.copy())
        self.texte_creation.get_rect().width -= 20
        self.texte_creation.set_largeur_max(self.rect_texte_creation.width - 20 - 30)

        self.texte_creation_btn = Constants.police40.render("créer macro", True, "white")
        self.creation_btn_rect = self.texte_creation_btn.get_rect()
        self.creation_btn_rect.size = (self.creation_btn_rect.width + 20, self.creation_btn_rect.height + 20)
        self.creation_btn_rect.centerx = self.rect_texte_creation.centerx
        self.creation_btn_rect.top = self.rect_texte_creation.bottom + 10

        # temps offset
        self.temps_offset = 0

    def maj_offset(self):
        if self.temps_offset > 0:
            for i in range((abs(self.temps_offset) // 5 + 1)):
                if self.y_offset < 0:  # condition scroll
                    self.y_offset += 25
            for i in range((abs(self.temps_offset) // 5) + 1):
                if self.temps_offset > 0:
                    self.temps_offset -= 1

        elif self.temps_offset < 0:
            for i in range((abs(self.temps_offset) // 5 + 1)):
                if self.y + self.y_offset > self.rect_dimensions.bottom - 20:  # condition scroll
                    self.y_offset -= 25
            for i in range((abs(self.temps_offset) // 5) + 1):
                if self.temps_offset < 0:
                    self.temps_offset += 1
    def blit(self):
        # on met à jour le scrolling
        self.maj_offset()

        self.rects_macros = []
        # blit du fond
        resize_screen.draw_rect(Constants.saumon, self.rect_dimensions, 50)
        #resize_screen.draw_rect("green", self.rect_affichage)
        #resize_screen.draw_rect("red", self.rect_creation)

        # check du chargement
        if not self.charged:
            texte = Constants.police30.render("chargement des macros...", True, "white")
            texte_rect = texte.get_rect()
            texte_rect.center = self.rect_affichage.center
            resize_screen.blit(texte, texte_rect.topleft)
            return None
        
        # check si pas de macros
        if len(self.liste_macros) == 0:
            texte = Constants.police30.render("pas de macros", True, "white")
            texte_rect = texte.get_rect()
            texte_rect.center = self.rect_affichage.center
            resize_screen.blit(texte, texte_rect.topleft)

        # blit des macros
        self.y = 150
        for macro in self.liste_macros:
            texte = macro
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

            self.y += 100

        # blit du cache
        resize_screen.draw_rect(Constants.beige, self.cache_haut)

        # blit éléments création macro
        resize_screen.blit(self.surface_creation, self.rect_creation.topleft)
        
        resize_screen.draw_rect(Constants.saumon, self.rect_texte_creation, 20)
        resize_screen.blit(self.texte_creation.get_image(), (self.rect_texte_creation.left + 20, self.rect_texte_creation.top + 10))

        # blit du bouton création de macro
        resize_screen.draw_rect(Constants.saumon, self.creation_btn_rect, 20)
        resize_screen.blit(self.texte_creation_btn, (self.creation_btn_rect.x + 10, self.creation_btn_rect.y + 10))

        #resize_screen.draw_rect("blue", pygame.rect.Rect(50, self.y + self.y_offset, 10, 10))

    def charger_macros(self):
        #self.y_offset = 0
        self.liste_macros = os.listdir("data/")
        
        a_enlever = []
        for element in self.liste_macros:
            if element[len(element)-len(".txt"):] != ".txt":
                a_enlever.append(element)
        
        for element in a_enlever:
            self.liste_macros.remove(element)

        for i in range(len(self.liste_macros)):
            self.liste_macros[i] = self.liste_macros[i].replace(".txt", "")

        self.charged = True
    
    def listen_entry(self, event):
        if not self.charged:
            self.charger_macros()
            self.blit() # pour mettre à jour self.rects_macros
        
        self.texte_creation.work(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect_affichage.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_macros:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            macro_choisie = self.liste_macros[self.rects_macros.index(rect)]
                            macro_view.charged = False
                            macro_view.nom_macro = macro_choisie
                            macro_view.y_offset = 0
                
                elif self.creation_btn_rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    if not self.texte_creation.texte + ".txt" in os.listdir("data/"):
                        # check des lettres, pour voi si elle sont autorisées
                        can_create = True
                        for element in self.texte_creation.texte:
                            if not element in Chiffrement.all_lettres:
                                can_create = False

                        if can_create and not len(self.texte_creation.texte) == 0:
                            fichier = open("data/" + self.texte_creation.texte + ".txt", "w")
                            fichier.close()
                            self.texte_creation.texte = ""
                            self.charged = False
                            macro_view.nom_macro = None
            
            elif event.button == 3:
                if self.rect_affichage.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_macros:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            macro_choisie = self.liste_macros[self.rects_macros.index(rect)]
                            os.remove("data/" + macro_choisie + ".txt")
                            self.charged = False
                            macro_view.nom_macro = None
        
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
                for i in range(abs(event.y)):
                    if event.y < 0:
                        if self.y + self.y_offset > self.rect_affichage.bottom:
                            self.temps_offset -= 5
                            #self.y_offset -= 30
                    
                    elif event.y > 0:
                        if self.y_offset < 0:
                            self.temps_offset += 5
                            #self.y_offset += 30
        
list_macro_view = ListMacroView()