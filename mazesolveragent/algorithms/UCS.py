from mazesolveragent.algorithms.AStar import AStar
from mazesolveragent.algorithms.Algorithm import Algorithm
from mazesolveragent.algorithms.Util.Node import Node


class UCS(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        super().__init__(maze, mazeSize, entryPoint, destination, startTime, timeLimit)

        self.aStar = AStar(maze, mazeSize, entryPoint, destination, startTime, timeLimit)


    def solve(self):
        # call A* with the 0 heuristic
        aStar = self.aStar.solve(heuristic=Node.Heuristic.Zero)
        aStar.Solution.setAlgoName(type(self).__name__)
        return aStar