import numpy as np
import heapq

from mazesolveragent.algorithms.Constants import X, Y
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Node import Node


class AStar(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        # a helper matrix where mazeIndicator[i][j] == shortest path to maze[i][j]
        self.mazeIndicator = np.full((self.mazeSize, self.mazeSize), np.inf)
        self.mazeIndicator[self.entryPoint[X]][self.entryPoint[Y]] = 0

    def solve(self, heuristic=Node.Heuristic.EuclideanDistance):
        # init heap and insert entry point
        heap = []
        entry = Node(self.entryPoint, self.destination, heuristic)
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
