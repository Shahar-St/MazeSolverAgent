import heapq

from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Constants import X, Y
from mazesolveragent.algorithms.Util.Node import Node


class BIASTAR(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        # visited lists
        self._forwardHash = {}
        self._backwardHash = {}

        # <direction>HelperHash[(i, j)] = shortest (least expensive) path (in form of a Node type) to maze[i][j]
        # in <direction> (that was found in any time)
        self._forwardHelperHash = {}
        self._backwardHelperHash = {}

    def solve(self):

        # init heaps and insert entry points
        forwardEntry = Node(self._entryPoint, self._destination, heuristic=Node.Heuristic.EuclideanDistance)
        forwardHeap = [forwardEntry]

        backwardEntry = Node(self._destination, self._entryPoint, heuristic=Node.Heuristic.EuclideanDistance)
        backwardHeap = [backwardEntry]

        # init helper hashes
        self._forwardHelperHash[(self._entryPoint[X], self._entryPoint[Y])] = forwardEntry
        self._backwardHelperHash[(self._destination[X], self._destination[Y])] = backwardEntry

        while len(forwardHeap) != 0 and len(backwardHeap) != 0:

            # forward
            # pop minimum
            currentForwardNode = heapq.heappop(forwardHeap)
            forwardCoords = (currentForwardNode.getCoordinates()[X], currentForwardNode.getCoordinates()[Y])

            # check for a solution
            if forwardCoords in self._backwardHash:
                minPath, minCost = self.lookForOtherSolutions(currentForwardNode, forwardCoords, self._backwardHash)
                return minPath, minCost + self.getCostOfPoint(self._destination)

            # insert to visited list
            self._forwardHash[forwardCoords] = currentForwardNode

            # backward (same logic as forward)
            currentBackwardNode = heapq.heappop(backwardHeap)
            backwardCoords = (currentBackwardNode.getCoordinates()[X], currentBackwardNode.getCoordinates()[Y])

            if backwardCoords in self._forwardHash:
                minPath, minCost = self.lookForOtherSolutions(currentBackwardNode, backwardCoords, self._forwardHash)
                return minPath, minCost + self.getCostOfPoint(self._destination)

            self._backwardHash[backwardCoords] = currentBackwardNode

            # expand successors
            self.expandNeighbors(currentForwardNode, forwardHeap, self._forwardHelperHash)
            self.expandNeighbors(currentBackwardNode, backwardHeap, self._backwardHelperHash)

        return None, None

    def expandNeighbors(self, currentNode, heap, helperHash):

        # a list of the node's neighbors
        neighbors = self.getNeighborsNode(currentNode)

        for neigh in neighbors:
            coords = (neigh.getCoordinates()[X], neigh.getCoordinates()[Y])
            # this if help us avoid expanding circles and maintains the helperHash definition
            if coords not in helperHash or neigh.getCost() < helperHash[coords].getCost():
                heapq.heappush(heap, neigh)
                helperHash[coords] = neigh

    def lookForOtherSolutions(self, foundNode, foundNodeCoords, otherHash):

        # our first found matching point
        matchingNode = otherHash[foundNodeCoords]
        minCost = foundNode.getCost() + matchingNode.getCost() - self.getCostOfPoint(matchingNode.getCoordinates())
        minPath = None  # TODO

        # get intersection of helper hashes. This guarantees to get all (and best) possible solutions,
        # derives from the helper hashes definition
        intersection = self._forwardHelperHash.keys() & self._backwardHelperHash.keys()

        # check all possible solution and pick the least expansive one
        for coordinates in intersection:
            cost = self._forwardHelperHash[coordinates].getCost() + self._backwardHelperHash[coordinates].getCost() \
                   - self.getCostOfPoint(coordinates)
            if cost < minCost:
                minCost = cost
                minPath = None  # TODO

        return minPath, minCost
