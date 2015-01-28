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
            explosion(gf, self.bombSize, -1, EXP_CENTER, x, y)
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
    direction = EXP_CENTER

    # @param myDir: boolean, is explosion in center
    # @param s: size left to expand (e.g. 2 = can expand 2 more times
    def __init__(self, gf, s, timeLeft, myDir, x, y):
        super(explosion, self).__init__()

        self.isWall = False
        self.breakable = False
        self.deadly = True
        self.mySize = s
        self.direction = myDir
        if self.direction == EXP_CENTER:
            self.timer = s * EXP_DURATION
            self.load("IMG", "bomb_animation.png") # TODO center explosion image
        else:
            self.timer = timeLeft
            self.load("IMG", "dummy.bmp") # TODO expanded explosion image

        gf.add(self, x, y)

    def load(self, dir, filename):
        temp_pic = image_test(FILENAME_I)
        if(temp_pic == False):
            raw_image = image_loader(dir, filename)
            self.filename_anim.blit(raw_image, (0,0), (6 * FIELD_SIZE_WIDTH, 0, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT))
            image_saver(FILENAME_I, self.filename_anim)
        else:
            self.filename_anim = temp_pic

        self.image = self.filename_anim

    def update(self, gf, x, y):
        self.timer -= 1
        if(self.timer <= 0):
            return True
        if(self.mySize > 0):
            self.counter += 1
            if(self.counter == EXPLOSION_EXPAND):
                self.expand(gf, self.mySize, x, y)
            return False
        return False

    def expand(self, gf, s, x, y):
        if(self.direction == EXP_CENTER):
            list = [[0, -1, EXP_UP], [1, 0, EXP_RIGHT], [0, 1, EXP_DOWN], [-1, 0, EXP_LEFT]]
            for z in list:
                newX = x + z[0]
                newY = y + z[1]
                check_expand(gf, s, self.timer, z[2], newX, newY)
        elif(self.direction == EXP_UP):
            newX = x
            newY = y -1
            check_expand(gf, s, self.timer, EXP_UP, newX, newY)
        elif(self.direction == EXP_RIGHT):
            newX = x + 1
            newY = y
            check_expand(gf, s, self.timer, EXP_RIGHT, newX, newY)
        elif(self.direction == EXP_DOWN):
            newX = x
            newY = y + 1
            check_expand(gf, s, self.timer, EXP_DOWN, newX, newY)
        elif(self.direction == EXP_LEFT):
            newX = x - 1
            newY = y
            check_expand(gf, s, self.timer, EXP_LEFT, newX, newY)

def check_expand(gf, s, timeLeft, direction, newX, newY):
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
                obj.counter == EXPLOSION_EXPAND
            else:
                gf.rem(obj, newX, newY)
        counter += 1

        # Zerstorung von Objekten PE
        # Zerstort den Spieler auch wenn er auf der Bombe steht
        # Leider manchmal auch zwei Kisten hintereinander -> TODO
        #if isBreakable:
        #    obj.destroy(gf, newX, newY)

    if not w:
        explosion(gf, s - 1, timeLeft, direction, newX, newY)

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