from constants import *
from box import *

class gamefield:
    fields = []
    c_screen = None

    def __init__(self, screen):
        for y in range(FIELDS_Y):
            self.fields.append(FIELDS_X * [dummy()])

        self.c_screen = screen

    def draw(self):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                self.fields[y][x].draw(self.c_screen, (x*FIELD_SIZE_WIDTH), (y*FIELD_SIZE_HEIGHT))