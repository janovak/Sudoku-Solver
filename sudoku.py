def main():
    board = [[0 for i in range(9)] for j in range(9)]
    with open("board.txt", "r") as input:
        i = 0
        for line in input:
            j = 0
            for s in line.split(' '):
                board[i][j] = int(s)
                j += 1
            i += 1
    solution = [[[] for i in range(9)] for j in range(9)]
    '''for i in range(9):
        for j in range(9):
            print(board[i][j]),
        print
    '''

if __name__ == "__main__":
    main()
