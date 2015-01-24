from helpers import *
from box import stone, crate, bomb

class player(object):
    image = None
    rect = None
    isWall = False
    breakable = False
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
        self.rect = self.image.get_rect()

class player_1(player):

    def __init__(self):
        super(player_1, self).__init__()

        self.load("IMG", "player.png")

    def update(self, gf, x, y):
        # Put bomb
        if self.putBomb:
            putBomb = False
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

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_up()
            if event.key == pygame.K_DOWN:
                self.move_down()
            if event.key == pygame.K_RIGHT:
                self.move_right()
            if event.key == pygame.K_LEFT:
                self.move_left()
            if event.key == pygame.K_SPACE:
                self.createBomb()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.stop()
            if event.key == pygame.K_DOWN:
                self.stop()
            if event.key == pygame.K_RIGHT:
                self.stop()
            if event.key == pygame.K_LEFT:
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

    """
    def collision(self, obj):
        if self.rect.colliderect(stone().rect):
            self.stop()
        elif self.rect.colliderect(crate().rect):
            self.stop()
        else:
            return False
    """
class KI(player):

    pass

