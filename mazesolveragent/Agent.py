

from mazesolveragent.algorithms.AStar import AStar
from mazesolveragent.algorithms.IDA import IDA
from mazesolveragent.algorithms.IDAStar import IDAStar
from mazesolveragent.algorithms.UCS import UCS


class Agent:
    _ALGORITHMS = {'ASTAR': AStar(),
                   'IDASTAR': IDAStar(),
                   'UCS': UCS(),
                   'IDA': IDA()
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

        # maze = np.array(maze)

        self._algorithm = Agent._ALGORITHMS[algorithmName]
        self._maze = maze
        self._mazeSize = matrixSize
        self._entrypoint = entryPoint
        self._destination = destination

    def solve(self):
        res = self._algorithm.solve(self._maze, self._mazeSize, self._entrypoint, self._destination)
        if res is not None:
            print(res[0])
            print("sum of path", res[1])
        else:
            print(None)
