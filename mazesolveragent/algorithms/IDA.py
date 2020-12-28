from mazesolveragent.algorithms import Constants
from mazesolveragent.algorithms.Algorithm import Algorithm


class IDA(Algorithm):

    def solve(self, maze, size, entryPoint, destination):

        path = [None for _ in range(size * size)]

        if entryPoint == destination:
            return path

        res = None
        depthCounter = 1
        while res is None and depthCounter <= size * size:
            res = self.recursiveDLS(maze, size, entryPoint, destination, path, 0, depthCounter,
                                    [[False for _ in range(size)] for _ in range(size)])
            depthCounter += 1

        return res[:res.index(None)] if res is not None else None

    def recursiveDLS(self, maze, mazeSize, currentPoint, destination, path, currentPathIndex, maxDepth, mazeIndicator):

        if currentPathIndex == maxDepth:
            return None

        x = currentPoint[Constants.X]
        y = currentPoint[Constants.Y]

        mazeIndicator[currentPoint[Constants.X]][currentPoint[Constants.Y]] = True
        pathCounter = 0

        i = x - 1
        j = y - 1
        while i < x + 2:
            if 0 <= i < mazeSize and 0 <= j < mazeSize and (i != x or j != y) and maze[i][j] != -1 and not \
                    mazeIndicator[i][j] and self.isNeeded(currentPoint, [i, j], mazeIndicator, mazeSize):
                path[currentPathIndex] = self.PATHS[pathCounter]
                mazeIndicator[i][j] = True
                newPoint = [i, j]
                if newPoint == destination:
                    path[currentPathIndex + 1] = None
                    return path

                res = self.recursiveDLS(maze, mazeSize, newPoint, destination, path, currentPathIndex + 1,
                                        maxDepth, mazeIndicator)
                mazeIndicator[i][j] = False

                if res is not None:
                    return path

            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathCounter += 1

        return None

    def isNeeded(self, currentPoint, pointToCheck, mazeIndicator, mazeSize):

        x = pointToCheck[Constants.X]
        y = pointToCheck[Constants.Y]

        needed = True
        i = x - 1
        j = y - 1
        while i < x + 2 and needed:
            if 0 <= i < mazeSize and 0 <= j < mazeSize and (i != x or j != y) and (
                    i != currentPoint[0] or j != currentPoint[1]) and mazeIndicator[i][j] is True:
                needed = False

            j += 1
            if j == y + 2:
                i += 1
                j = y - 1

        return needed
