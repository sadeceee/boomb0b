from box import box


class fire_item(box):

    def __init__(self):
        super(fire_item, self).__init__()

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_fire.png")

    def destroyNew(self, gf, x, y, player):
        player.increaseBombSize()
        gf.rem(self, x, y)
        return player

class bomb_item(box):

    def __init__(self):
        super(bomb_item, self).__init__()

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_bomb.png")

    def destroyNew(self, gf, x, y, player):
        player.increaseMaxBombs()
        gf.rem(self, x, y)
        return player

class skull_item(box):

    def __init__(self):
        super(skull_item, self).__init__()

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_skull.png")

    def destroyNew(self, gf, x, y, player):
        player.poisonPlayer()
        gf.rem(self, x, y)
        return player