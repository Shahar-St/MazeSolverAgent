import numpy as np

from mazesolveragent.algorithms.Algorithm import Algorithm


class Agent:

    def __init__(self, fileName):
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

        maze = np.array(maze)

        # init the object fields
        self._algorithm = Algorithm.factory(algorithmName, maze, matrixSize, entryPoint, destination)

    def solve(self):

        path, cost = self._algorithm.solve()
        if path is not None:
            print(path)
            print("sum of path", cost)
        else:
            print(None)



