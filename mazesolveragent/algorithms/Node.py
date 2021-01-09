import numpy as np
from scipy.spatial import distance
import enum


class Node:
    class Heuristic(enum.Enum):
        Zero = 0
        EuclideanDistance = 1

    def __init__(self, entryPoint, destination=None, heuristic=Heuristic.Zero):
        self.cost = 0
        self.coordinates = entryPoint
        # list that saves the path: i.e: ['RU' ,'LU', ... ]
        self.path = []
        self.destination = destination
        self.heuristic = heuristic

    def addStep(self, newPoint, costToNewPoint, path):
        # logic of path
        self.path.append(path)
        self.coordinates = np.array(newPoint)
        self.cost += costToNewPoint

    # how the nodes will be ordered in the heap
    def __lt__(self, other):
        if self.cost + self.getH() != other.cost + other.getH():
            return self.cost + self.getH() < other.cost + other.getH()

        # tie breaking according to h
        return self.getH() < other.getH()

    def getF(self):
        return self.cost + self.getH()

    def getH(self):
        if self.heuristic == self.Heuristic.Zero:
            return 0
        if self.heuristic == self.Heuristic.EuclideanDistance:
            return self.euclideanDistanceH()
        raise Exception

    def euclideanDistanceH(self):
        a = distance.euclidean(self.coordinates, self.destination)
        return distance.euclidean(self.coordinates, self.destination)
