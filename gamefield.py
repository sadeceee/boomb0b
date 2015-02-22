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
    wall = []
    c_screen = None

    def __init__(self, screen):
        random.seed()
        self.fields = map_loader("MAP", "default.map")

        self.player_list = []

        self.map = []
        row = [0] * FIELDS_X
        for i in range(FIELDS_Y):
            self.map.append(list(row))

        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                nx = x * FIELD_SIZE_WIDTH
                ny = y * FIELD_SIZE_HEIGHT
                mValue = self.fields[y][x]
                self.fields[y][x] = []
                self.fields[y][x].append(boden(nx, ny))
                if mValue == '1':
                    self.fields[y][x] = [] # remove boden
                    self.fields[y][x].append(stone(nx, ny))
                    self.map[y][x] = 1
                elif mValue == '2':
                    rand = random.randint(2, 30)
                    if rand % 2 == 0:
                        self.fields[y][x].append(crate(nx, ny))
                        self.map[y][x] = 1
                elif mValue == '3':
                    self.player_list.append(player_x(nx, ny, "player1"))
                elif mValue == '4':
                    self.fields[y][x].append(bomb(self, 3, nx, ny))
                elif mValue == '5':
                    self.player_list.append(KI(nx, ny))
                elif mValue == '6':
                    self.player_list.append(player_x(nx, ny, "player2"))
                elif mValue == '7':
                    self.fields[y][x].append(bomb_item(nx, ny))
                elif mValue == '8':
                    self.fields[y][x].append(fire_item(nx, ny))
                elif mValue == '9':
                    self.fields[y][x].append(skull_item(nx, ny))

        self.c_screen = screen

    def draw(self):
        for obj_list1 in self.fields:
            for obj_list2 in obj_list1:
                for obj in obj_list2:
                    obj.draw(self.c_screen)

        for player in self.player_list:
            player.draw(self.c_screen)

    def update(self):
        for obj_list1 in self.fields:
            for obj_list2 in obj_list1:
                for obj in obj_list2:
                    if obj.update(self):
                        self.rem(obj)
                    if obj.tickable:
                        obj._tick()

        for player in self.player_list:
            if player.update(self):
                self.rem(obj)
            if player.tickable:
                player._tick()

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
                templist.append((obj, obj.isWall, obj.isBomb, obj.isItem, obj.breakable, obj.deadly))

            return templist

    def collisionWall(self, obj1):
        x = int(round((float(obj1.rect.x) / float(FIELD_SIZE_WIDTH))+0.49))
        y = int(round((float(obj1.rect.y) / float(FIELD_SIZE_HEIGHT))+0.49))

        dirX = 0
        dirY = 0

        if obj1.x_runSpeed > 0:
            dirX = 1
            x = int(round((float(obj1.rect.x) / float(FIELD_SIZE_WIDTH))-0.49))
        elif obj1.x_runSpeed < 0:
            dirX = -1
            x = int(round((float(obj1.rect.x) / float(FIELD_SIZE_WIDTH))+0.49))
        elif obj1.y_runSpeed > 0:
            dirY = 1
            y = int(round((float(obj1.rect.y) / float(FIELD_SIZE_HEIGHT))-0.49))
        elif obj1.y_runSpeed < 0:
            dirY = -1
            y = int(round((float(obj1.rect.y) / float(FIELD_SIZE_HEIGHT))+0.49))
        list = self.checkPosition(x+dirX, y+dirY)

        for i in list:
            obj, isWall, isBomb, isItem, isBreakable, isDeadly = i

            if isWall and obj1.rect.colliderect(obj.rect):
                if obj1.rect.colliderect(obj.rect):
                    obj1.rect.colliderect(obj.rect)
                    print "ja"
                return True
        return False


    def move(self, obj, to_x, to_y, x, y):
        if (0 <= to_x <= FIELDS_X - 1) and (0 <= to_y <= FIELDS_Y - 1):
           self.rem(obj, x, y)
           self.add(obj, to_x, to_y)

    def handleEvent(self, event):
        for y in range(FIELDS_Y):
            for x in range(FIELDS_X):
                for obj in self.fields[y][x]:
                    obj.handleEvent(event)

        for player in self.player_list:
            player.handleEvent(event)
