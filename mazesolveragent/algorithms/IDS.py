import numpy as np

from mazesolveragent.algorithms.Constants import X, Y
from mazesolveragent.algorithms.Algorithm import Algorithm


class IDS(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination):
        super().__init__(maze, mazeSize, entryPoint, destination)
        # distanceHash[(i, j)] = maximum number of left steps when we reached maze[i][j] (in some iteration)
        self.distanceHash = {}

    def solve(self):

        path = None
        weight = 0

        # edge case, entry == destination
        if np.array_equal(self.entryPoint, self.destination):
            return 'No moves needed', weight

        currentPath = np.array([None for _ in range(self.mazeSize ** 2)], dtype=str)

        # call DLS with an increasing maximum depth
        depthCounter = 1
        while path is None and depthCounter <= self.mazeSize ** 2:
            path, weight = self.recursiveDLS(self.entryPoint, currentPath, 0, depthCounter)
            depthCounter += 1

        # if we found a solution, return it
        if path is not None:
            index = np.where(path == 'None')[0][0]
            # TODO - currently returns length not weight
            return path[:index], index

        return None, None

    def recursiveDLS(self, currentPoint, path, currentPathIndex, maxDepth):

        if currentPathIndex == maxDepth:
            return None, None

        leftSteps = maxDepth - currentPathIndex

        x = currentPoint[X]
        y = currentPoint[Y]

        self.distanceHash[(x, y)] = leftSteps
        pathCounter = 0

        # go around the current node
        i = x - 1
        j = y - 1
        while i < x + 2:
            # check if we can and need to expand this neighbor
            if self.isValid(x, y, i, j) and self.isNeeded(currentPoint, (i, j), leftSteps):
                # add the neighbor's direction
                path[currentPathIndex] = self.PATHS[pathCounter]
                newPoint = (i, j)
                # check if we reached the goal
                if np.array_equal(newPoint, self.destination):
                    path[currentPathIndex + 1] = None
                    return path, None
                # call recursively with the neighbor
                res, _ = self.recursiveDLS(newPoint, path, currentPathIndex + 1, maxDepth)

                # if we have a solution, return
                if res is not None:
                    return path, None

            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathCounter += 1

        # didn't reach a solution from this point with the remaining steps
        return None, None

    def isNeeded(self, currentPoint, pointToCheck, leftSteps):

        # this function uses the distance matrix to make sure we need to expand this node.
        # There are 2 cases this method will return false:
        # 1) distanceHash[pointToCheck] >= leftSteps - 1 :: this means we already visited this point and had more
        #       or equal steps left. This means we don't need to check this point
        # 2) If the first condition didn't happen,
        #       we check if distanceHash[one of pointToCheck's neighbor] > leftSteps - 1 :: this means that
        #       although we didn't visit this point with more steps yet, we will! So we can leave this point for now,
        #       we'll get to it through one of it's other neighbors with more steps.
        x = pointToCheck[X]
        y = pointToCheck[Y]

        currX = currentPoint[X]
        currY = currentPoint[Y]

        # check case 1
        if (x, y) in self.distanceHash and self.distanceHash[(x, y)] >= leftSteps - 1:
            return False

        # check case 2
        needed = True
        i = x - 1
        j = y - 1
        while i < x + 2 and needed:
            if self.isValid(x, y, i, j) and (i != currX or j != currY) and (i, j) in self.distanceHash and \
                    self.distanceHash[(i, j)] > leftSteps - 1:
                needed = False
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1

        return needed
