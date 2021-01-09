import time
from mazesolveragent.Agent import Agent


def main():
    start = time.time()
    agent = Agent('SmallInputFile.txt')
    agent.solve()
    end = time.time()
    print(f'The algorithm took {end - start:.4f} seconds')


if __name__ == '__main__':
    main()
