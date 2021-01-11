import time

import numpy as np
import heapq

from mazesolveragent.algorithms.Util.Constants import X, Y
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Node import Node


class AStar(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        super().__init__(maze, mazeSize, entryPoint, destination, startTime, timeLimit)

        # a helper matrix where mazeIndicator[i][j] == shortest path to maze[i][j]
        self.mazeIndicator = np.full((self._mazeSize, self._mazeSize), np.inf)
        self.mazeIndicator[self._entryPoint[X]][self._entryPoint[Y]] = 0

    def solve(self, heuristic=Node.Heuristic.EuclideanDistance):

        if heuristic == Node.Heuristic.EuclideanDistance:
            self._heuristicName = 'Euclidean Distance'
        # init heap and insert entry point
        heap = []
        entry = Node(self._entryPoint, self._destination, heuristic)
        self._sumOfHValues += entry.getH()
        heapq.heappush(heap, entry)

        timeLeft = True

        while len(heap) != 0 and timeLeft:
            currentNode = heapq.heappop(heap)

            # check if reached goal
            if np.array_equal(currentNode.getCoordinates(), self._destination):
                self.addCutoff(len(currentNode.getPath()))
                self._setSuccess(currentNode.getPath(), currentNode.getCost(), len(currentNode.getPath()))
                return self

            self.addNeighborsToHeap(currentNode, heap)

            if self._timeLimit < time.time() - self._startTime:
                timeLeft = False

        self._setSuccess(success=False)
        return self

    def addNeighborsToHeap(self, currentNode, heap):
        # a list of the node's neighbors
        neighbors = self.getNeighborsNode(currentNode)

        for neigh in neighbors:
            if neigh.getCost() < self.mazeIndicator[neigh.getCoordinates()[X]][neigh.getCoordinates()[Y]]:
                self.mazeIndicator[neigh.getCoordinates()[X]][neigh.getCoordinates()[Y]] = neigh.getCost()
                heapq.heappush(heap, neigh)
                self._numOfExpandedNodes += 1
                self._sumOfHValues += neigh.getH()
