from mazesolveragent.algorithms.AStar import AStar
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Node import Node


class UCS(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)

        self.aStar = AStar(maze, mazeSize, entryPoint, destination)


    def solve(self):
        return self.aStar.solve(heuristic=Node.Heuristic.Zero)
