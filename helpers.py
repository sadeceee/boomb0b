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
