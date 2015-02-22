import pygame
from constants import *
from box import box


class fire_item(box):

    def __init__(self, posX, posY):
        super(fire_item, self).__init__()

        self.posX = posX
        self.posY = posY

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_fire.png")
        self.rect = pygame.Rect(self.posX, self.posY, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT)

    def destroyNew(self, gf, x, y, player):
        player.increaseBombSize()
        gf.rem(self, x, y)
        return player

class bomb_item(box):

    def __init__(self, posX, posY):
        super(bomb_item, self).__init__()

        self.posX = posX
        self.posY = posY

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_bomb.png")
        self.rect = pygame.Rect(self.posX, self.posY, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT)

    def destroyNew(self, gf, x, y, player):
        player.increaseMaxBombs()
        gf.rem(self, x, y)
        return player

class skull_item(box):

    def __init__(self, posX, posY):
        super(skull_item, self).__init__()

        self.posX = posX
        self.posY = posY

        self.breakable = True
        self.isItem = True

        self.load("IMG", "item_skull.png")
        self.rect = pygame.Rect(self.posX, self.posY, FIELD_SIZE_WIDTH, FIELD_SIZE_HEIGHT)

    def destroyNew(self, gf, x, y, player):
        player.poisonPlayer()
        gf.rem(self, x, y)
        return player