from abc import abstractmethod


class Algorithm:


    @abstractmethod
    def solve(self, maze, size, entryPoint, destination):
        raise NotImplementedError
