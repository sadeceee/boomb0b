import os
import ConfigParser
from helpers import *
from box import bomb

class player(object):
    """
    draw(screen, x, y), load(dir, filename), move_up(), move_down(), move_right(), move_left(), stop(), createBomb(), resetBomb()
    """
    image = None
    rect = None
    isWall = False
    breakable = True
    deadly = False
    putBomb = False

    # Moving keys
    K_BOMB  = -1
    K_UP    = -1
    K_DOWN  = -1
    K_RIGHT = -1
    K_LEFT  = -1

    """
    keyMapping: None for KI
                Else section name in keymapping, like 'player1'
    """
    def __init__(self, keyMapping = None):
        self.bombSize = 2
        self.bombCount = 2
        self.y_runSpeed = 0
        self.x_runSpeed = 0

        if (keyMapping != None):
            self.loadKeys(keyMapping)
            self.load("IMG", "player.png")
        else:
            self.load("IMG", "KI.png")

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)

    def loadKeys(self, keyMapping):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join("DATA", "keymapping.ini"))
        self.K_BOMB  = config.getint(keyMapping, "bomb")
        self.K_UP    = config.getint(keyMapping, "up")
        self.K_DOWN  = config.getint(keyMapping, "down")
        self.K_RIGHT = config.getint(keyMapping, "right")
        self.K_LEFT  = config.getint(keyMapping, "left")

    def move_up(self):
        if self.x_runSpeed == 0:
            self.y_runSpeed = -1

    def move_down(self):
        if self.x_runSpeed == 0:
            self.y_runSpeed = 1

    def move_right(self):
        if self.y_runSpeed == 0:
            self.x_runSpeed = 1

    def move_left(self):
        if self.y_runSpeed == 0:
            self.x_runSpeed = -1

    def stop(self):
        self.y_runSpeed = 0
        self.x_runSpeed = 0

    def createBomb(self):
        self.putBomb = True

    def resetBomb(self):
        self.putBomb = False

    def destroy(self, gf, x, y):
        gf.rem(self, x, y)

    def update(self, gf, x, y):
        # Put bomb
        if self.putBomb:
            #putBomb = False
            self.resetBomb()
            bomb(gf, self.bombSize, x, y)

        # Move player
        list = gf.checkPosition(x+self.x_runSpeed, y+self.y_runSpeed)
        w = False
        for i in list:
            obj, isWall, isBreakable, isDeadly = i

            if isWall:
                w = True

        if not w:
            gf.move(self, x+self.x_runSpeed, y+self.y_runSpeed, x, y)
            self.x_runSpeed = 0
            self.y_runSpeed = 0

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.K_UP:
                self.move_up()
            elif event.key == self.K_DOWN:
                self.move_down()
            elif event.key == self.K_RIGHT:
                self.move_right()
            elif event.key == self.K_LEFT:
                self.move_left()
            if event.key == self.K_BOMB:
                self.createBomb()
        if event.type == pygame.KEYUP:
            if event.key == self.K_UP:
                self.stop()
            elif event.key == self.K_DOWN:
                self.stop()
            elif event.key == self.K_RIGHT:
                self.stop()
            elif event.key == self.K_LEFT:
                self.stop()
            if event.key == self.K_BOMB:
                self.resetBomb()

class KI(player):
    """

    """
    def __init__(self):
        super(KI, self).__init__()

    def update(self, gf, x, y):
        pass

    def handleEvent(self, event):
        pass