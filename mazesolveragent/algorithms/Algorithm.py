import copy
from abc import abstractmethod
import numpy as np
import importlib

from mazesolveragent.algorithms.Util.Constants import X, Y


class Algorithm:
    PATHS = np.array(['LU', 'U', 'RU', 'L', None, 'R', 'LD', 'D', 'RD'])

    def __init__(self, maze, mazeSize, entryPoint, destination):
        self._mazeSize = mazeSize
        self._maze = maze
        self._entryPoint = entryPoint
        self._destination = destination

    @abstractmethod
    def solve(self):
        # return path, weight
        raise NotImplementedError

    @staticmethod
    def factory(algoName, maze, mazeSize, entryPoint, destination):
        module = importlib.import_module('mazesolveragent.algorithms.' + algoName)
        algo = getattr(module, algoName)
        return algo(maze, mazeSize, entryPoint, destination)

    def isValid(self, x, y, newX, newY):
        return 0 <= newX <= self._mazeSize - 1 and 0 <= newY <= self._mazeSize - 1 and (newX != x or newY != y) and \
               self._maze[newX][newY] != -1

    def getNeighborsNode(self, currentNode):

        x = currentNode.getCoordinates()[X]
        y = currentNode.getCoordinates()[Y]

        neighbors = []
        pathIndex = 0

        # loop to iterate around the current node
        i = x - 1
        j = y - 1
        while i < x + 2:
            if self.isValid(x, y, i, j):
                newNeighbor = copy.deepcopy(currentNode)
                newNeighbor.addStep((i, j), self._maze[i][j], self.PATHS[pathIndex])
                neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathIndex += 1

        neighbors = np.array(neighbors)
        return neighbors

    def getCostOfPoint(self, point):
        return self._maze[point[X]][point[Y]]