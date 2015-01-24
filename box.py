from helpers import *
from constants import *
import pygame

class box(object):
    image = None
    isWall = False
    breakable = False
    deadly = False

    def __init__(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)

    def update(self, gf, x, y):
        pass

class stone(box):

    def __init__(self):
        super(stone, self).__init__()

        self.isWall = True
        self.breakable = False

        self.load("IMG", "stone.bmp")


class crate(box):

    def __init__(self):
        super(crate, self).__init__()

        self.isWall = True
        self.breakable = True

        self.load("IMG", "crate.bmp")


class bomb(box):
    bombSize = 0
    counter = 0
    def __init__(self, size):
        super(bomb, self).__init__()

        self.isWall = True
        self.breakable = False
        self.bombSize = size
        self.load("IMG", "bomb.bmp")

    def update(self, x, y):
        self.counter += 1
        if(self.counter > BOMB_TIMER):
            explosion(True, x, y)
            return True
        return False

class explosion(box):
    counter = 0

    # @param center: boolean, is explosion in center
    def __init__(self, center, x, y):
        super(explosion, self).__init__()

        self.isWall = False
        self.breakable = False
        self.deadly = True
        if center:
            self.load("IMG", "dummy.bmp") # TODO center explosion image
        else: self.load("IMG", "dummy.bmp") # TODO expanded explosion image

        gf.add(self, x, y)

    def update(self, gf, x, y):
        self.counter += 1
        if(self.counter > EXPLOSION_EXPAND):
            self.expand(gf, x, y)

    # list: [up, right, down, left)
    # example: [False, True, True, False]
    def expand(self, gf, x, y):
        list = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        for z in list:
            newX = x + list[0]
            newY = y + list[1]
            isWall, isBreakable, isDeadly = gf.checkPosition(newX, newY)
            if not isWall:
                explosion(False, newX, newY)
            # TODO check isBreakable




class dummy(box):

    def __init__(self):
        super(dummy, self).__init__()

        self.isWall = False
        self.breakable = False

        self.load("IMG", "dummy.bmp")

class boden(box):

    def __init__(self):
        super(boden, self).__init__()

        self.isWall = False
        self.breakable = False

        self.load("IMG", "boden.bmp")