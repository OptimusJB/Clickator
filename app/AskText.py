import sys
import Constants
from Screen import resize_screen
from TextZone import TextZone
import Chiffrement
import pygame
pygame.init()

class AskText:
    def __init__(self, pos, texte, valeur, type_attendu):
        self.texte = texte
        self.type_attendu = type_attendu
        self.valeur = valeur
        self.pos = pos
        self.size = (1, 1)

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

    def ask(self):
        # screen de choix
        fond_noir = pygame.surface.Surface((1920, 1080)).convert()
        fond_noir.fill((0, 0, 0))
        fond_noir.set_alpha(255 // 2)

        # blit du fond
        resize_screen.blit(fond_noir, (0, 0))
        rect_fond = pygame.rect.Rect(0, 0, 800, 400)
        rect_fond.center = (1920 // 2, 1080 // 2)
        resize_screen.draw_rect(Constants.saumon, rect_fond, 50)

        # création instruction
        instruction = Constants.police50.render("nouvelle valeur", True, "white")
        instruction_rect = instruction.get_rect()
        instruction_rect.centerx = rect_fond.centerx
        instruction_rect.y = rect_fond.top + 50

        # création texte
        texte = TextZone(Constants.police40)
        rect_texte = pygame.rect.Rect(rect_fond.left + 20, rect_fond.top + 150, rect_fond.width - 20 - 20, 80)
        texte.set_rect(rect_texte)
        texte.set_largeur_max(rect_texte.width - 20 - 20)
        texte.texte = self.valeur
        texte.clicked = True

        # création bouton valider
        valider_btn = Constants.police50.render("valider", True, "white")
        valider_btn_rect = valider_btn.get_rect()
        valider_btn_rect.width += 20
        valider_btn_rect.height += 20
        valider_btn_rect.centerx = rect_fond.centerx
        valider_btn_rect.bottom = rect_fond.bottom - 40

        boucle = True
        clock = pygame.time.Clock()
        while boucle:
            # reblit du fond + instruction + bouton valider
            resize_screen.draw_rect(Constants.saumon, rect_fond, 50)
            resize_screen.blit(instruction, instruction_rect.topleft)

            resize_screen.draw_rect(Constants.saumon2, valider_btn_rect, 20)
            resize_screen.blit(valider_btn, (valider_btn_rect.x + 10, valider_btn_rect.y + 10))

            # blit du texte
            resize_screen.draw_rect(Constants.saumon2, rect_texte, 20)
            resize_screen.blit(texte.get_image(), (rect_texte.x + 10, rect_texte.y + 10))

            clock.tick(30)
            resize_screen.flip()
            for event in pygame.event.get():
                texte.work(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not rect_fond.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            return None
                        else:
                            if valider_btn_rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                                can_change = True
                                for lettre in texte.get_text():
                                    if not lettre in Chiffrement.all_lettres:
                                        can_change = False

                                if can_change:
                                    # changement de valeur
                                    try:
                                        test = self.type_attendu(texte.get_text())
                                        self.valeur = str(test)
                                        return None
                                    except:
                                        pass


    def listen_entry(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.rect.Rect(self.pos, (self.size[0] + 20, self.size[1] + 20))
                if rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    old_valeur = self.valeur
                    self.ask()
                    if old_valeur != self.valeur:
                        return "changement"