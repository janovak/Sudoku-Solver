class BoardPos:
    def __init__(self, w, x, y, z):
        self.a = w
        self.r = x
        self.c = y
        self.b = z

def safeRemove(l, e):
    if l.count(e) > 0:
        l.remove(e)

class Sudoku:
    board = [[[[None for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
    rows = [[i for i in range(1, 10)] for j in range(9)]
    cols = [[i for i in range(1, 10)] for j in range(9)]
    boxes = [[i for i in range(1, 10)] for j in range(9)]
    openList = list()

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
                        self.board[i][j][k][l] = BoardPos(square, rInd, cInd, bInd)
                        if square != 0:
                            safeRemove(self.rows[rInd], square)
                            safeRemove(self.cols[cInd], square)
                            safeRemove(self.boxes[bInd], square)
                        else:
                            self.openList.append((i, j, k, l))
                f.read(1) # new line character
        f.close()

    def solve(self):
        while len(self.openList) > 0:
            oldLength = len(self.openList)
            possibilities = self.getPossibilities(self.openList[0])
            i, j, k, l = self.openList[0]
            if len(possibilities) == 1:
                self.board[i][j][k][l].a = possibilities[0]
                self.removeFound(i, j, k, l, possibilities[0])
                del self.openList[0]
            else:
                answer = possibilities
                for b in range(3):
                    for d in range(3):
                        if self.board[i][b][k][d].a == 0 and (j, l) != (b, d):
                            answer = list(set(answer) - set(self.getPossibilities((i, b, k, d))))
                    else:
                        continue
                    break
                if len(answer) == 1:
                    self.board[i][j][k][l].a = answer[0]
                    self.removeFound(i, j, k, l, answer[0])
                    del self.openList[0]
                    continue

                answer = possibilities
                for a in range(3):
                    for c in range(3):
                        if self.board[a][j][c][l].a == 0 and (i, k) != (a, c):
                            answer = list(set(answer) - set(self.getPossibilities((a, j, c, l))))
                    else:
                        continue
                    break
                    self.board[i][j][k][l].a = answer[0]
                    self.removeFound(i, j, k, l, answer[0])
                    del self.openList[0]
                    continue

                answer = possibilities
                for c in range(3):
                    for d in range(3):
                        if self.board[i][j][c][d].a == 0:
                            answer = list(set(answer) - set(self.getPossibilities((i, j, c, d))))
                    else:
                        continue
                    break
                if len(answer) == 1:
                    self.board[i][j][k][l].a = answer[0]
                    self.removeFound(i, j, k, l, answer[0])
                    del self.openList[0]
                    continue

            if oldLength == len(self.openList):
                self.openList.append(self.openList.pop(0))

    def removeFound(self, i, j, k, l, el):
        safeRemove(self.rows[self.board[i][j][k][l].r], el)
        safeRemove(self.cols[self.board[i][j][k][l].c], el)
        safeRemove(self.boxes[self.board[i][j][k][l].b], el)

    def getPossibilities(self, index):
        i, j, k, l = index
        tempRow = self.rows[self.board[i][j][k][l].r]
        tempCol = self.cols[self.board[i][j][k][l].c]
        tempBox = self.boxes[self.board[i][j][k][l].b]
        return list(set(tempRow) & set(tempCol) & set(tempBox))

    def box(self, i, j, k, l):
        return i * 3 + j

    def row(self, i, j, k, l):
        return i * 3 + k

    def col(self, i, j, k, l):
        return j * 3 + l

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
