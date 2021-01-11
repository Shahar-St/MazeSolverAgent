import numpy as np
from math import ceil
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Constants import X, Y
from mazesolveragent.algorithms.Util.Node import Node


class IDAStar(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)
        self.leftCostHash = {}

    def solve(self):
        root = Node(self._entryPoint, self._destination, Node.Heuristic.EuclideanDistance)

        fLimit = root.getH()

        while fLimit != np.inf:
            solution, fLimit = self.idaStarRecur(root, ceil(fLimit), np.inf)
            if solution is not None:
                return solution.getPath(), None

        return None

    def idaStarRecur(self, node, fLimit, nextF):

        if node.getF() > fLimit:
            return None, node.getF()

        if np.array_equal(node.getCoordinates(), self._destination):
            return node, fLimit

        self.leftCostHash[(node.getCoordinates()[X], node.getCoordinates()[Y])] = fLimit - node.getF()

        neighbors = self.getNeighborsNode(node)
        for n in neighbors:
            if self.isNeeded(node, n, fLimit):
                solution, newF = self.idaStarRecur(n, fLimit, nextF)
                if solution is not None:
                    return solution, fLimit
                nextF = min(nextF, newF)

        return None, nextF

    def isNeeded(self, currentNode, nodeToCheck, fLimit):

        pointToCheck = nodeToCheck.getCoordinates()
        x = pointToCheck[X]
        y = pointToCheck[Y]
        if (x, y) in self.leftCostHash and fLimit - (currentNode.getCost() + self._maze[x][y] + nodeToCheck.getH()) <= \
                self.leftCostHash[(x, y)]:
            return False

        return True
