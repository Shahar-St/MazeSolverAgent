from fibheap import *
import heapq

from mazesolveragent.algorithms.Algorithm import Algorithm
import numpy as np


class UCS(Algorithm):
    class Node:
        def __init__(self, point):
            self.cost = 0
            self.coordinates = point
            # ['RU' , ]
            self._path = []

        def addStep(self, newPoint, costToNewPoint):
            # logic of path
            self._path.append('RU')
            self.coordinates = newPoint
            self.cost += costToNewPoint

        def __lt__(self, other):
            return self.cost < other.cost

    def getNeighborsNode(self):
        return []


    def solve(self, maze, size, entryPoint, destination):
        # init heap and insert entry point
        heap = []
        entry = UCS.Node(entryPoint)
        heapq.heappush(heap, entry)

        while len(heap) != 0:
            currentNode = heapq.heappop(heap)

            if currentNode.coordinates == destination:
                return currentNode
            # check if reached goal

            # list of Nodes
            neighbors = self.getNeighborsNode()

            for n in neighbors:
                heapq.heappush(heap, n)

        return None
