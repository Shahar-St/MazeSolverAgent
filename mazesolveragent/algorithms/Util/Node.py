import numpy as np
from scipy.spatial import distance
import enum

from mazesolveragent.algorithms.Util.Constants import X, Y


class Node:
    class Heuristic(enum.Enum):
        Zero = 0
        MaxDeltas = 1

    def __init__(self, entryPoint, destination=None, heuristic=Heuristic.Zero):

        self._cost = 0
        self._coordinates = entryPoint
        # list that saves the path: i.e: ['RU' ,'LU', ... ]
        self._path = []
        self._destination = destination
        self._heuristic = heuristic

    def addStep(self, newPoint, costToNewPoint, path):
        # logic of path
        self._path.append(path)
        self._coordinates = np.array(newPoint)
        self._cost += costToNewPoint

    # how the nodes will be ordered in the heap
    def __lt__(self, other):
        if self._cost + self.getH() != other.getCost() + other.getH():
            return self._cost + self.getH() < other.getCost() + other.getH()

        # tie breaking according to h
        return self.getH() < other.getH()

    def getF(self):
        return self._cost + self.getH()

    def getH(self):
        if self._heuristic == self.Heuristic.Zero:
            return 0
        if self._heuristic == self.Heuristic.MaxDeltas:
            return self.maxDeltas()
        raise Exception

    def maxDeltas(self):

        return max(np.absolute(self.getCoordinates()[X] - self._destination[X]),
                   np.absolute(self.getCoordinates()[Y] - self._destination[Y]))


    def getCoordinates(self):
        return self._coordinates

    def getCost(self):
        return self._cost

    def getPath(self):
        return self._path
