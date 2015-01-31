import os
import ConfigParser
import pygame
from constants import *
from helpers import image_loader, get_image
from timer import *
from box import bomb


class player(object, timer):
    """
    draw(screen, x, y), load(dir, filename), move_up(), move_down(), move_right(), move_left(), stop(), createBomb(), resetBomb()
    """
    image     = None
    rect      = None
    isWall    = False
    isBomb    = False
    breakable = True
    deadly    = False
    putBomb   = False

    def __init__(self):
        self.bombSize = 2
        self.bombCount = 2
        self.y_runSpeed = 0
        self.x_runSpeed = 0

        self.load_timer(0)

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)

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

    def destroy(self, gf, x, y):
        gf.rem(self, x, y)


class player_x(player):
    # Moving keys
    K_BOMB    = -1
    K_UP      = -1
    K_DOWN    = -1
    K_RIGHT   = -1
    K_LEFT    = -1

    def __init__(self, keyMapping = None):
        super(player_x, self).__init__()

        self.DIRECTION = "F"
        self.WALKING_F = []
        self.WALKING_B = []
        self.WALKING_R = []
        self.WALKING_L = []

        self.loadKeys(keyMapping)
        self.load("IMG", "player.png")

        if (keyMapping != None):
            self.loadKeys(keyMapping)

    def load(self, dir, filename):
        sprite_sheet = image_loader(dir, filename)

        # Front
        image = get_image(sprite_sheet, 0 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_F.append(image)
        image = get_image(sprite_sheet, 1 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_F.append(image)
        image = get_image(sprite_sheet, 0 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_F.append(image)
        image = get_image(sprite_sheet, 2 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_F.append(image)

        # Back
        image = get_image(sprite_sheet, 3 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_B.append(image)
        image = get_image(sprite_sheet, 4 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_B.append(image)
        image = get_image(sprite_sheet, 3 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_B.append(image)
        image = get_image(sprite_sheet, 5 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_B.append(image)

        # Right
        image = get_image(sprite_sheet, 6 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_R.append(image)
        image = get_image(sprite_sheet, 7 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_R.append(image)
        image = get_image(sprite_sheet, 6 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_R.append(image)
        image = get_image(sprite_sheet, 8 * FIELD_SIZE_WIDTH, 0)
        self.WALKING_R.append(image)

        # Left
        image = get_image(sprite_sheet, 6 * FIELD_SIZE_WIDTH, 0)
        image = pygame.transform.flip(image, True, False)
        self.WALKING_L.append(image)
        image = get_image(sprite_sheet, 7 * FIELD_SIZE_WIDTH, 0)
        image = pygame.transform.flip(image, True, False)
        self.WALKING_L.append(image)
        image = get_image(sprite_sheet, 6 * FIELD_SIZE_WIDTH, 0)
        image = pygame.transform.flip(image, True, False)
        self.WALKING_L.append(image)
        image = get_image(sprite_sheet, 8 * FIELD_SIZE_WIDTH, 0)
        image = pygame.transform.flip(image, True, False)
        self.WALKING_L.append(image)

        self.image = self.WALKING_F[0]

    def loadKeys(self, keyMapping):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join("DATA", "keyMapping.ini"))
        self.K_BOMB  = config.getint(keyMapping, "bomb")
        self.K_UP    = config.getint(keyMapping, "up")
        self.K_DOWN  = config.getint(keyMapping, "down")
        self.K_RIGHT = config.getint(keyMapping, "right")
        self.K_LEFT  = config.getint(keyMapping, "left")

    def update(self, gf, x, y):
        # Put bomb
        if self.putBomb:
            self.resetBomb()
            bomb(gf, self.bombSize, x, y)

        # Move player
        list = gf.checkPosition(x+self.x_runSpeed, y+self.y_runSpeed)
        w = False
        for i in list:
            obj, isWall, isBomb, isBreakable, isDeadly = i

            if isWall:
                w = True

        if not w:
            gf.move(self, x+self.x_runSpeed, y+self.y_runSpeed, x, y)
            self.x_runSpeed = 0
            self.y_runSpeed = 0

        # Animation
        if self.DIRECTION == "F":
            frame = y % len(self.WALKING_F)
            self.image = self.WALKING_F[frame]
        elif self.DIRECTION == "B":
            frame = y % len(self.WALKING_F)
            self.image = self.WALKING_B[frame]
        elif self.DIRECTION == "R":
            frame = x % len(self.WALKING_F)
            self.image = self.WALKING_R[frame]
        elif self.DIRECTION == "L":
            frame = x % len(self.WALKING_F)
            self.image = self.WALKING_L[frame]

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

        self.load("IMG", "KI.png")


    def update(self, gf, x, y):
        pass

    def handleEvent(self, event):
        pass