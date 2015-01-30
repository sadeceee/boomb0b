from helpers import *
from constants import *

class box(object):
    """
    draw(screen, x, y), load(dir, filename), update(gf, x, y), handleEvent(event)
    """
    image = None
    isWall = False
    isBomb = False
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

    def destroy(self, gf, x, y):
        gf.rem(self, x, y)

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
    """
    update(gf, x, y)
    """
    bombSize = 0
    counter = 0
    def __init__(self, gf, mySize, x, y):
        super(bomb, self).__init__()

        self.isWall = True
        self.isBomb = True
        self.breakable = True
        self.bombSize = mySize
        self.load("IMG", "bomb.png")

        gf.add(self, x, y)

    def update(self, gf, x, y):
        self.counter += 1
        if(self.counter == BOMB_TIMER):
            explosion(gf, self.bombSize, -1, EXP_INITIAL, EXP_INITIAL, x, y)
            return True
        return False

class explosion(box):
    """
    update(gf, x, y), expand(gf, s, x, y)
    """
    filename_anim = pygame.Surface((FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))

    mySize = 0
    counter = 0
    timer = 0
    type = EXP_INITIAL
    direction = EXP_INITIAL

    # @param myDir: boolean, is explosion in center
    # @param s: size left to expand (e.g. 2 = can expand 2 more times
    def __init__(self, gf, s, timeLeft, type, myDir, x, y):
        super(explosion, self).__init__()

        self.isWall = False
        self.breakable = False
        self.deadly = True
        self.mySize = s
        self.type = type
        self.direction = myDir
        if self.direction == EXP_INITIAL:
            self.timer = (s + 1) * EXP_DURATION
        else:
            self.timer = timeLeft

        self.load("IMG", "bomb_animation.png", self.type, self.direction)

        gf.add(self, x, y)

    def load(self, dir, filename, type, direction):
        self.filename_anim = pygame.Surface((FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
        temp_pic = image_test(type)

        if(temp_pic == False):
            raw_image = image_loader(dir, filename)
            if(type == EXP_INITIAL):
                self.filename_anim.blit(raw_image, (0,0), (6 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_INITIAL, self.filename_anim)
            elif(type == EXP_CENTER_X):
                self.filename_anim.blit(raw_image, (0,0), (4 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_CENTER_X, self.filename_anim)
            elif(type == EXP_CENTER_T):
                self.filename_anim.blit(raw_image, (0,0), (5 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_CENTER_T, self.filename_anim)
            elif(type == EXP_CENTER_L):
                self.filename_anim.blit(raw_image, (0,0), (3 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_CENTER_L, self.filename_anim)
            elif(type == EXP_CENTER_B):
                self.filename_anim.blit(raw_image, (0,0), (1 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_CENTER_B, self.filename_anim)
            elif(type == EXP_CENTER_U):
                self.filename_anim.blit(raw_image, (0,0), (0 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_CENTER_U, self.filename_anim)
            elif(type == EXP_BRIDGE):
                self.filename_anim.blit(raw_image, (0,0), (1 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_BRIDGE, self.filename_anim)
            elif(type == EXP_END):
                self.filename_anim.blit(raw_image, (0,0), (2 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
                image_saver(EXP_END, self.filename_anim)
        else: self.filename_anim = temp_pic

        if(direction == EXP_UP):
            pass
        elif(direction == EXP_RIGHT):
            self.filename_anim = pygame.transform.rotate(self.filename_anim, -90)
        elif(direction == EXP_DOWN):
            self.filename_anim = pygame.transform.rotate(self.filename_anim, 180)
        elif(direction == EXP_LEFT):
            self.filename_anim = pygame.transform.rotate(self.filename_anim, 90)

        self.image = self.filename_anim

    def update(self, gf, x, y):
        self.timer -= 1
        if(self.timer <= 0):
            return True
        if(self.mySize > 0):
            self.counter += 1
            if(self.counter == EXPLOSION_EXPAND):
                self.expand(gf, x, y)
            return False
        return False

    def expand(self, gf, x, y):
        if(self.direction == EXP_INITIAL):
            list = [[0, -1, EXP_UP], [1, 0, EXP_RIGHT], [0, 1, EXP_DOWN], [-1, 0, EXP_LEFT]]
            keyList = []
            for z in list:
                newX = x + z[0]
                newY = y + z[1]
                key = self.check_expand(gf, z[2], newX, newY)
                keyList.append(key)
            self.check_center(keyList)
        elif(self.direction == EXP_UP):
            newX = x
            newY = y -1
            self.check_expand(gf, EXP_UP, newX, newY)
        elif(self.direction == EXP_RIGHT):
            newX = x + 1
            newY = y
            self.check_expand(gf, EXP_RIGHT, newX, newY)
        elif(self.direction == EXP_DOWN):
            newX = x
            newY = y + 1
            self.check_expand(gf, EXP_DOWN, newX, newY)
        elif(self.direction == EXP_LEFT):
            newX = x - 1
            newY = y
            self.check_expand(gf, EXP_LEFT, newX, newY)

    def check_center(self, keyList):
        key = ""
        key = key.join(keyList)
        myType, myDirection = get_center_value(key)
        if(myType and myDirection):
            self.load("IMG", "bomb_animation.png", myType, myDirection)

    def check_expand(self, gf, direction, newX, newY):
        list = gf.checkPosition(newX, newY)
        w = False
        counter = 0
        for x in list:
            obj, isWall, isBomb, isBreakable, isDeadly = x

            if isWall:
                w = True
            if isBreakable:
                obj = gf.getObjectBreakable(newX, newY, counter)
                if isBomb:
                    obj.counter = 80
                else:
                    gf.rem(obj, newX, newY)
            counter += 1
            
            # Zerstoerung von Objekten PE
            # Zerstoert den Spieler auch wenn er auf der Bombe steht
            # Leider manchmal auch zwei Kisten hintereinander -> TODO
            #if isBreakable:
            #    obj.destroy(gf, newX, newY)
        if not w:
            tempType = EXP_CENTER_X
            if(self.type == EXP_INITIAL): # TODO check for Center types as well
                tempType = EXP_END
            elif(self.type == EXP_END):
                self.load("IMG", "bomb_animation.png", EXP_BRIDGE, self.direction)
                tempType = EXP_END
            explosion(gf, self.mySize - 1, self.timer, tempType, direction, newX, newY)
            # TODO check isBreakable
            return "1"
        return "0"


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