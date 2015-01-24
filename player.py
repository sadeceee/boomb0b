from helpers import *

class player(object):
    image = None
    rect = None

    def __init__(self):
        self.bombSize = 0
        self.bombCount = 0
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.stop()
            if event.key == pygame.K_DOWN:
                self.stop()
            if event.key == pygame.K_RIGHT:
                self.stop()
            if event.key == pygame.K_LEFT:
                self.stop()

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

class KI(player):

    pass

