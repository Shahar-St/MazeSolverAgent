import numpy as np

from mazesolveragent.algorithms.Heuristics.Heuristic import Heuristic


class EuclideanDistance(Heuristic):
    def calculateH(self, node):
        return np.linalg.norm(node.coordinates - self.destination)
