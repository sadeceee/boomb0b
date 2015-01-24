class box:
    image = None
    isWall = False
    breakable = False

    def __init__(self):
        pass

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def load(self, path):
        pass

class stone(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = False


class crate(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = True


class bomb(box):

    def __init__(self):
        super(box)

        self.isWall = True
        self.breakable = False