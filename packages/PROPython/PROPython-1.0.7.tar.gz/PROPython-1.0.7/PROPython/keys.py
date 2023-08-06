import pygame
from PROPython.Settings import _keys_
from time import sleep

def is_key_pressed(key):
    keys = pygame.key.get_pressed()

    sleep(0.02)
    if keys[key]:
        return True
    else:
        return False