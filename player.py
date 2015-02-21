import os
import ConfigParser
import pygame
from constants import *
from helpers import image_loader, get_image, loadhelper
from timer import *
from box import bomb


class player(object, timer):
    """
    draw(screen, x, y), load(dir, filename), tick(), move_up(), move_down(), move_right(), move_left(), stop(), createBomb(), resetBomb(), destory()
    """
    image     = None
    rect      = None
    isWall    = False
    isBomb    = False
    breakable = True
    deadly    = False
    bombs     = PLAYER_MAX_BOMBS
    putBomb   = False

    def __init__(self):
        self.bombSize = PLAYER_BOMB_SIZE
        self.maxBombs = PLAYER_MAX_BOMBS
        self.y_runSpeed = 0
        self.x_runSpeed = 0

        self.DIRECTION = "F"
        self.WALKING_F = []
        self.WALKING_B = []
        self.WALKING_R = []
        self.WALKING_L = []
        self.frame = 0
        self.ANIMATION_SPEED = 10

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        sprite_sheet = image_loader(dir, filename)

        # Front
        loadhelper(sprite_sheet, [0, 1, 0, 2], self.WALKING_F, False)

        # Back
        loadhelper(sprite_sheet, [3, 4, 3, 5], self.WALKING_B, False)

        # Right
        loadhelper(sprite_sheet, [6, 7, 6, 8], self.WALKING_R, False)

        # Left
        loadhelper(sprite_sheet, [6, 7, 6, 8], self.WALKING_L, True)

        self.image = self.WALKING_F[0]
        self.load_timer(self.ANIMATION_SPEED)

    def tick(self):
        pass

    def move_up(self):
        if self.x_runSpeed == 0:
            self.y_runSpeed = -1
            self.DIRECTION = "B"

    def move_down(self):
        if self.x_runSpeed == 0:
            self.y_runSpeed = 1
            self.DIRECTION = "F"

    def move_right(self):
        if self.y_runSpeed == 0:
            self.x_runSpeed = 1
            self.DIRECTION = "R"

    def move_left(self):
        if self.y_runSpeed == 0:
            self.x_runSpeed = -1
            self.DIRECTION = "L"

    def stop(self):
        self.y_runSpeed = 0
        self.x_runSpeed = 0

    def createBomb(self):
        self.putBomb = True

    def resetBomb(self):
        self.putBomb = False

    def giveBomb(self):
        self.bombs = min(self.bombs + 1, self.maxBombs)

    def destroy(self, gf, x, y):
        gf.rem(self, x, y)


class player_x(player):
    """
    loadKeys(), update(), tick(), handleEvent()
    """
    # Moving keys
    K_BOMB    = -1
    K_UP      = -1
    K_DOWN    = -1
    K_RIGHT   = -1
    K_LEFT    = -1

    def __init__(self, keyMapping = None):
        super(player_x, self).__init__()

        self.loadKeys(keyMapping)
        self.load("IMG", "player.png")

        if (keyMapping != None):
            self.loadKeys(keyMapping)

    def loadKeys(self, keyMapping):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join("DATA", "keyMapping.ini"))
        self.K_BOMB  = config.getint(keyMapping, "bomb")
        self.K_UP    = config.getint(keyMapping, "up")
        self.K_DOWN  = config.getint(keyMapping, "down")
        self.K_RIGHT = config.getint(keyMapping, "right")
        self.K_LEFT  = config.getint(keyMapping, "left")

    def update(self, gf, x, y):

        # Move player
        list = gf.checkPosition(x+self.x_runSpeed, y+self.y_runSpeed)
        w = False
        d = False
        b = False
        for i in list:
            obj, isWall, isBomb, isBreakable, isDeadly = i

            if isWall:
                w = True
            if isDeadly:
                d = True
            if isBomb:
                b = True

        # Put bomb
        if self.putBomb:
            self.resetBomb()
            if (not b and self.bombs > 0):
                bomb(gf, self,  self.bombSize, x, y)
                self.bombs = max(self.bombs - 1, 0)
                return

        if d:
            self.destroy(gf, x, y)
        else:
            if(self.x_runSpeed != 0 or self.y_runSpeed != 0):
                if not w:
                    gf.move(self, x+self.x_runSpeed, y+self.y_runSpeed, x, y)
                    self.x_runSpeed = 0
                    self.y_runSpeed = 0

    def tick(self):
        # Animation
        if self.DIRECTION == "F":
            self.image = self.WALKING_F[self.frame]
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        elif self.DIRECTION == "B":
            self.image = self.WALKING_B[self.frame]
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        elif self.DIRECTION == "R":
            self.image = self.WALKING_R[self.frame]
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        elif self.DIRECTION == "L":
            self.image = self.WALKING_L[self.frame]
            self.frame += 1
            if self.frame > 3:
                self.frame = 0

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.K_UP:
                self.move_up()
                self.timer_start()
                self.image = self.WALKING_B[0]
            elif event.key == self.K_DOWN:
                self.move_down()
                self.timer_start()
                self.image = self.WALKING_F[0]
            elif event.key == self.K_RIGHT:
                self.move_right()
                self.timer_start()
                self.image = self.WALKING_R[0]
            elif event.key == self.K_LEFT:
                self.move_left()
                self.timer_start()
                self.image = self.WALKING_L[0]
            if event.key == self.K_BOMB:
                self.createBomb()
        if event.type == pygame.KEYUP:
            if event.key == self.K_UP:
                self.stop()
                self.timer_stop()
            elif event.key == self.K_DOWN:
                self.stop()
                self.timer_stop()
            elif event.key == self.K_RIGHT:
                self.stop()
                self.timer_stop()
            elif event.key == self.K_LEFT:
                self.stop()
                self.timer_stop()
            if event.key == self.K_BOMB:
                self.resetBomb()

class KI(player):
    """

    """

    def __init__(self):
        super(KI, self).__init__()

        self.load("IMG", "KI.png")

    def update(self, gf, x, y):
        pass

    def handleEvent(self, event):
        pass