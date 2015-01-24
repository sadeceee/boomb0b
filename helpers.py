import os
import pygame


images = {}

def image_loader(dir, filename):
    if filename not in images:
        images[filename] = pygame.image.load(os.path.join(dir, filename))

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