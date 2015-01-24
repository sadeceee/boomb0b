import os
import pygame


def image_loader(dir, filename):
    return pygame.image.load(os.path.join(dir, filename))

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
    print(fields)
    return fields