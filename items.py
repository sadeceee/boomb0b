from box import box


class fire_item(box):

    def __init__(self):
        super(fire_item, self).__init__()

        self.breakable = True

        self.load("IMG", "item_fire.png")

class bomb_item(box):

    def __init__(self):
        super(bomb_item, self).__init__()

        self.breakable = True

        self.load("IMG", "item_bomb.png")

class skull_item(box):

    def __init__(self):
        super(skull_item, self).__init__()

        self.breakable = True

        self.load("IMG", "item_skull.png")