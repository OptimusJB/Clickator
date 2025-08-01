import sys
from Screen import resize_screen
from Save import save
import Constants
from Clic import Clic
from Wait import Wait
from TP import TP
from Mouvement import Mouvement
from Touche import Touche
from ReturnStart import ReturnStart
from MacroRun import MacroRun
from Scroll import Scroll
import PCControl
from Settings import settings
import pygame
pygame.init()

class MacroView:
    def __init__(self):
        self.selection_move = None
        self.action_ouverte = None  # détermine l'action qui doit être blitée à droite
        self.rect_dimensions = pygame.rect.Rect(20 + 500 + 40, 100, 500, 1080 - 100 - 40)
        self.nom_macro = None
        self.charged = False
        self.saved = True
        self.liste_actions = []  # liste d'objets (sans extension)
        self.rects_actions = []

        self.y = 0
        self.y_offset = 0


        self.cache_haut = pygame.rect.Rect(20 + 500 + 40 - 100, 0, 1460, 100)
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

        # bouton ajout d'action
        self.ajout_texte = Constants.police30.render("ajouter +", True, "white")
        self.rect_ajout_texte = self.ajout_texte.get_rect()
        self.rect_ajout_texte.width += 20
        self.rect_ajout_texte.height += 20
        self.rect_ajout_texte.centerx = self.rect_dimensions.centerx

        # bouton lancer macro
        self.texte_launch = Constants.police30.render("lancer macro", True, "white")
        self.rect_launch = self.texte_launch.get_rect()
        self.rect_launch.width += 20
        self.rect_launch.height += 20
        self.rect_launch.centerx = self.rect_dimensions.centerx
        self.rect_launch.y = 20

    def charger_macro(self):
        assert self.nom_macro != None, "nom macro pas encore initialisé"
        self.liste_actions = save.load_sauvegarde(self.nom_macro)[1:]
        self.charged = True
        self.action_ouverte = None
        self.selection_move = None
        self.saved = True
    
    def blit(self):
        self.rects_actions = []
        if self.nom_macro == None:
            return None
        
        resize_screen.draw_rect(Constants.saumon, self.rect_dimensions, 50)

        # check du chargement
        if not self.charged:
            texte = Constants.police30.render("chargement de la macro...", True, "white")
            texte_rect = texte.get_rect()
            texte_rect.center = self.rect_affichage.center
            resize_screen.blit(texte, texte_rect.topleft)
            return None

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
                if texte_rect.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())) or action == self.action_ouverte:
                    color = Constants.orange
                resize_screen.draw_rect(color, texte_rect, 20)
                resize_screen.blit(texte, (texte_rect.x + 10, texte_rect.y + 10))

            # blit de la selection move
            if self.selection_move != None and self.selection_move == action:
                move_rect = texte_rect.copy()
                move_texte = texte.copy()
                move_texte.set_alpha(255//2)

                move_rect.center = resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())
                resize_screen.draw_rect(Constants.saumon2, move_rect, 20)
                resize_screen.blit(move_texte, (move_rect.x + 10, move_rect.y + 10))

            self.rects_actions.append(texte_rect)

            self.y = self.y + 100

        # modification du rect d'ajout d'action + blit
        self.rect_ajout_texte.centery = self.y + self.y_offset

        color = Constants.saumon2
        if self.rect_ajout_texte.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
            color = Constants.orange

        if self.rect_ajout_texte.colliderect(self.rect_affichage):
            resize_screen.draw_rect(color, self.rect_ajout_texte, 20)
            resize_screen.blit(self.ajout_texte, (self.rect_ajout_texte.x + 10, self.rect_ajout_texte.y + 10))
        self.y = self.y + 100

        # blit du cache
        resize_screen.draw_rect(Constants.beige, self.cache_haut)

        # blit éléments titre macro
        resize_screen.blit(self.surface_titre, self.rect_titre.topleft)
        texte = Constants.police40.render(self.nom_macro, True, "white")
        texte_rect = texte.get_rect()
        texte_rect.center = self.rect_titre.center
        resize_screen.blit(texte, texte_rect.topleft)

        # blit bouton lancement macro
        color = Constants.saumon2
        if self.rect_launch.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
            color = Constants.orange

        resize_screen.draw_rect(color, self.rect_launch, 100)
        resize_screen.blit(self.texte_launch, (self.rect_launch.x + 10, self.rect_launch.y + 10))

        # appel du blit potentiel de l'action
        if not self.action_ouverte == None:
            if self.action_ouverte.blit() == "changement":
                self.action_ouverte.charged = False
                save.sauvegarder([self.nom_macro] + self.liste_actions)
                # self.saved = False

        # check pression bouton lancement macro
        if PCControl.check_pressed(settings.get_value("bouton lancement macro selectionnée")):
            MacroRun(self.liste_actions).run()

    def ajout_action(self):
        """
        écran à part pour l'ajout d'action
        """
        liste_actions = ["Clic", "Wait", "TP", "Mouvement", "Touche", "Scroll", "ReturnStart"]

        fond_noir = pygame.surface.Surface((1920, 1080)).convert()
        fond_noir.fill((0, 0, 0))
        fond_noir.set_alpha(255//2)

        # blit du fond
        resize_screen.blit(fond_noir, (0, 0))
        rect_fond = pygame.rect.Rect(0, 0, 310, 720)    # à changer au besoin
        rect_fond.center = (1920//2, 1080//2)
        resize_screen.draw_rect(Constants.saumon, rect_fond, 50)

        # blit des éléments
        rects_actions = []
        y = rect_fond.top + 20
        x = rect_fond.x + 20

        for element in liste_actions:
            texte = Constants.police40.render(element, True, "white")
            texte_rect = texte.get_rect()
            texte_rect.width += 20
            texte_rect.height += 20
            texte_rect.topleft = (x, y)

            resize_screen.draw_rect(Constants.saumon2, texte_rect, 20)
            resize_screen.blit(texte, (texte_rect.x + 10, texte_rect.y + 10))
            rects_actions.append(texte_rect)

            y = y + 100
            if y > rect_fond.bottom - texte_rect.size[1]:
                y = rect_fond.top + 20
                x = x + 300

        clock = pygame.time.Clock()
        boucle = True
        while boucle:
            clock.tick(30)
            resize_screen.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not rect_fond.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            return None
                        else:
                            for rect in rects_actions:
                                if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                                    index_rect = rects_actions.index(rect)
                                    action_choisie = liste_actions[index_rect]
                                    boucle = False

        # ajout dans self.liste_actions
        action_finale = None
        if action_choisie == "Clic":
            action_finale = Clic(["normal", "gauche", "appuyer"])
        elif action_choisie == "Wait":
            action_finale = Wait(["temps", "a", "1000", "non", "0"])
        elif action_choisie == "TP":
            action_finale = TP(["coordonnées", "0", "0", "images/", "non", "0"])
        elif action_choisie == "Mouvement":
            action_finale = Mouvement(["coordonnées", "0", "0", "images/", "non", "0", "2000"])
        elif action_choisie == "Touche":
            action_finale = Touche(["normal", "a", "appuyer"])
        elif action_choisie == "ReturnStart":
            action_finale = ReturnStart([])
        elif action_choisie == "Scroll":
            action_finale = Scroll(["bas", "10"])
        # à continuer : ajouter des instances d'action ici
        else:
            raise ValueError("action choisie non prise en charge")

        self.liste_actions.append(action_finale)
        self.charged = False

        # sauvegarde
        save.sauvegarder([self.nom_macro] + self.liste_actions)
        #self.saved = False

    def listen_entry(self, event):
        if self.nom_macro == None:
            return None

        if not self.charged:
            self.charger_macro()
            self.blit() # pour mettre à jour self.rects_macros

        if event.type == pygame.MOUSEWHEEL:
            if self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(pygame.mouse.get_pos())):
                for i in range(abs(event.y)):
                    if event.y < 0:
                        if self.y + self.y_offset > self.rect_affichage.bottom:
                            self.y_offset -= 30

                    elif event.y > 0:
                        if self.y_offset < 0:
                            self.y_offset += 30

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect_ajout_texte.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    # écran ajout d'action
                    self.ajout_action()

                elif self.rect_launch.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    MacroRun(self.liste_actions).run()

                elif self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_actions:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
                                # ouverture de la page de l'action cliquée
                                index_rect = self.rects_actions.index(rect)
                                self.action_ouverte = self.liste_actions[index_rect]
                                self.action_ouverte.charged = False
                            else:
                                # shift pressé, donc clonage
                                index_rect = self.rects_actions.index(rect)
                                new_action = type(self.liste_actions[index_rect])(self.liste_actions[index_rect].valeurs)
                                self.liste_actions.insert(index_rect, new_action)
                                self.charged = False

                                # sauvegarde
                                save.sauvegarder([self.nom_macro] + self.liste_actions)

            elif event.button == 3:
                if self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_actions:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            # suppression de l'action
                            index_rect = self.rects_actions.index(rect)
                            self.action_ouverte = None

                            self.liste_actions.pop(index_rect)
                            self.charged = False

                            # sauvegarde
                            save.sauvegarder([self.nom_macro] + self.liste_actions)

            elif event.button == 2:
                if self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_actions:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            index_rect = self.rects_actions.index(rect)
                            self.selection_move = self.liste_actions[index_rect]

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selection_move != None:
                if self.rect_dimensions.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    for rect in self.rects_actions:
                        if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            index_rect = self.rects_actions.index(rect)
                            if not self.liste_actions[index_rect] == self.selection_move:
                                # déplacement
                                index_ancien = self.liste_actions.index(self.selection_move)
                                self.liste_actions[index_ancien] = self.liste_actions[index_rect]
                                self.liste_actions[index_rect] = self.selection_move
                                self.charged = False

                                # sauvegarde
                                save.sauvegarder([self.nom_macro] + self.liste_actions)

                self.selection_move = None

        # appel du listen_entry potentiel de l'action
        if not self.action_ouverte == None:
            if self.action_ouverte.listen_entry(event) == "changement":
                self.action_ouverte.charged = False
                save.sauvegarder([self.nom_macro] + self.liste_actions)
                #self.saved = False

macro_view = MacroView()