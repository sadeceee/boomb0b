import math
from constants import *
from heapq import heappush, heappop   # for priority queue

class node:
    xPos = 0
    yPos = 0
    distance = 0
    priority = 0

    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority

    def update_priority(self, xDest, yDest):
        self.priority = self.distance + self.luftlinie(xDest, yDest) * 10

    def luftlinie(self, xZiel, yZiel):
        xDest = xZiel - self.xPos
        yDest = yZiel - self.yPos

        d = math.sqrt(xDest*xDest + yDest*yDest)
        return d

    def lower_then(self, other):
        return self.priority < other.priority

    def next(self, direction, d):
        if direction == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10

class findPath:


    def __init__(self, map, direction, dx, dy, xStart, yStart, xEnd, yEnd, n=FIELDS_X, m=FIELDS_Y):
        self.map = map
        self.n = n
        self.m = m
        self.direction = direction
        self.dx = dx
        self.dy = dy
        self.xStart = xStart
        self.yStart = yStart
        self.xEnd = xEnd
        self.yEnd = yEnd

        self.closed = []
        self.open = []
        self.map_direct = []
        self.row = []

        self.load()

    def load(self):
        row = [0] * self.n
        for i in range(self.m):
            self.closed.append(list(row))
            self.open.append(list(row))
            self.map_direct.append(list(row))

        self.notTried = [[], []]
        self.notTriedPriority = 0
        self.node0 = node(self.xStart, self.yStart, 0, 0)
        self.node0.update_priority(self.xEnd, self.yEnd)
        heappush(self.notTried[self.notTriedPriority], self.node0)
        self.open[self.yStart][self.xStart] = self.node0.priority

    def search(self):
        while len(self.notTried[self.notTriedPriority]) > 0:
            self.node1 = self.notTried[self.notTriedPriority][0]  # Top Node
            self.node0 = node(self.node1.xPos, self.node1.yPos, self.node1.distance, self.node1.priority)
            x = self.node0.xPos
            y = self.node1.yPos
            heappop(self.notTried[self.notTriedPriority])   # remove node from open list
            self.open[y][x] = 0
            self.closed[y][x] = 1

            if x == self.xEnd and y == self.yEnd:   # quit searching
                path = ""
                while not(x == self.xStart and y == self.yStart):
                    j = self.map_direct[y][x]
                    c = str((j + self.direction / 2) % self.direction)
                    path = c + path
                    x += self.dx[j]
                    y += self.dy[j]

                return path

            self.generate(x, y)

        return ""

    def generate(self, x, y):
        for i in range(self.direction):
            xdx = x + self.dx[i]
            ydy = y + self.dy[i]
            if not (xdx < 0 or xdx > self.n-1 or ydy < 0 or ydy > self.m-1
                    or self.map[ydy][xdx] == 1 or self.closed[ydy][xdx] == 1):
                self.mode0 = node(xdx, ydy, self.node0.distance, self.node0.priority)
                self.mode0.next(self.direction, i)
                self.mode0.update_priority(self.xEnd, self.yEnd)

                if self.open[ydy][xdx] == 0:
                    self.open[ydy][xdx] = self.mode0.priority
                    heappush(self.notTried[self.notTriedPriority], self.mode0)

                    self.map_direct[ydy][xdx] = (i + self.direction / 2) % self.direction

                elif self.open[ydy][xdx] > self.mode0.priority:
                    self.open[ydy][xdx] = self.mode0.priority
                    self.map_direct[ydy][xdx] = (i + self.direction / 2) % self.direction


                    while not (self.notTried[self.notTriedPriority][0].xPos == xdx and self.notTried[self.notTriedPriority][0].yPos == ydy):
                        heappush(self.notTried[1 - self.notTriedPriority], self.notTried[self.notTriedPriority][0])
                        heappop(self.notTried[self.notTriedPriority])
                    heappop(self.notTried[self.notTriedPriority])

                    if len(self.notTried[self.notTriedPriority]) > len(self.notTried[1 - self.notTriedPriority]):
                        self.notTriedPriority = 1 - self.notTriedPriority
                    while len(self.notTried[self.notTriedPriority]) > 0:
                        heappush(self.notTried[1 - self.notTriedPriority], self.notTried[self.notTriedPriority][0])
                        heappop(self.notTried[self.notTriedPriority])
                    self.notTriedPriority = 1 - self.notTriedPriority
                    heappush(self.notTried[self.notTriedPriority], self.mode0)
