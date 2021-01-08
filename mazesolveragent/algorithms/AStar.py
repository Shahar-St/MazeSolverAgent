import numpy as np
import heapq
import copy

from mazesolveragent.algorithms.Constants import X, Y
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Heuristics.EuclideanDistance import EuclideanDistance


class AStar(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        # a helper matrix where mazeIndicator[i][j] == shortest path to maze[i][j]
        self.mazeIndicator = np.full((self.mazeSize, self.mazeSize), np.inf)
        self.mazeIndicator[self.entryPoint[X]][self.entryPoint[Y]] = 0
        self.heuristic = EuclideanDistance(maze, mazeSize, entryPoint, destination)

    # an object that defines the node
    class Node:
        def __init__(self, entryPoint, heuristic):
            self.cost = 0
            self.coordinates = entryPoint
            # list that saves the path: i.e: ['RU' ,'LU', ... ]
            self.path = []
            self.heuristic = heuristic.calculateH

        def addStep(self, newPoint, costToNewPoint, path):
            # logic of path
            self.path.append(path)
            self.coordinates = newPoint
            self.cost += costToNewPoint

        # how the nodes will be ordered in the heap
        def __lt__(self, other):
            return self.cost + self.heuristic(self) < other.cost + self.heuristic(other)

    def solve(self):
        # init heap and insert entry point
        heap = []
        entry = AStar.Node(self.entryPoint, self.heuristic)
        heapq.heappush(heap, entry)

        while len(heap) != 0:
            currentNode = heapq.heappop(heap)

            # check if reached goal
            if np.array_equal(currentNode.coordinates, self.destination):
                return currentNode.path, currentNode.cost

            # a list of the node's neighbors
            neighbors = self.getNeighborsNode(currentNode)

            for neigh in neighbors:
                if neigh.cost < self.mazeIndicator[neigh.coordinates[X]][neigh.coordinates[Y]]:
                    self.mazeIndicator[neigh.coordinates[X]][neigh.coordinates[Y]] = neigh.cost
                    heapq.heappush(heap, neigh)

        return None, None

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
                newNeighbor.addStep([i, j], self.maze[i][j], self.PATHS[pathIndex])
                neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathIndex += 1

        neighbors = np.array(neighbors)
        return neighbors
