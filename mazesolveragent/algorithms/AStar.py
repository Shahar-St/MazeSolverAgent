import copy
import heapq
import sys

from mazesolveragent.algorithms import Constants
from mazesolveragent.algorithms.Algorithm import Algorithm


class AStar(Algorithm):

    class Node:
        def __init__(self, point):
            self.cost = 0
            self.coordinates = point
            # ['RU' , ]
            self.path = []

        def addStep(self, newPoint, costToNewPoint, path, destination):
            # logic of path
            self.path.append(path)
            self.coordinates = newPoint
            h = max(abs(self.coordinates[Constants.X] - destination[Constants.X]),
                    abs(self.coordinates[Constants.Y] - destination[Constants.Y]))
            self.cost = self.cost + costToNewPoint + h

        def __lt__(self, other):
            return self.cost < other.cost

    def solve(self, maze, mazeSize, entryPoint, destination):
        # init heap and insert entry point
        heap = []
        entry = AStar.Node(entryPoint)
        heapq.heappush(heap, entry)

        mazeIndicator = [[sys.maxsize for _ in range(mazeSize)] for _ in range(mazeSize)]

        mazeIndicator[entryPoint[Constants.X]][entryPoint[Constants.Y]] = 0

        while len(heap) != 0:
            currentNode = heapq.heappop(heap)

            # check if reached goal
            if currentNode.coordinates == destination:
                return currentNode.path, currentNode.cost

            # list of Nodes
            neighbors = self.getNeighborsNode(maze, mazeSize, currentNode, destination)

            for n in neighbors:
                if n.cost < mazeIndicator[n.coordinates[Constants.X]][n.coordinates[Constants.Y]]:
                    mazeIndicator[n.coordinates[Constants.X]][n.coordinates[Constants.Y]] = n.cost
                    heapq.heappush(heap, n)

        return None

    def getNeighborsNode(self, maze, mazeSize, currentNode, destination):

        x = currentNode.coordinates[0]
        y = currentNode.coordinates[1]

        neighbors = []

        pathCounter = 0
        i = x - 1
        j = y - 1
        while i < x + 2:
            if 0 <= i < mazeSize and 0 <= j < mazeSize and (i != x or j != y) and maze[i][j] != -1:
                newNeighbor = copy.deepcopy(currentNode)
                newNeighbor.addStep([i, j], maze[i][j], self.PATHS[pathCounter], destination)
                neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathCounter += 1

        return neighbors
