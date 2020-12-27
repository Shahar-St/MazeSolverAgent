import numpy as np

from mazesolveragent.algorithms.AStar import AStar


class Agent:
    _algorithms = {'ASTAR': AStar(),
                   'IDASTAR': AStar()
                   }

    def __init__(self, fileName):


        inputFile = open(fileName, 'r')
        algorithmName = inputFile.readline().replace('\n', '')
        matrixSize = int(inputFile.readline().replace('\n', ''))
        entryPoint = [int(num) for num in inputFile.readline().replace('\n', '').split(',')]
        destination = [int(num) for num in inputFile.readline().replace('\n', '').split(',')]
        # maze = np.array()

        sc = {' ', '\n'}

        maze = []
        for line in inputFile:
            strLine = ''.join([c for c in line if c not in sc])
            maze.append([int(num) for num in strLine.split(',')])

        maze = np.array(maze)

        self._algorithm = Agent._algorithms[algorithmName]
        self._maze = maze
        self._mazeSize = matrixSize
        self._entrypoint = entryPoint
        self._destination = destination



    def solve(self):
        self._algorithm.solve()
