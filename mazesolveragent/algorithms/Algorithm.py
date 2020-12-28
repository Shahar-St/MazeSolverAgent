from abc import abstractmethod


class Algorithm:

    PATHS = ['LU', 'U', 'RU', 'L', None, 'R', 'LD', 'D', 'RD']

    @abstractmethod
    def solve(self, maze, size, entryPoint, destination):
        raise NotImplementedError
