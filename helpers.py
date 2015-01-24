import os
import pygame


images = {}

def image_loader(dir, filename):
    if filename not in images:
        images[filename] = pygame.image.load(os.path.join(dir, filename))
        if ".png" in filename:
            images[filename].convert_alpha()

    return images[filename]

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

def check_expand(gf, size, direction, newX, newY):
    isWall, isBreakable, isDeadly = gf.checkPosition(newX, newY)
    if not isWall:
        explosion(gf, size, direction, newX, newY)
    # TODO check isBreakable
