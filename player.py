import os
import ConfigParser
import pygame
import random
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
    isPlayer  = True
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
        """ CAUTION: when movement is changed, take care of new x, y values """
        list = gf.checkPosition(x+self.x_runSpeed, y+self.y_runSpeed)
        w = False
        d = False
        b = False
        itemList = []
        for i in list:
            obj, isWall, isBomb, isItem, isBreakable, isDeadly, isPlayer = i

            if isWall:
                w = True
            if isDeadly:
                d = True
            if isBomb:
                b = True
            if isItem:
                itemList.append(obj)

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

                    for item in itemList:
                        """ CAUTION: when movement is changed, take care of new x, y values """
                        self = item.destroyNew(gf, x+self.x_runSpeed, y+self.y_runSpeed, self)

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

    # KI Type constants
    KI_TERMINATOR   = 0
    KI_AGGRO        = 1
    KI_ITEM         = 2
    KI_DUMMY        = 3

    # KI Direction constants
    KI_LEFT         = "2"
    KI_UP           = "3"
    KI_RIGHT        = "0"
    KI_DOWN         = "1"

    def __init__(self):
        super(KI, self).__init__()

        self.dx = [1, 0, -1, 0]
        self.dy = [0, 1, 0, -1]

        self.Type = random.choice([KI.KI_TERMINATOR, KI.KI_AGGRO, KI.KI_ITEM, KI.KI_DUMMY])

        self.desX = None
        self.desY = None
        self.seqDesX = None
        self.seqDesY = None

        self.map = []

        self.pathToDes  = ""
        self.pathSeq    = ""

        self.counter = 0

        self.load("IMG", "KI.png")
        self.timer_start()

    def selectDestination(self):
        self.pathToDes = ""

        if self.Type == KI.KI_TERMINATOR:
            # Get next player
            for y in range(FIELDS_Y):
                for x in range(FIELDS_X):
                    if self.map[y][x] == 4:
                        self.desX = x
                        self.desY = y
                        return

        if self.Type == KI.KI_ITEM or self.Type == KI.KI_AGGRO:
            # Get next/random crate
            while self.desX == None and self.desY == None:
                nX = random.randint(1, 9)
                nY = random.randint(1, 9)

                if self.map[nY][nX] == 2:
                    self.desX = nX
                    self.desY = nY
                    return

        if self.Type == KI.KI_DUMMY:
            # Get random free position
            while self.desX == None and self.desY == None:
                nX = random.randint(1, 9)
                nY = random.randint(1, 9)

                if self.map[nY][nX] == 0:
                    self.desX = nX
                    self.desY = nY
                    return

    def update(self, gf, x, y):
        if self.counter >= TICKS/2:
            # Update map
            self.map = gf.generateMap(self)

            # Select new destination if none is set
            if self.desX == None or self.desY == None or (x == self.desX and y == self.desY):
                self.selectDestination()

            # Calculate path to destination
            if self.pathToDes == "":
                route = findPath(self.map, 4, self.dx, self.dy, x, y, self.desX, self.desY)
                self.pathToDes = route.search()


            print "Ziel: " + str(self.desX) + ", " + str(self.desY)
            print "Posi: " + str(x) + ", " + str(y)

            # Get the next direction
            self.pathToDes, direction = self.left(self.pathToDes, 1)

            # Map direction
            dirX = 0
            dirY = 0
            if direction == KI.KI_LEFT:
                dirX = -1
            elif direction == KI.KI_UP:
                dirY = -1
            elif direction == KI.KI_RIGHT:
                dirX = +1
            elif direction == KI.KI_DOWN:
                dirY = +1

            # Check if there is an breakable crate
            list = gf.checkPosition(x+dirX, y+dirY)

            w = False
            d = False
            ba = False
            b = False

            itemList = []
            for i in list:
                obj, isWall, isBomb, isItem, isBreakable, isDeadly, isPlayer = i

                if isWall:
                    w = True
                if isDeadly:
                    d = True
                if isBreakable:
                    ba = True
                if isBomb:
                    b = True
                if isItem:
                    itemList.append(obj)

            # Take action on check
            #if d:
            #    self.destroy(gf, x, y)
            #else:

            # Test if we can put an bomb and wait for it
            if w and ba:
                # Put an bomb
                self.createBomb()
                # And add the direction to the pathToDest on first place
                self.pathToDes = direction + self.pathToDes

            else:
                # Move in direction
                gf.move(self, x+dirX, y+dirY, x, y)

                for item in itemList:
                    """ CAUTION: when movement is changed, take care of new x, y values """
                    self = item.destroyNew(gf, x+dirX, y+dirY, self)

            # Put bomb
            if self.putBomb:
                self.resetBomb()
                if (not b and self.bombs > 0):
                    bomb(gf, self,  self.bombSize, x, y)
                    self.bombs = max(self.bombs - 1, 0)
                    return

            self.counter = 0
        else:
            self.counter += 1

    def handleEvent(self, event):
        pass

    def left(self, s, amount):
        c = s[:amount]
        s = s[amount:]
        return (s, c)
