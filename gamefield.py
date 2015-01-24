from constants import *
from box import *

class gamefield:
    fields = []
    c_screen = None

    def __init__(self, screen):
        self.fields = map_loader("MAP", "default.map")
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                if(self.fields[y][x] == '1'):
                    self.fields[y][x] = stone()
                elif(self.fields[y][x] == '2'):
                    self.fields[y][x] = crate()
                else:
                    self.fields[y][x] = boden()

        self.c_screen = screen

    def draw(self):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                self.fields[y][x].draw(self.c_screen, (x*FIELD_SIZE_WIDTH), (y*FIELD_SIZE_HEIGHT))