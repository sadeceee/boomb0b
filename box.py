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

    def handleEvent(self, event):
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
    def __init__(self, gf, mySize, x, y):
        super(bomb, self).__init__()

        self.isWall = True
        self.breakable = False
        self.bombSize = mySize
        self.load("IMG", "bomb.png")

        gf.add(self, x, y)

    def update(self, gf, x, y):
        self.counter += 1
        if(self.counter == BOMB_TIMER):
            explosion(gf, self.bombSize, EXP_CENTER, x, y)
            return False
        return False

class explosion(box):
    mySize = 0
    counter = 0
    direction = EXP_CENTER

    # @param center: boolean, is explosion in center
    # @param size: size left to expand (e.g. 2 = can expand 2 more times
    def __init__(self, gf, s, myDir, x, y):
        super(explosion, self).__init__()

        self.isWall = False
        self.breakable = False
        self.deadly = True
        self.mySize = s
        self.direction = myDir
        if self.direction == EXP_CENTER:
            self.load("IMG", "dummy.bmp") # TODO center explosion image
        else: self.load("IMG", "dummy.bmp") # TODO expanded explosion image

        gf.add(self, x, y)

    def update(self, gf, x, y):
        if(self.mySize > 0):
            self.counter += 1
            if(self.counter == EXPLOSION_EXPAND):
                self.expand(gf, self.mySize, x, y)
            return False
        return False


    def expand(self, gf, s, x, y):
        if(self.direction == EXP_CENTER):
            list = [[0, -1, EXP_UP], [1, 0, EXP_RIGHT], [0, 1, EXP_DOWN], [-1, 0, EXP_LEFT]]
            for z in list:
                newX = x + z[0]
                newY = y + z[1]
                check_expand(gf, s, z[2], newX, newY)
        elif(self.direction == EXP_UP):
            newX = x
            newY = y -1
            check_expand(gf, s, EXP_UP, newX, newY)
        elif(self.direction == EXP_RIGHT):
            newX = x + 1
            newY = y
            check_expand(gf, s, EXP_RIGHT, newX, newY)
        elif(self.direction == EXP_DOWN):
            newX = x
            newY = y + 1
            check_expand(gf, s, EXP_DOWN, newX, newY)
        elif(self.direction == EXP_LEFT):
            newX = x - 1
            newY = y
            check_expand(gf, s, EXP_LEFT, newX, newY)

def check_expand(gf, s, direction, newX, newY):
    list = gf.checkPosition(newX, newY)
    w = False
    for x in list:
        isWall, isBreakable, isDeadly = x

        if isWall:
            w = True

    if not w:
        explosion(gf, s - 1, direction, newX, newY)
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