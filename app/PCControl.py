# ce fichier contient l'intégralité des éléments pyautogui et keyboard (pour ne pas avoir à rechecker tout le code si les librairies deviennent obsolètes)
# note importante : il est possible que les fonctions ne fonctionnement pas si la fenêtre pygame ne répond pas (du genre keyboard.is_pressed() qui semble ne pas marcher dans ce cas là)
import keyboard
import pyautogui

import pygame
import time
pygame.init()

def check_pressed(touche):
    """
    Retourne True si la ou les touches en paramètre sont actuellement pressées.
    exemple paramètre si plusieurs touches = 'abcd'
    Marche même si la fenêtre est en arrière-plan.
    """
    try:
        resultat = True
        for element in touche:
            if not keyboard.is_pressed(element):
                resultat = False
        return resultat
    except:
        return False

def get_mouse_pos():
    """
    retourne un tuple de la forme (x, y) représentant la valeur de la souris sur l'écran
    le point (0, 0) est en haut à gauche
    """
    return pyautogui.position()

def wait_for_not_pressed(touche):
    """
    la fonction s'arrête quand la ou les touches arrêtent d'être pressées
    exemple paramètre si plusieurs touches = 'abcd'
    Marche même si la fenêtre est en arrière-plan.
    """
    boucle = True
    while boucle:
        resultat = True
        for element in touche:
            if keyboard.is_pressed(element):
                resultat = False
        if resultat:
            boucle = False
        pygame.event.get()  # d'après quelques tests, is_pressed ne fonctionne pas bien si la fenêtre ne répond pas
        time.sleep(0.1)