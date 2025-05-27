# ce fichier contient l'intégralité des éléments pyautogui et keyboard (pour ne pas avoir à rechecker tout le code si les librairies deviennent obsolètes)
import keyboard
import pyautogui
import time

def check_pressed(touche):
    """
    Retourne True si la touche pressée en paramètre est actuellement pressée.
    Marche même si la fenêtre est en arrière-plan.
    """
    try:
        return keyboard.is_pressed(touche)
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
    la fonction s'arrête quand la touche arrête d'être pressée
    """
    while keyboard.is_pressed(touche):
        time.sleep(0.1)