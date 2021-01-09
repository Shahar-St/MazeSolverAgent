import copy
from abc import abstractmethod
import numpy as np
import importlib

from mazesolveragent.algorithms.Constants import X, Y


class Algorithm:
    PATHS = np.array(['LU', 'U', 'RU', 'L', None, 'R', 'LD', 'D', 'RD'])

    def __init__(self, maze, mazeSize, entryPoint, destination):
        self.mazeSize = mazeSize
        self.maze = maze
        self.entryPoint = entryPoint
        self.destination = destination

    @abstractmethod
    def solve(self):
        # return path, weight
        raise NotImplementedError

    def isValid(self, x, y, newX, newY):
        return 0 <= newX <= self.mazeSize - 1 and 0 <= newY <= self.mazeSize - 1 and (newX != x or newY != y) and \
               self.maze[newX][newY] != -1

    @staticmethod
    def factory(algoName, maze, mazeSize, entryPoint, destination):
        module = importlib.import_module('mazesolveragent.algorithms.' + algoName)
        algo = getattr(module, algoName)
        return algo(maze, mazeSize, entryPoint, destination)

    def getNeighborsNode(self, currentNode):

        x = currentNode.coordinates[X]
        y = currentNode.coordinates[Y]

        neighbors = []
        pathIndex = 0

        # loop to iterate around the current node
        i = x - 1
        j = y - 1
        while i < x + 2:
            if self.isValid(x, y, i, j):
                newNeighbor = copy.deepcopy(currentNode)
                newNeighbor.addStep((i, j), self.maze[i][j], self.PATHS[pathIndex])
                neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathIndex += 1

        neighbors = np.array(neighbors)
        return neighbors