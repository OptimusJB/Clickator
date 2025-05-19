from Screen import resize_screen
from Save import save
import pygame
pygame.init()

class MacroView:
    def __init__(self):
        self.nom_macro = None
        self.charged = False
        self.liste_actions = []  # liste d'objets (sans extension)
        self.rects_actions = []

        self.y = 0
        self.y_offset = 0

    def charger_macro(self):
        assert self.nom_macro != None, "nom macro pas encore initialisé"
        self.liste_actions = save.load_sauvegarde(self.nom_macro)
        self.charged = True
    
    def blit(self):
        if self.nom_macro == None:
            return None
    
    def listen_entry(self, event):
        if self.nom_macro == None:
            return None

        if not self.charged:
            self.charger_macro()
            self.blit() # pour mettre à jour self.rects_macros

macro_view = MacroView()