from abc import abstractmethod


class H:

    def __init__(self, maze, mazeSize, entryPoint, destination):
        self.maze = maze
        self.mazeSize = mazeSize
        self.entryPoint = entryPoint
        self.destination = destination

    @abstractmethod
    def h(self, node):
        raise NotImplementedError
