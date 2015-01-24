from helpers import *

class box:
    image = None
    isWall = False
    breakable = False

    def __init__(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, dir, filename):
        image = image_loader(dir, filename)

class stone(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = False

        self.load("IMG", "stone.bmp")


class crate(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = True

        # self.load("IMG", TODO)


class bomb(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = False

        # self.load("IMG", TODO)