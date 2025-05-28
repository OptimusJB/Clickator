# ce fichier contient l'intégralité des éléments pyautogui et keyboard (pour ne pas avoir à rechecker tout le code si les librairies deviennent obsolètes)
# note importante : il est possible que les fonctions ne fonctionnement pas si la fenêtre pygame ne répond pas (du genre keyboard.is_pressed() qui semble ne pas marcher dans ce cas là)
import keyboard
import pyautogui

from Settings import settings
import pygame
import time
pygame.init()

pyautogui.PAUSE = 0 # permet d'enlever la pause entre les fonctions de pyautogui

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
        print("bouton pressé : touche inconnue")
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
    try:
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
    except:
        print("wait : touche inconnue")
        return False

def clic_normal(touche):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    fait un clic normal à l'emplacement de la souris
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic : touche invalide")
        return False
    dico = {"gauche":"left", "milieu":"middle", "droit":"right"}
    pyautogui.click(button=dico[touche])

def clic_press(touche):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    enfonce la touche de souris passée en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic maintenu: touche invalide")
        return False
    dico = {"gauche": "left", "milieu": "middle", "droit": "right"}
    pyautogui.mouseDown(button=dico[touche])

def clic_release(touche):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    relève la touche de souris passée en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic release : touche invalide")
        return False
    dico = {"gauche": "left", "milieu": "middle", "droit": "right"}
    pyautogui.mouseUp(button=dico[touche])

def teleport(x, y):
    """
    téléporte la souris aux coordonnées passées en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    pyautogui.moveTo(x, y)

def mouvement(x, y, temps):
    """
    déplace la souris aux coordonnées passées en paramètre avec le temps passé en paramètre (en ms)
    le setting 'degré de ressemblance image' est utilisé
    Marche même si la fenêtre est en arrière-plan.
    """
    pyautogui.moveTo(x, y, temps/1000)  # ms --> secondes

def get_image_center(chemin_image):
    """
    renvoie sous forme de tuple (x, y) le centre de l'image si elle est sur l'écran
    Marche même si la fenêtre est en arrière-plan.
    """
    try:
        image_pos = pyautogui.locateCenterOnScreen(chemin_image, confidence=settings.get_value("degré de ressemblance image"))
        return image_pos
    except pyautogui.ImageNotFoundException:
        return None