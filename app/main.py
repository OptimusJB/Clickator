import pygame
from Screen import resize_screen
from State import state
import os
pygame.init()

if __name__ == '__main__':
    # création du dossier data s'il n'existe pas
    if not "data" in os.listdir():
        os.mkdir("data")

    infos = pygame.display.Info()
    pygame.display.set_caption("Clickator")
    pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load("assets/logo.png"), (32, 32)))
    resize_screen.set_mode((min(infos.current_w, 1920) * 0.6, min(infos.current_h, 1080) * 0.6), pygame.RESIZABLE)

    while True:
        state.state_actuel.run()