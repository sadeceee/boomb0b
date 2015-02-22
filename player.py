import os
import ConfigParser
import pygame
from constants import *
from helpers import image_loader, get_image, loadhelper
from timer import *
from box import bomb
from astar import *


class player(object, timer):
    """
    draw(screen, x, y), load(dir, filename), tick(), move_up(), move_down(), move_right(), move_left(), stop(), createBomb(), resetBomb(), destory()
    """
    image     = None
    rect      = None
    isWall    = False
    isBomb    = False
    isItem    = False
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

    def draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))

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

    # reduced move function with additional parameter
    # horizontal: is the movement horizontal (left or right) or not (vertical, face, back)
    def move_to_direction(self, direction, runspeed, horizontal):
        if horizontal:
            if self.y_runSpeed == 0:
                self.x_runSpeed = runspeed
                self.DIRECTION = direction
        else:
            if self.x_runSpeed == 0:
                self.y_runSpeed = runspeed
                self.DIRECTION = direction
        self.timer_start();

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
        #gf.rem(self, x, y)
        pass

    def increaseBombSize(self):
        self.bombSize += 1

    def increaseMaxBombs(self):
        self.maxBombs += 1
        self.bombs += 1

    def poisonPlayer(self):
        self.bombSize = 1
        self.maxBombs = 1
        self.bombs = min(self.bombs, 1)


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

    def __init__(self, posX, posY, keyMapping = None):
        super(player_x, self).__init__()

        self.posX = posX
        self.posY = posY

        self.loadKeys(keyMapping)
        self.load("IMG", "player.png")
        self.rect = pygame.Rect(self.posX+13, self.posY+12, FIELD_SIZE_WIDTH-26, FIELD_SIZE_HEIGHT-24)


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

    def update(self, gf):
        if not gf.collisionWall(self):
            self.posX = self.posX + self.x_runSpeed
            self.posY = self.posY + self.y_runSpeed
            self.rect.x = self.posX+13
            self.rect.y = self.posY+12
        #self.posX = self.posX + self.x_runSpeed
        #self.rect.x = self.posX

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
                self.move_to_direction("B", -PLAYER_RUNSPEED, False)
                self.image = self.WALKING_B[0]
            elif event.key == self.K_DOWN:
                self.move_to_direction("F", PLAYER_RUNSPEED, False)
                self.image = self.WALKING_F[0]
            elif event.key == self.K_RIGHT:
                self.move_to_direction("R", PLAYER_RUNSPEED, True)
                self.image = self.WALKING_R[0]
            elif event.key == self.K_LEFT:
                self.move_to_direction("L", -PLAYER_RUNSPEED, True)
                self.image = self.WALKING_L[0]
            if event.key == self.K_BOMB:
                self.createBomb()
        if event.type == pygame.KEYUP:
            if event.key in (self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT):
                self.stop()
                self.timer_stop()
            if event.key == self.K_BOMB:
                self.resetBomb()

class KI(player):
    """

    """

    path = ""

    def __init__(self, posX, posY):
        super(KI, self).__init__()

        self.posX = posX
        self.posY = posY
        self.dx = [1, 0, -1, 0]
        self.dy = [0, 1, 0, -1]


        self.load("IMG", "KI.png")
        self.rect = pygame.Rect(self.posX, self.posY, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT)
        self.timer_start()


    def update(self, gf):
        pass
        """
        # Move player
        list = gf.checkPosition(self.posX/64+self.x_runSpeed, self.posY/64+self.y_runSpeed)
        w = False
        d = False
        itemList = []
        for i in list:
            obj, isWall, isBomb, isItem, isBreakable, isDeadly = i

            if isWall:
                w = True
            if isDeadly:
                d = True
            if isItem:
                itemList.append(obj)

        if d:
            self.destroy(gf, self.posX, self.posY)
        else:
            if self.path != "2222":


                route = findPath(gf.map, 4, self.dx, self.dy, self.posX/64, self.posY/64, 5, 9)
                self.path = route.search()

            if not w:


                gf.move(self, self.posX+self.x_runSpeed, self.posY+self.y_runSpeed, self.posX, self.posY)

                for item in itemList:
                    CAUTION: when movement is changed, take care of new x, y values
                    self = item.destroyNew(gf, x+self.x_runSpeed, y+self.y_runSpeed, self)

                self.x_runSpeed = 0
                self.y_runSpeed = 0
        """


    def tick(self):
        direction = self.left(self.path, 1)


        if direction == "2":
            self.move_to_direction("L", -PLAYER_RUNSPEED, True)
        elif direction == "3":
            self.move_to_direction("B", -PLAYER_RUNSPEED, False)
        elif direction == "0":
            self.move_to_direction("R", PLAYER_RUNSPEED, True)
        elif direction == "1":
            self.move_to_direction("F", PLAYER_RUNSPEED, False)

        self.path = ""

    def handleEvent(self, event):
        pass

    def left(self, s, amount):
        return s[:amount]
