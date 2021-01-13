import time

import numpy as np
from math import ceil
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Constants import X, Y, HEURISTIC
from mazesolveragent.algorithms.Util.Node import Node


class IDASTAR(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        super().__init__(maze, mazeSize, entryPoint, destination, startTime, timeLimit)
        self.leftCostHash = {}
        self._heuristicName = HEURISTIC

    def solve(self):

        # edge case - entry or destination are -1
        if self._maze[self._entryPoint[X]][self._entryPoint[Y]] == -1 or\
                self._maze[self._destination[X]][self._destination[Y]] == -1:
            self._setSuccess(success=False)
            return self

        root = Node(self._entryPoint, self._destination, Node.Heuristic.MaxDeltas)

        fLimit = root.getH()
        self._sumOfHValues += root.getH()

        while fLimit != np.inf:

            solutionNode, fLimit = self.idaStarRecur(root, ceil(fLimit), np.inf)
            if solutionNode is not None:
                self._setSuccess(solutionNode.getPath(), solutionNode.getCost(), len(solutionNode.getPath()))
                return self

        self._setSuccess(success=False)
        return self

    def idaStarRecur(self, node, fLimit, nextF):

        if self._timeLimit < time.time() - self._startTime:
            self._setSuccess(success=False)
            return None, np.inf

        if node.getF() > fLimit:
            self.addCutoff(len(node.getPath()))
            return None, node.getF()

        if np.array_equal(node.getCoordinates(), self._destination):
            self.addCutoff(len(node.getPath()))
            return node, fLimit

        self.leftCostHash[(node.getCoordinates()[X], node.getCoordinates()[Y])] = fLimit - node.getF()

        neighbors = self.getNeighborsNode(node)

        for n in neighbors:
            if self.isNeeded(node, n, fLimit):
                self._sumOfHValues += n.getH()
                self._numOfExpandedNodes += 1
                solutionNode, newF = self.idaStarRecur(n, fLimit, nextF)
                if solutionNode is not None:
                    return solutionNode, fLimit
                nextF = min(nextF, newF)
            else:
                self.addCutoff(len(n.getPath()))

        return None, nextF

    def isNeeded(self, currentNode, nodeToCheck, fLimit):

        pointToCheck = nodeToCheck.getCoordinates()
        x = pointToCheck[X]
        y = pointToCheck[Y]
        if (x, y) in self.leftCostHash and fLimit - (currentNode.getCost() + self._maze[x][y] + nodeToCheck.getH()) <= \
                self.leftCostHash[(x, y)]:
            return False

        return True
