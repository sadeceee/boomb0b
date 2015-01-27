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

"""
surface: base image
color:   color to modulate
colors:  lists of tuples of name, color
"""
def modulate_color(surface, color, colors):
    base_surface = surface.copy()
    mapped_base_color = pygame.Surface.map_rgb(color)

    pixel_array = pygame.PixelArray(base_surface)

    # Iterate over the colors
    for c_name,c_color in colors:
        mapped_color = pygame.Surface.map_rgb(c_color)

        # Iterate over the pixel array of the base surface
        c_counter = 0
        for pixel in pixel_array:
            # Compare pixel color with the mapped base color
            if pixel == mapped_base_color:
                # Overwrite the color in the pixel array
                pixel_array[c_counter] = mapped_color

            c_counter += 1

        # Generate surface from pixel array and save into the images directory
        image_saver(c_name, pixel_array.make_surface())