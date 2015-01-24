from player import *
from box import *
import random

class gamefield:
    """
    draw(), update(), add(nObject, x, y), rem(nObject, x, y), checkPosition(x, y), move(nObject, iX, iY, x, y), handleEvent(event)
    """
    fields = []
    c_screen = None

    def __init__(self, screen):
        random.seed()
        self.fields = map_loader("MAP", "default.map")
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                if(self.fields[y][x] == '1'):
                    self.fields[y][x] = []
                    self.fields[y][x].append(stone())
                elif(self.fields[y][x] == '2'):
                    iRandom = random.randint(2, 30)
                    if (iRandom % 2 == 0):
                        self.fields[y][x] = []
                        self.fields[y][x].append(boden())
                        self.fields[y][x].append(crate())
                    else:
                        self.fields[y][x] = []
                        self.fields[y][x].append(boden())
                elif(self.fields[y][x] == '3'):
                    self.fields[y][x] = []
                    self.fields[y][x].append(boden())
                    self.fields[y][x].append(player_1())
                elif(self.fields[y][x] == '4'):
                    self.fields[y][x] = []
                    self.fields[y][x].append(boden())
                    self.fields[y][x].append(bomb(self, 3, x, y))
                elif(self.fields[y][x] == '5'):
                    self.fields[y][x] = []
                    self.fields[y][x].append(boden())
                    self.fields[y][x].append(KI())
                else:
                    self.fields[y][x] = []
                    self.fields[y][x].append(boden())

        self.c_screen = screen

    def draw(self):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    obj.draw(self.c_screen, (x*FIELD_SIZE_WIDTH), (y*FIELD_SIZE_HEIGHT))

    def update(self):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    if (obj.update(self, x, y) == True):
                        self.rem(obj, x, y)

    def add(self, nObject, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            self.fields[y][x].append(nObject)

    def rem(self, nObject, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            self.fields[y][x].remove(nObject)

    def checkPosition(self, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            tempList = []
            for obj in self.fields[y][x]:
                tempList.append((obj.isWall, obj.breakable, obj.deadly))

        return tempList

    def getObjectBreakable(self, x, y, pos):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            return self.fields[y][x][pos]
        return False

    def move(self, nObject, iX, iY, x, y):
        if (0 <= iX <= FIELDS_X - 1) and (0 <= iY <= FIELDS_Y - 1):
           self.rem(nObject, x, y)
           self.add(nObject, iX, iY)

    def handleEvent(self, event):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    obj.handleEvent(event)