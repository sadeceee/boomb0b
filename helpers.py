import os
import pygame


def image_loader(dir, filename):
    return pygame.image.load(os.path.join(dir, filename))