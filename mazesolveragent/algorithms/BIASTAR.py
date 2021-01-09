import numpy as np
import heapq

from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Constants import X, Y
from mazesolveragent.algorithms.Util.Node import Node


class BIASTAR(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        # a helper matrix where mazeIndicator[i][j] == shortest path to maze[i][j]
        self.mazeIndicator = np.full((self._mazeSize, self._mazeSize), np.inf)
        self.mazeIndicator[self._entryPoint[X]][self._entryPoint[Y]] = 0

        self.mazeIndicatorBack = np.full((self._mazeSize, self._mazeSize), np.inf)
        self.mazeIndicatorBack[self._destination[X]][self._destination[Y]] = 0

    def solve(self):
        # init heaps and insert forwardEntry points
        forwardHeap = []
        backwardHeap = []
        forwardEntry = Node(self._entryPoint, self._destination, heuristic=Node.Heuristic.EuclideanDistance)
        heapq.heappush(forwardHeap, forwardEntry)
        backwardEntry = Node(self._destination, self._entryPoint, heuristic=Node.Heuristic.EuclideanDistance)
        heapq.heappush(backwardHeap, backwardEntry)

        commonHash = {}
        backwardHash = {}

        while len(forwardHeap) != 0 and len(backwardHeap) != 0:

            currentForwardNode = heapq.heappop(forwardHeap)
            forwardX = currentForwardNode.getCoordinates()[X]
            forwardY = currentForwardNode.getCoordinates()[Y]

            if (forwardX, forwardY) in backwardHash:
                print("forward: ", currentForwardNode.getCoordinates())
                other = commonHash[forwardX, forwardY]
                minCost = currentForwardNode.getCost() + other.getCost()
                # set1 = set(forwardHeap)
                # set2 = set(backwardsHeap)
                # intersection = set1.intersection(set2)
                #
                # minPath = None
                # for inter in intersection:
                #     coordinates = inter.coordinates
                #     node1 = [x for x in forwardHeap if x.coordinates == coordinates][0]
                #     node2 = [x for x in backwardsHeap if x.coordinates == coordinates][0]
                #     if node1.cost + node2.cost < minCost:
                #         minCost = node1.cost + node2.cost
                # minPath = np.concatenate(node1.path, np.flip(node2.path))

                return currentForwardNode.path, minCost

            print("insert forward to hash", currentForwardNode.getCoordinates())
            commonHash[(forwardX, forwardY)] = currentForwardNode

            currentBackwardNode = heapq.heappop(backwardHeap)
            backwardX = currentBackwardNode.getCoordinates()[X]
            backwardY = currentBackwardNode.getCoordinates()[Y]

            if (backwardX, backwardY) in commonHash:
                other = commonHash[backwardX, backwardY]
                minCost = currentBackwardNode.getCost() + other.getCost()

                backwardHeap.append(currentBackwardNode)
                print("backward: ", currentBackwardNode.coordinates)
                set1 = set(forwardHeap)
                set2 = set(backwardHeap)
                intersection = set1.intersection(set2)
                minPath = None
                for inter in intersection:
                    coordinates = inter.coordinates
                    node1 = [x for x in forwardHeap if x.coordinates == coordinates][0]
                    node2 = [x for x in backwardHeap if x.coordinates == coordinates][0]
                    if node1.cost + node2.cost < minCost:
                        minCost = node1.cost + node2.cost
                        # minPath = np.concatenate(node1.path, np.flip(node2.path))

                return currentForwardNode.path, minCost

            print("insert backward to hash", currentBackwardNode.getCoordinates())
            backwardHash[(backwardX, backwardY)] = currentBackwardNode

            # a list of the node's neighbors
            forwardNeighbors = self.getNeighborsNode(currentForwardNode)
            backwardNeighbors = self.getNeighborsNode(currentBackwardNode)

            for neigh in forwardNeighbors:
                neighX = neigh.getCoordinates()[X]
                neighY = neigh.getCoordinates()[Y]
                if neigh.getCost() < self.mazeIndicator[neighX][neighY]:
                    self.mazeIndicator[neighX][neighY] = neigh.getCost()
                    # if (neighX, neighY) in commonHash:
                    #     commonHash.pop((neighX, neighY))
                    heapq.heappush(forwardHeap, neigh)

            for neigh in backwardNeighbors:
                neighX = neigh.getCoordinates()[X]
                neighY = neigh.getCoordinates()[Y]
                if neigh.getCost() < self.mazeIndicatorBack[neighX][neighY]:
                    self.mazeIndicatorBack[neighX][neighY] = neigh.getCost()
                    # if (neighX, neighY) in commonHash:
                    #     commonHash.pop((neighX, neighY))
                    heapq.heappush(backwardHeap, neigh)

        return None, None
