from mazesolveragent.algorithms.Constants import X, Y
from mazesolveragent.algorithms.Hu.H import H
from math import sqrt


class H1(H):
    def h(self, node):
        x = node.coordinates[X]
        y = node.coordinates[Y]

        goalX = self.destination[X]
        goalY = self.destination[Y]

        res = sqrt((x - goalX) ** 2 + (y - goalY) ** 2)
        return res
