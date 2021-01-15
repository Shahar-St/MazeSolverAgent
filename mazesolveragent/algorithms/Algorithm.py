import copy
import time
from abc import abstractmethod
import numpy as np
import importlib

from mazesolveragent.algorithms.Util.Constants import X, Y


class Algorithm:
    PATHS = np.array(['LU', 'U', 'RU', 'L', None, 'R', 'LD', 'D', 'RD'])

    def __init__(self, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        self._mazeSize = mazeSize
        self._maze = maze
        self._entryPoint = entryPoint
        self._destination = destination
        self._numOfExpandedNodes = 1
        self._sumOfHValues = 0
        self.solution = None
        self._sumOfCutoffs = 0
        self._numOfCutoffs = 0
        self._minCutoff = np.inf
        self._maxCutoff = -1
        self._heuristicName = 'None (Uninformed Search)'
        self._startTime = startTime
        self._timeLimit = timeLimit

    @abstractmethod
    def solve(self):
        raise NotImplementedError

    @staticmethod
    def factory(algoName, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        module = importlib.import_module('mazesolveragent.algorithms.' + algoName)
        algo = getattr(module, algoName)
        return algo(maze, mazeSize, entryPoint, destination, startTime, timeLimit)

    def isValid(self, x, y, newX, newY):
        return 0 <= newX <= self._mazeSize - 1 and 0 <= newY <= self._mazeSize - 1 and (newX != x or newY != y)

    def getNeighborsNode(self, currentNode, reverse=False):
        # get the node's neighbors, check if they are valid and update the statistics
        x = currentNode.getCoordinates()[X]
        y = currentNode.getCoordinates()[Y]

        neighbors = []
        pathIndex = 0

        # loop to iterate around the current node
        i = x - 1
        j = y - 1
        while i < x + 2:
            if self.isValid(x, y, i, j):
                if self._maze[i][j] == -1:
                    self.addCutoff(len(currentNode.getPath()) + 1)
                else:
                    newNeighbor = copy.deepcopy(currentNode)
                    if reverse is False:
                        newNeighbor.addStep((i, j), self._maze[i][j], self.PATHS[pathIndex])
                    else:  # special case for BIA*
                        newNeighbor.addStep((i, j), self._maze[i][j], np.flip(self.PATHS)[pathIndex])
                    neighbors.append(newNeighbor)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathIndex += 1

        neighbors = np.array(neighbors)
        return neighbors

    def getCostOfPoint(self, point):
        return self._maze[point[X]][point[Y]]

    def addCutoff(self, depth):
        self._sumOfCutoffs += depth
        self._numOfCutoffs += 1
        if depth < self._minCutoff:
            self._minCutoff = depth
        if depth > self._maxCutoff:
            self._maxCutoff = depth

    class Solution:
        def __init__(self, path, cost, numOfExpandedNodes, penetrationRatio, avgHValue, ebf, minCutoff, avgCutoff,
                     maxCutoff, results, n, startTime, timeLimit, algoName):
            self._path = path
            self._cost = cost
            self._numOfExpandedNodes = numOfExpandedNodes
            self._penetrationRatio = penetrationRatio
            self._avgHValue = avgHValue
            self._ebf = ebf
            self._minCutoff = minCutoff
            self._avgCutoff = avgCutoff
            self._maxCutoff = maxCutoff
            self._results = results
            self._n = n
            self._startTime = startTime
            self._timeLimit = timeLimit
            self.algoName = algoName

        def printResults(self, fileName, heuristicName):

            outputFile = open(fileName + ' - solution.txt', 'w')

            totalTime = time.time() - self._startTime
            if totalTime > self._timeLimit:
                outputFile.write('FAILED (Time Limit Exceeded)\n')
            elif self._results:
                outputFile.write(f"{'-'.join(self._path)} {self._cost} {self._numOfExpandedNodes}\n")
            else:
                outputFile.write('FAILED\n')

            outputFile.write('Problem Name: ' + fileName + '\n' +
                             f'Algorithm: {self.algoName}\n' +
                             'Heuristic Name: ' + heuristicName + '\n' +
                             f'N = {self._n}\n' +
                             f'd = {self._numOfExpandedNodes}\n' +
                             f'd/N = {self._penetrationRatio:.4f}\n' +
                             f'Success = {self._results}\n' +
                             f'Time = {totalTime:.4f} seconds\n' +
                             f'Time Limit = {self._timeLimit:.4f} seconds\n' +
                             f'EBF = {self._ebf:.4f}\n' +
                             f'Average H value = {self._avgHValue:.4f}\n' +
                             f'Cutoffs: Min = {self._minCutoff}, Max = {self._maxCutoff}, Avg = {self._avgCutoff:.4f}\n'
                             )
            outputFile.close()

        def setAlgoName(self, algoName):
            self.algoName = algoName

    def _setSuccess(self, path=None, cost=None, solutionDepth=-1, success=True):

        totalTime = time.time() - self._startTime
        if success is True and totalTime > self._timeLimit:
            path = None
            cost = None
            solutionDepth = -1
            success = False

        self.solution = Algorithm.Solution(
            path=path,
            cost=cost,
            numOfExpandedNodes=self._numOfExpandedNodes,
            penetrationRatio=self._numOfExpandedNodes / (self._mazeSize ** 2),
            avgHValue=self._sumOfHValues / self._numOfExpandedNodes,
            ebf=(self._mazeSize ** 2) ** (1 / solutionDepth) if solutionDepth > 0 else 0,
            minCutoff=self._minCutoff,
            avgCutoff=self._sumOfCutoffs / self._numOfCutoffs if self._numOfCutoffs != 0 else 0,
            maxCutoff=self._maxCutoff,
            results=success,
            n=self._mazeSize ** 2,
            startTime=self._startTime,
            timeLimit=self._timeLimit,
            algoName=type(self).__name__
        )

    def printResultsToFile(self, fileName):
        self.solution.printResults(fileName, self._heuristicName)
