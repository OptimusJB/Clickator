# ce fichier contient l'intégralité des éléments mouse, pyautogui et keyboard (pour ne pas avoir à rechecker tout le code si les librairies deviennent obsolètes)
# note importante : il est possible que les fonctions ne fonctionnent pas si la fenêtre pygame ne répond pas (du genre keyboard.is_pressed() qui semble ne pas marcher dans ce cas là)
# keyboard.is_pressed() ne semble pas détecter les touches appuyées par le programme
# normalement compatible avec les jeux
import mouse
import keyboard
import pygame
import time
import pyautogui
from Settings import settings
pygame.init()

def check_pressed(touche:str):
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
    return mouse.get_position()

def wait_for_not_pressed(touche:str):
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

def clic_normal(touche:str):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    fait un clic normal à l'emplacement de la souris
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic : touche invalide")
        return False
    dico = {"gauche": mouse.LEFT, "milieu": mouse.MIDDLE, "droit": mouse.RIGHT}
    mouse.click(button=dico[touche])

def touche_normal(touche:str):
    """
    fait un appui simple d'une touche de clavier
    Il peut y avoir plusieurs touches
    exemple touche si plusieurs touches : abcde
    Marche même si la fenêtre est en arrière-plan.
    """
    if touche[:2] == "./":
        touche = touche.replace("./", "")
        touche = touche.replace(" ", "")    # on enlève les espaces
        for element in touche.split("+"):
            try:
                keyboard.send(element)
            except:
                print(element + " : touche inconnue")
        return None

    for element in touche:
        try:
            keyboard.send(element)
        except:
            print(element + " : touche inconnue")

def clic_press(touche:str):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    enfonce la touche de souris passée en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic maintenu: touche invalide")
        return False
    dico = {"gauche": mouse.LEFT, "milieu": mouse.MIDDLE, "droit": mouse.RIGHT}
    mouse.press(button=dico[touche])

def touche_press(touche:str):
    """
    enfonce la ou les touches de clavier passées en paramètre
    exemple touche si plusieurs touches : abcde
    Marche même si la fenêtre est en arrière-plan.
    si ./ au début, exécute chaque éléments séparés par des + (ex : ctrl+alt+esc)
    """
    if touche[:2] == "./":
        touche = touche.replace("./", "")
        touche = touche.replace(" ", "")    # on enlève les espaces
        for element in touche.split("+"):
            try:
                keyboard.press(element)
            except:
                print(element + " : touche inconnue")
        return None

    for element in touche:
        try:
            keyboard.press(element)
        except:
            print(element + " : touche inconnue")

def clic_release(touche:str):
    """
    touche = 'gauche' ou 'milieu' ou 'droit'
    relève la touche de souris passée en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    if not touche in ["gauche", "milieu", "droit"]:
        print("clic release : touche invalide")
        return False
    dico = {"gauche": mouse.LEFT, "milieu": mouse.MIDDLE, "droit": mouse.RIGHT}
    mouse.release(button=dico[touche])

def touche_release(touche):
    """
    relève la ou les touches de clavier passées en paramètre
    exemple touche si plusieurs touches : abcde
    Marche même si la fenêtre est en arrière-plan.
    """
    if touche[:2] == "./":
        touche = touche.replace("./", "")
        touche = touche.replace(" ", "")    # on enlève les espaces
        for element in touche.split("+"):
            try:
                keyboard.release(element)
            except:
                print(element + " : touche inconnue")
        return None

    for element in touche:
        try:
            keyboard.release(element)
        except:
            print(element + " : touche inconnue")

def release_all_keys():
    """
    relève toutes les touches potentiellement enfoncées
    Marche même si la fenêtre est en arrière-plan.
    """
    for element in "azertyuiopmlkjhgfdsqwxcvbn,;:!&é'(-è_çà)=0123456789²*-+/?./§£µ%~#{[|`^@]}" + '"':
        keyboard.release(element)
    for element in [mouse.LEFT, mouse.MIDDLE, mouse.RIGHT]:
        mouse.release(element)

def teleport(x:int, y:int):
    """
    téléporte la souris aux coordonnées passées en paramètre
    Marche même si la fenêtre est en arrière-plan.
    """
    mouse.move(x, y)

def mouvement(x:int, y:int, temps:int):
    """
    déplace la souris aux coordonnées passées en paramètre avec le temps passé en paramètre (en ms)
    le setting 'degré de ressemblance image' est utilisé
    Marche même si la fenêtre est en arrière-plan.
    """
    mouse.move(x, y, duration=temps/1000)  # ms --> secondes

def get_image_center(chemin_image:str):
    """
    renvoie sous forme de tuple (x, y) le centre de l'image si elle est sur l'écran
    Marche même si la fenêtre est en arrière-plan.
    """
    try:
        image_pos = pyautogui.locateCenterOnScreen(chemin_image, confidence=settings.get_value("degré de ressemblance image"))
        #print("image pos", image_pos)
        return image_pos
    except OSError:
        return "pas de fichier"
    except pyautogui.ImageNotFoundException:
        return "non trouvé sur l'écran"

def scroll(valeur:int):
    """
    si valeur négative, scroll vers le bas. Si positif, vers le haut
    Marche même si la fenêtre est en arrière-plan.
    """
    mouse.wheel(valeur)

def check_size(x, y):
    """
    retourne un tuple (x, y) qui est contenu dans l'écran (en gros ça modifie x ou y s'ils sont en dehors de l'écran (tp/mouvement impossible))
    Marche même si la fenêtre est en arrière-plan.
    """
    size = pyautogui.size()
    x = min(x, size[0] - 1)    # size[0] - 1 car le point en haut à gauche est (0,0) et pas (1, 1)
    y = min(y, size[1] - 1)
    return (x, y)