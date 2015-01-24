from helpers import *
from constants import *
import pygame

class box(object):
    image = None
    rect = None
    isWall = False
    breakable = False
    deadly = False

    def __init__(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)
        self.rect = self.image.get_rect()

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
        if(self.counter > BOMB_TIMER):
            explosion(gf, self.bombSize, EXP_CENTER, x, y)
            return True
        return False

class explosion(box):
    size = 0
    counter = 0
    direction = EXP_CENTER

    # @param center: boolean, is explosion in center
    # @param size: size left to expand (e.g. 2 = can expand 2 more times
    def __init__(self, gf, size, direction, x, y):
        super(explosion, self).__init__()

        self.isWall = False
        self.breakable = False
        self.deadly = True
        self.size = size
        self.direction = direction
        if self.direction == EXP_CENTER:
            self.load("IMG", "dummy.bmp") # TODO center explosion image
        else: self.load("IMG", "dummy.bmp") # TODO expanded explosion image

        gf.add(self, x, y)

    def update(self, gf, x, y):
        if(size > 0):
            self.counter += 1
            if(self.counter > EXPLOSION_EXPAND):
                self.expand(gf, size, x, y)
            return False
        return False


    def expand(self, gf, size, x, y):
        if(self.direction == EXP_CENTER):
            list = [[0, -1], [1, 0], [0, 1], [-1, 0]]
            for z in list:
                newX = x + list[0]
                newY = y + list[1]
                check_expand(gf, size, self.direction, newX, newY)
        elif(self.direction == EXP_UP):
            newX = x
            newY = y -1
            check_expand(gf, size, self.direction, newX, newY)
        elif(self.direction == EXP_RIGHT):
            newX = x + 1
            newY = y
            check_expand(gf, size, self.direction, newX, newY)
        elif(self.direction == EXP_DOWN):
            newX = x
            newY = y + 1
            check_expand(gf, size, self.direction, newX, newY)
        elif(self.direction == EXP_LEFT):
            newX = x - 1
            newY = y
            check_expand(gf, size, self.direction, newX, newY)


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