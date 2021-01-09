import numpy as np
import heapq
import copy

from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Heuristics.EuclideanDistance import EuclideanDistance
from mazesolveragent.algorithms.Util.Constants import X, Y


class BIASTAR(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        # a helper matrix where mazeIndicator[i][j] == shortest path to maze[i][j]
        self.mazeIndicator = np.full((self._mazeSize, self._mazeSize), np.inf)
        self.mazeIndicator[self._entryPoint[X]][self._entryPoint[Y]] = 0

        self.mazeIndicatorBack = np.full((self._mazeSize, self._mazeSize), np.inf)
        self.mazeIndicatorBack[self._destination[X]][self._destination[Y]] = 0

        self.heuristic = EuclideanDistance(maze, mazeSize, entryPoint, destination)
        self.heuristicBack = EuclideanDistance(maze, mazeSize, destination, entryPoint)

    # an object that defines the node
    class Node:
        def __init__(self, entryPoint, heuristic):
            self.cost = 0
            self.coordinates = entryPoint
            # list that saves the path: i.e: ['RU' ,'LU', ... ]
            self.path = []
            self.heuristic = heuristic.calculateH

        def __hash__(self):
            return hash((self.coordinates[X], self.coordinates[Y]))

        def __eq__(self, other):
            return (self.coordinates[X], self.coordinates[Y]) == (other.coordinates[X], other.coordinates[Y])

        def __ne__(self, other):
            return not (self.coordinates[X], self.coordinates[Y]) == (other.coordinates[X], other.coordinates[Y])

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
        heapBack = []
        entry = BIASTAR.Node(self._entryPoint, self.heuristic)
        heapq.heappush(heap, entry)
        entryBack = BIASTAR.Node(self._destination, self.heuristicBack)
        heapq.heappush(heapBack, entryBack)

        hashTable = set()

        while len(heap) != 0 and len(heapBack) != 0:

            currentNode = heapq.heappop(heap)
            if currentNode in hashTable:
                t = np.array(hashTable)
                minCost = currentNode.cost + [x for x in t if x.coordinates == currentNode.coordinates][0]
                print("forward: ", currentNode.coordinates)
                set1 = set(heap)
                set2 = set(heapBack)
                intersection = set1.intersection(set2)

                minPath = None
                for inter in intersection:
                    coordinates = inter.coordinates
                    node1 = [x for x in heap if x.coordinates == coordinates][0]
                    node2 = [x for x in heapBack if x.coordinates == coordinates][0]
                    if node1.cost + node2.cost < minCost:
                        minCost = node1.cost + node2.cost
                        # minPath = np.concatenate(node1.path, np.flip(node2.path))

                return currentNode.path, minCost

            print("insert forward to hash", currentNode.coordinates)
            hashTable.add(currentNode)
            # hashTable[currentNode] = currentNode.cost, currentNode.path

            currentNodeBack = heapq.heappop(heapBack)
            if currentNodeBack in hashTable:
                t = [x for x in hashTable]

                minCost = currentNodeBack.cost + [x for x in t if np.array_equal(x.coordinates, currentNodeBack.coordinates)][0].cost
                heapBack.append(currentNodeBack)
                print("backward: ", currentNodeBack.coordinates)
                set1 = set(heap)
                set2 = set(heapBack)
                intersection = set1.intersection(set2)
                minPath = None
                for inter in intersection:
                    coordinates = inter.coordinates
                    node1 = [x for x in heap if x.coordinates == coordinates][0]
                    node2 = [x for x in heapBack if x.coordinates == coordinates][0]
                    if node1.cost + node2.cost < minCost:
                        minCost = node1.cost + node2.cost
                        # minPath = np.concatenate(node1.path, np.flip(node2.path))

                return currentNode.path, minCost
            print("insert backward to hash", currentNodeBack.coordinates)
            hashTable.add(currentNodeBack)
            # hashTable[currentNodeBack] = currentNodeBack.cost, currentNodeBack.path

            # check if reached goal
            # if np.array_equal(currentNode.coordinates, self.destination):
            #     return currentNode.path, currentNode.cost

            # a list of the node's neighbors
            neighbors = self.getNeighborsNode(currentNode)
            neighborsBack = self.getNeighborsNode(currentNodeBack)

            for neigh in neighbors:
                if neigh.cost < self.mazeIndicator[neigh.coordinates[X]][neigh.coordinates[Y]]:
                    self.mazeIndicator[neigh.coordinates[X]][neigh.coordinates[Y]] = neigh.cost
                    heapq.heappush(heap, neigh)

            for neigh in neighborsBack:
                if neigh.cost < self.mazeIndicatorBack[neigh.coordinates[X]][neigh.coordinates[Y]]:
                    self.mazeIndicatorBack[neigh.coordinates[X]][neigh.coordinates[Y]] = neigh.cost
                    heapq.heappush(heapBack, neigh)

        return None, None
