import heapq
import copy
import sys

from mazesolveragent.algorithms import Constants
from mazesolveragent.algorithms.Algorithm import Algorithm
import numpy as np


class UCS(Algorithm):


    class Node:
        def __init__(self, point):
            self.cost = 0
            self.coordinates = point
            # ['RU' , ]
            self.path = []

        def addStep(self, newPoint, costToNewPoint, path):
            # logic of path
            self.path.append(path)
            self.coordinates = newPoint
            self.cost += costToNewPoint

        def __lt__(self, other):
            return self.cost < other.cost

    def solve(self, maze, mazeSize, entryPoint, destination):
        # init heap and insert entry point
        heap = []
        entry = UCS.Node(entryPoint)
        heapq.heappush(heap, entry)

        mazeIndicator = [[sys.maxsize for _ in range(mazeSize)] for _ in range(mazeSize)]

        mazeIndicator[entryPoint[Constants.X]][entryPoint[Constants.Y]] = 0

        while len(heap) != 0:
            currentNode = heapq.heappop(heap)

            # check if reached goal
            if currentNode.coordinates == destination:
                return currentNode.path

            # list of Nodes
            neighbors = self.getNeighborsNode(maze, mazeSize, currentNode)

            for n in neighbors:
                if n.cost < mazeIndicator[n.coordinates[Constants.X]][n.coordinates[Constants.Y]]:
                    mazeIndicator[n.coordinates[Constants.X]][n.coordinates[Constants.Y]] = n.cost
                    heapq.heappush(heap, n)

        return None

    def getNeighborsNode(self, maze, mazeSize, currentNode):

        x = currentNode.coordinates[0]
        y = currentNode.coordinates[1]

        neighbors = []

        pathCounter = 0
        i = x - 1
        j = y - 1
        while i < x + 2:
            if 0 <= i < mazeSize and 0 <= j < mazeSize and (i != x or j != y) and maze[i][j] != -1:
                newNeighbor = copy.deepcopy(currentNode)
                newNeighbor.addStep([i, j], maze[i][j], self.PATHS[pathCounter])
                neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathCounter += 1

        return neighbors
