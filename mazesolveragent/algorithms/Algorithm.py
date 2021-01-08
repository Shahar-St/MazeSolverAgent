from abc import abstractmethod
import importlib


class Algorithm:
    PATHS = ['LU', 'U', 'RU', 'L', None, 'R', 'LD', 'D', 'RD']

    def __init__(self, maze, mazeSize, entryPoint, destination):
        self.mazeSize = mazeSize
        self.maze = maze
        self.entryPoint = entryPoint
        self.destination = destination

    @abstractmethod
    def solve(self):
        # return path, weight
        raise NotImplementedError

    def isValid(self, x, y, newX, newY):
        return 0 <= newX <= self.mazeSize - 1 and 0 <= newY <= self.mazeSize - 1 and (newX != x or newY != y) and \
               self.maze[newX][newY] != -1

    @staticmethod
    def factory(algoName, maze, mazeSize, entryPoint, destination):
        module = importlib.import_module('mazesolveragent.algorithms.' + algoName)
        algo = getattr(module, algoName)
        return algo(maze, mazeSize, entryPoint, destination)
