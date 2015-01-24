from helpers import *
from box import stone, crate, bomb

class player(object):
    """
    draw(screen, x, y), load(dir, filename)
    """
    image = None
    rect = None
    isWall = False
    breakable = True
    deadly = False
    putBomb = False

    def __init__(self):
        self.bombSize = 2
        self.bombCount = 2
        self.y_runSpeed = 0
        self.x_runSpeed = 0

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        self.image = image_loader(dir, filename)

class player_1(player):
    """
    update(gf, x, y), handleEvent(event), move_up(), move_down(), move_right(), move_left(), stop(), createBomb(), resetBomb()
    """
    def __init__(self):
        super(player_1, self).__init__()

        self.load("IMG", "player.png")

    def update(self, gf, x, y):
        # Put bomb
        if self.putBomb:
            #putBomb = False
            self.resetBomb()
            bomb(gf, self.bombSize, x, y)

        # Move player
        list = gf.checkPosition(x+self.x_runSpeed, y+self.y_runSpeed)
        w = False
        for i in list:
            isWall, isBreakable, isDeadly = i

            if isWall:
                w = True

        if not w:
            gf.move(self, x+self.x_runSpeed, y+self.y_runSpeed, x, y)
            self.x_runSpeed = 0
            self.y_runSpeed = 0

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_up()
            elif event.key == pygame.K_DOWN:
                self.move_down()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
            elif event.key == pygame.K_LEFT:
                self.move_left()
            if event.key == pygame.K_SPACE:
                self.createBomb()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.stop()
            elif event.key == pygame.K_DOWN:
                self.stop()
            elif event.key == pygame.K_RIGHT:
                self.stop()
            elif event.key == pygame.K_LEFT:
                self.stop()
            if event.key == pygame.K_SPACE:
                self.resetBomb()

    def move_up(self):
        self.y_runSpeed = -1

    def move_down(self):
        self.y_runSpeed = 1

    def move_right(self):
        self.x_runSpeed = 1

    def move_left(self):
        self.x_runSpeed = -1

    def stop(self):
        self.y_runSpeed = 0
        self.x_runSpeed = 0

    def createBomb(self):
        self.putBomb = True

    def resetBomb(self):
        self.putBomb = False

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