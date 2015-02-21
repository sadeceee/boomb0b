from player import *
from box import *
from items import *
import random


class gamefield:
    """
    draw(), update(), add(nObject, x, y), rem(nObject, x, y), checkPosition(x, y), move(nObject, iX, iY, x, y),
    handleEvent(event)
    """
    fields = []
    c_screen = None

    def __init__(self, screen):
        itemList = [False, fire_item(), False, bomb_item(), False, skull_item(), False]
        random.seed()
        self.fields = map_loader("MAP", "default.map")

        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                mValue = self.fields[y][x]
                self.fields[y][x] = []
                self.fields[y][x].append(boden())
                if mValue == '1':
                    self.fields[y][x] = [] # remove boden
                    self.fields[y][x].append(stone())
                elif mValue == '2':
                    rand = random.randint(2, 30)
                    if rand % 2 == 0:
                        self.fields[y][x].append(crate(random.choice(itemList)))
                elif mValue == '3':
                    self.fields[y][x].append(player_x("player1"))
                elif mValue == '4':
                    self.fields[y][x].append(bomb(self, 3, x, y))
                elif mValue == '5':
                    self.fields[y][x].append(KI())
                elif mValue == '6':
                    self.fields[y][x].append(player_x("player2"))
                elif mValue == '7':
                    self.fields[y][x].append(bomb_item())
                elif mValue == '8':
                    self.fields[y][x].append(fire_item())
                elif mValue == '9':
                    self.fields[y][x].append(skull_item())

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
                    if obj.update(self, x, y):
                        self.rem(obj, x, y)

    def tick(self):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    if obj.tickable:
                        obj._tick()

    def add(self, obj, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            self.fields[y][x].append(obj)

    def rem(self, obj, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            self.fields[y][x].remove(obj)

    def checkPosition(self, x, y):
        if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
            templist = []
            for obj in self.fields[y][x]:
                templist.append((obj, obj.isWall, obj.isBomb, obj.isItem, obj.breakable, obj.deadly, obj.isPlayer))

            return templist

    # TOTALLY NOT NEEDED... I GUESS
    # def getObjectBreakable(self, x, y, pos):
    #     if (0 <= x <= FIELDS_X) and (0 <= y <= FIELDS_Y):
    #         return self.fields[y][x][pos]
    #     return False

    def move(self, obj, to_x, to_y, x, y):
        if (0 <= to_x <= FIELDS_X - 1) and (0 <= to_y <= FIELDS_Y - 1):
           self.rem(obj, x, y)
           self.add(obj, to_x, to_y)

    def handleEvent(self, event):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    obj.handleEvent(event)

    def generateMap(self, gobj):
        map = []
        row = [0] * FIELDS_X
        for i in range(FIELDS_Y):
            map.append(list(row))

        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    if gobj != obj:
                        try:
                            if obj.isPlayer:
                                map[y][x] = 4       # Player
                            elif obj.deadly:
                                map[y][x] = 3       # Toedlich
                            elif obj.breakable:
                                map[y][x] = 2       # Zerstoerbar
                            elif obj.isWall:
                                map[y][x] = 1       # Wall
                            else:
                                map[y][x] = 0       # Frei
                        except AttributeError:
                            map[y][x] = 0           # Frei
                    else:
                        map[y][x] = -1              # Objekt selbst

        return map