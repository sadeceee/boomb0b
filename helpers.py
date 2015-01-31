import os
import pygame
from constants import *


images = {}

def image_loader(dir, filename):
    if filename not in images:
        images[filename] = pygame.image.load(os.path.join(dir, filename))
        if ".png" in filename:
            images[filename].convert_alpha()
        else:
            images[filename].convert()

    return images[filename]

def image_saver(savename, surface):
    if savename not in images:
        images[savename] = surface
        images[savename].set_colorkey(BLACK)
        images[savename].convert()

    return images[savename]

def image_test(savename):
    if savename in images:
        return images[savename]

    return False

def get_image(savename, x, y):
    images[savename] = pygame.Surface([FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT])
    images[savename].fill(RED)
    images[savename].blit(savename, (0, 0), (x, y, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
    images[savename].set_colorkey(RED)
    images[savename].convert()
    return images[savename]

def map_loader(dir, filename):
    f = open(os.path.join(dir, filename), "r")
    fields = []
    for line in f:
        row = []
        for x in line:
            if(x != "\n"):
                row.append(x)
        fields.append(row)
    f.close()
    return fields

def get_center_value(key):
    if(key in CENTER_DICTIONARY):
        return CENTER_DICTIONARY[key]
    else:
        return (False, False)