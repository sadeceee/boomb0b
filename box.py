from helpers import *
from constants import *
from timer import *


class box(object, timer):
    """
    draw(screen, x, y), load(dir, filename), update(gf, x, y), handleEvent(event)
    """
    image = None
    isWall = False
    isBomb = False
    isItem = False
    breakable = False
    deadly = False
    isPlayer = False



    def __init__(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)
        self.load_timer(0)

    def update(self, gf, x, y):
        pass

    def tick(self):
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

    crateItem = False

    def __init__(self, item):
        super(crate, self).__init__()

        self.isWall = True
        self.breakable = True
        self.crateItem = item

        self.crate_anim = []
        self.count = 1
        self.des = False
        self.ANIMATION_SPEED = 4
        self.load("IMG", "crate.png")

    def update(self, gf, x, y):
        if self.des == True:
            gf.rem(self, x, y)
            if self.crateItem:
                gf.add(self.crateItem, x, y)

    def load(self, dir, filename):
        sprite_sheet = image_loader(dir, filename)

        loadhelper(sprite_sheet, [0, 1, 2], self.crate_anim, False)

        self.load_timer(self.ANIMATION_SPEED)
        self.timer_stop()
        self.image = self.crate_anim[0]

    def destroy(self, gf, x, y):
        self.timer_start()

    def tick(self):
        if self.count <= 2:
            self.image = self.crate_anim[self.count]
        elif self.count > 3:
            self.count = 0
            self.des = True
        self.count += 1

class bomb(box):
    """
    update(gf, x, y)
    """
    bombSize = 0
    counter = 0
    mPlayer = None
    def __init__(self, gf, player, mySize, x, y):
        super(bomb, self).__init__()

        self.isWall = True
        self.isBomb = True
        self.breakable = True
        self.bombSize = mySize
        self.mPlayer = player
        self.load("IMG", "bomb.png")

        gf.add(self, x, y)

    def update(self, gf, x, y):
        self.counter += 1
        if(self.counter == BOMB_TIMER):
            self.mPlayer.giveBomb()
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

            self.filename_anim.blit(raw_image, (0,0), (type * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
            image_saver(type, self.filename_anim)
        else: self.filename_anim = temp_pic

        self.filename_anim = pygame.transform.rotate(self.filename_anim, direction)

        self.image = self.filename_anim
        self.load_timer(0)

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
            self.check_center(keyList, gf, x, y)
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

    def check_center(self, keyList, gf, x, y):
        key = ""
        key = key.join(keyList)
        myType, myDirection = get_center_value(key)
        if((myType and myDirection) or myType == 0):
            self.load("IMG", "bomb_animation.png", myType, myDirection)
        list = gf.checkPosition(x, y)
        for item in list:
            obj, isWall, isBomb, isItem, isBreakable, isDeadly, isPlayer = item
            if isBreakable:
                obj.destroy(gf, x, y)

    def check_expand(self, gf, direction, newX, newY):
        list = gf.checkPosition(newX, newY)
        w = False
        for x in list:
            obj, isWall, isBomb, isItem, isBreakable, isDeadly, isPlayer = x

            if isWall:
                w = True
            if isBreakable:
                if isBomb:
                    obj.counter = 89
                else:
                    obj.destroy(gf, newX, newY)
            
            # Zerstoerung von Objekten PE
            # Zerstoert den Spieler auch wenn er auf der Bombe steht
            # Leider manchmal auch zwei Kisten hintereinander -> TODO
            
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

        #if not w:
        #    explosion(gf, s - 1, timeLeft, direction, newX, newY)

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