import os
import pygame


images = {}

def image_loader(dir, filename):
    if filename not in images:
        images[filename] = pygame.image.load(os.path.join(dir, filename))

    return images[filename]