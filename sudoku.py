# John Novak
# janovak@mtu.edu
# 03/05/2015
#
# Solves a Sudoku puzzle

# Only removes the element from the list if it exists in the list
def safeRemove(l, e):
    if l.count(e) > 0:
        l.remove(e)

# Represents the board and keeps track of everything needed for solving the puzzle
class Sudoku:
    # 3x3 array of 3x3 arrays to represent the board
    board = [[[[None for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
    # Keeps track of all numbers that are not currently taken in each row, column, and box
    rows = [[i for i in range(1, 10)] for j in range(9)]
    cols = [[i for i in range(1, 10)] for j in range(9)]
    boxes = [[i for i in range(1, 10)] for j in range(9)]
    # Unsolved squares
    openList = list()

    # Keeps track of each square's current value (0 for unsolved) and which
    # row, column, and box the square is a part of
    class BoardPos:
        def __init__(self, w, x, y, z):
            self.a = w
            self.r = x
            self.c = y
            self.b = z

    def __init__(self, filename):
        f = open(filename, "r")
        for i in range(3):
            for k in range(3):
                for j in range(3):
                    for l in range(3):
                        square = int(f.read(1))
                        rInd = self.row(i, j, k, l)
                        cInd = self.col(i, j, k, l)
                        bInd = self.box(i, j, k, l)
                        # Fill the board with the initial values for each square
                        # and which row, column, and box the square is a part of
                        self.board[i][j][k][l] = Sudoku.BoardPos(square, rInd, cInd, bInd)
                        # Remove a number from the row, column, and box
                        # associated with the square if the square is solved
                        if square != 0:
                            safeRemove(self.rows[rInd], square)
                            safeRemove(self.cols[cInd], square)
                            safeRemove(self.boxes[bInd], square)
                        else:
                            # Fill the list of unsolved squares
                            self.openList.append((i, j, k, l))
                f.read(1) # new line character
        f.close()

    # Iteratively solve the board from its initial state
    def solve(self):
        # Used to check if we cannot be certain of the next move
        firstUnsolved = self.openList[-1]
        # Iterate over the open list until it is empty
        while len(self.openList) > 0:
            # Cannot solve any more squares without trial and error
            if firstUnsolved == self.openList[0] and len(self.openList) != 1:
                break

            # Used to check if a square was solved this iteration
            oldLength = len(self.openList)
            possibilities = self.getPossibilities(self.openList[0])
            i, j, k, l = self.openList[0]
            if len(possibilities) == 1:
                firstUnsolved = self.openList[-1]
                # If the first square in the open list only has one possible solution
                # given the board's current state
                self.found(self.openList[0], possibilities[0])
            else:
                # If a row, column, or box only has one possible square for a
                # value then put the value in that square

                # Check if none of the other squares in the row could hold any
                # of the square's possible solutions
                answer = possibilities
                for b in range(3):
                    for d in range(3):
                        if self.board[i][b][k][d].a == 0 and (j, l) != (b, d):
                            answer = list(set(answer) - set(self.getPossibilities((i, b, k, d))))
                if len(answer) == 1:
                    firstUnsolved = self.openList[-1]
                    self.found(self.openList[0], answer[0])
                    continue

                # Check if none of the other squares in the column could hold any
                # of the square's possible solutions
                answer = possibilities
                for a in range(3):
                    for c in range(3):
                        if self.board[a][j][c][l].a == 0 and (i, k) != (a, c):
                            answer = list(set(answer) - set(self.getPossibilities((a, j, c, l))))
                if len(answer) ==  1:
                    firstUnsolved = self.openList[-1]
                    self.found(self.openList[0], answer[0])
                    continue

                # Check if none of the other squares in the box could hold any
                # of the square's possible solutions
                answer = possibilities
                for c in range(3):
                    for d in range(3):
                        if self.board[i][j][c][d].a == 0:
                            answer = list(set(answer) - set(self.getPossibilities((i, j, c, d))))
                if len(answer) == 1:
                    firstUnsolved = self.openList[-1]
                    self.found(self.openList[0], answer[0])
                    continue

            # Move first element to the end if first element was not removed
            if oldLength == len(self.openList):
                self.openList.append(self.openList.pop(0))

        # Logical methods could not solve every square
        if len(self.openList) > 0:
            self.depthFirst()

    # Use backtracking to solve the puzzle from its current state
    def depthFirst(self):
        if len(self.openList) == 0:
            return True

        curSquare = self.openList[0]
        possibilities = self.getPossibilities(curSquare)

        i, j, k, l = curSquare
        for e in possibilities:
            self.found(curSquare, e)
            if self.depthFirst():
                return True
            # Restore to state of the last partial, possibile solution
            self.board[i][j][k][l].a = 0
            self.rows[self.board[i][j][k][l].r].append(e)
            self.cols[self.board[i][j][k][l].c].append(e)
            self.boxes[self.board[i][j][k][l].b].append(e)
            self.openList.insert(0, curSquare)

        return False

    # Set the square the value found and remove that value from the square's
    # row, column, and box and remove the square from the open list
    def found(self, index, e):
        i, j, k, l = index
        self.board[i][j][k][l].a = e
        self.removeFound(index, e)
        self.openList.remove(index)

    # Remove the value from the square's row, column, and box
    def removeFound(self, index, e):
        i, j, k, l = index
        self.rows[self.board[i][j][k][l].r].remove(e)
        self.cols[self.board[i][j][k][l].c].remove(e)
        self.boxes[self.board[i][j][k][l].b].remove(e)

    # Returns a list of all possible values for the square
    def getPossibilities(self, index):
        i, j, k, l = index
        tempRow = self.rows[self.board[i][j][k][l].r]
        tempCol = self.cols[self.board[i][j][k][l].c]
        tempBox = self.boxes[self.board[i][j][k][l].b]
        return list(set(tempRow) & set(tempCol) & set(tempBox))

    # Returns the box of the square
    def box(self, i, j, k, l):
        return i * 3 + j

    # Returns the row of the square
    def row(self, i, j, k, l):
        return i * 3 + k

    # Returns the column of the square
    def col(self, i, j, k, l):
        return j * 3 + l

    # Prints the board
    def printBoard(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        print (self.board[i][k][j][l].a),
                print ""

def main():
    puzzle = Sudoku("board.txt")
    puzzle.solve()
    puzzle.printBoard()

if __name__ == "__main__":
    main()
