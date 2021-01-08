from abc import abstractmethod


class Heuristic:

    def __init__(self, maze, mazeSize, entryPoint, destination):
        self.maze = maze
        self.mazeSize = mazeSize
        self.entryPoint = entryPoint
        self.destination = destination

    @abstractmethod
    def calculateH(self, node):
        raise NotImplementedError
