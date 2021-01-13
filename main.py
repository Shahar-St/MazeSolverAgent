from mazesolveragent.Agent import Agent


def printMenu(inputFile, timeLimit):
    maxTime = 'Log2(n)'

    if timeLimit is not None:
        maxTime = f'{timeLimit} seconds'

    print('Please choose from the following options:\n'
          '0: Exit\n'
          f'1: Start (input file = {inputFile}, Time limit = {maxTime}).\n'
          '2: Change input file.\n'
          '3: Change time limit.')


def main():
    inputFile = 'SpiralTest.txt'
    maxTime = None

    validInput = False
    while not validInput:
        printMenu(inputFile, maxTime)

        try:
            inp = int(input('Enter: '))
            if 0 <= inp <= 3:
                if inp == 0:
                    return
                elif inp == 1:
                    validInput = True
                elif inp == 2:
                    inputFile = input('Enter input path: ')
                else:
                    maxTime = float(input('Enter time limit (in seconds): '))
            else:
                print('Number not in range, please try again')

        except ValueError:
            print("Not a valid answer, please try again")

        print()

    print('----Starting----')
    agent = Agent(inputFile, maxTime)
    agent.solve()
    print(f'----Done. Results we printed to "{inputFile} - solution.txt"----')


if __name__ == '__main__':
    main()
