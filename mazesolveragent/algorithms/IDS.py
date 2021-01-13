import time

import numpy as np

from mazesolveragent.algorithms.Util.Constants import X, Y
from mazesolveragent.algorithms.Algorithm import Algorithm


class IDS(Algorithm):

    def __init__(self, maze, mazeSize, entryPoint, destination, startTime, timeLimit):
        super().__init__(maze, mazeSize, entryPoint, destination, startTime, timeLimit)
        # distanceHash[(i, j)] = maximum number of left steps when we reached maze[i][j] (in some iteration)
        self.distanceHash = {}

    def solve(self):

        # edge case - entry or destination are -1
        if self._maze[self._entryPoint[X]][self._entryPoint[Y]] == -1 or\
                self._maze[self._destination[X]][self._destination[Y]] == -1:
            self._setSuccess(success=False)
            return self
        path = None

        # edge case, entry == destination
        if np.array_equal(self._entryPoint, self._destination):
            self.addCutoff(0)
            self._setSuccess(path=['No moves needed'], cost=0, solutionDepth=0)
            return self

        currentPath = np.array([None for _ in range(self._mazeSize ** 2)], dtype=str)

        # call DLS with an increasing maximum depth
        depthCounter = 1
        while path is None and depthCounter <= self._mazeSize ** 2:
            path = self.recursiveDLS(self._entryPoint, currentPath, 0, depthCounter)
            depthCounter += 1

        # if we found a solution, return it
        if path is not None:
            index = np.where(path == 'None')[0][0]
            path = path[:index]
            cost = self.calculateCost(path)
            self._setSuccess(path, cost, len(path))
        else:
            self._setSuccess(success=False)

        return self

    def recursiveDLS(self, currentPoint, path, currentPathIndex, maxDepth):

        if self._timeLimit < time.time() - self._startTime:
            self._setSuccess(success=False)
            return self

        if currentPathIndex == maxDepth:
            self.addCutoff(currentPathIndex)
            return None

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
            if self.isValid(x, y, i, j):
                if self._maze[i][j] == -1:
                    self.addCutoff(currentPathIndex)
                elif self.isNeeded(currentPoint, (i, j), leftSteps):
                    # add the neighbor's direction
                    path[currentPathIndex] = self.PATHS[pathCounter]
                    newPoint = (i, j)

                    self._numOfExpandedNodes += 1

                    # check if we reached our goal
                    if np.array_equal(newPoint, self._destination):
                        path[currentPathIndex + 1] = None
                        self.addCutoff(currentPathIndex)
                        return path
                    # call recursively with the neighbor
                    res = self.recursiveDLS(newPoint, path, currentPathIndex + 1, maxDepth)

                    # if we have a solution, return
                    if res is not None:
                        return path
                else:
                    self.addCutoff(currentPathIndex)
            j += 1
            if j == y + 2:
                i += 1
                j = y - 1
            pathCounter += 1

        # didn't reach a solution from this point with the remaining steps
        return None

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

    def calculateCost(self, path):

        cost = 0
        row = 0
        col = 0
        for step in path:
            if step == self.PATHS[0]:  # LU
                row -= 1
                col -= 1
            elif step == self.PATHS[1]:  # U
                row -= 1
            elif step == self.PATHS[2]:  # RU
                row -= 1
                col += 1
            elif step == self.PATHS[3]:  # L
                col -= 1
            elif step == self.PATHS[5]:  # R
                col += 1
            elif step == self.PATHS[6]:  # LD
                row += 1
                col -= 1
            elif step == self.PATHS[7]:  # D
                row += 1
            elif step == self.PATHS[8]:  # RD
                row += 1
                col += 1

            cost += self._maze[row][col]

        return cost
