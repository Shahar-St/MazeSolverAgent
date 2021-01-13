import time
import numpy as np
from math import log2

from mazesolveragent.algorithms.Algorithm import Algorithm


class Agent:

    def __init__(self, fileName, timeLimit):
        startTime = time.time()

        # Parse the data
        inputFile = open(fileName, 'r')
        algorithmName = inputFile.readline().replace('\n', '')
        matrixSize = int(inputFile.readline().replace('\n', ''))
        entryPoint = np.array([int(num) for num in inputFile.readline().replace('\n', '').split(',')])
        destination = np.array([int(num) for num in inputFile.readline().replace('\n', '').split(',')])

        unwantedChars = (' ', '\n')
        maze = []
        for line in inputFile:
            strLine = ''.join([c for c in line if c not in unwantedChars])
            maze.append([int(num) for num in strLine.split(',')])

        inputFile.close()
        maze = np.array(maze)

        if timeLimit is None:
            timeLimit = log2(matrixSize)

        # init the object fields
        self._algorithm = Algorithm.factory(algorithmName, maze, matrixSize, entryPoint, destination, startTime,
                                            timeLimit)
        if fileName.endswith('.txt'):
            fileName = fileName[:len(fileName) - 4]
        self._fileName = fileName
        self._startTime = startTime

    def solve(self):

        actualAlg = self._algorithm.solve()
        actualAlg.printResultsToFile(self._fileName)
