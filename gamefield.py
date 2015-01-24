from constants import *

class gamefield:
    fields = []

    def __init__(self):
        for y in range(FIELDS_Y):
            self.fields.append(FIELDS_X * [None])