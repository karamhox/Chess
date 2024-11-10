


black =  ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖", "♙"]
white = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜", "♟"]
types = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
cors = "ABCDEFGH"

board = None

class Piece:
    def __init__(self, type, color, x, y, emoji):
        self.type = type
        self.color = color
        self.row = x
        self.col = y
        self.emoji = emoji
        self.firstMove = True

    def move(self, row, col):
        board[self.row][self.col] = 0
        self.row = row
        self.col = col
        board[row][col] = self

        #Only needed for the pawns actually..
        self.firstMove = False  
        

    def checkSubRow(self, col):
        lowerCol = (col < self.col) * col + (self.col < col) * self.col
        higherCol = (col > self.col) * col + (self.col > col) * self.col
        deltaCol = higherCol - lowerCol

        if board[self.row][col]:
            if board[self.row][col].color == self.color:
                return 0
        
        #No need to check the last and first squares since, one is checked up, the other is self
        for coli in range(lowerCol + 1, higherCol):
            if not board[self.row][coli]:
                continue

            elif board[self.row][coli]:
                return 0

        return 1
                        
    def checkSubVert(self, row):
        lowerRow = (row < self.row) * row + (self.row < row) * self.row
        higherRow = (row > self.row) * row + (self.row > row) * self.row

        if board[row][self.col]:
            if board[row][self.col].color == self.color:
                return 0

        #No need to check the last and first squares since it's checked up, one is checked up the other is self
        for rowi in range(lowerRow + 1, higherRow):
            if not board[rowi][self.col]:
                continue

            elif board[rowi][self.col]:
                return 0

        return 1
            
    def checkSubDiag(self, row, col):
        deltaCol = col - self.col
        deltaRow = row - self.row

        #Thinking of making start, finish, increment and refactor it into one loop
        start = None
        end = None
        coli = None

        if abs(deltaRow) != abs(deltaCol):
            return 0

        elif deltaRow == 0 or deltaCol == 0:
            return 0
        
        elif board[row][col]:
            if board[row][col].color == self.color:
                return 0

        if deltaRow < 0:
            if deltaCol < 0:
                coli = col
                for rowi in range(row, self.row):
                    if not board[rowi][coli]:
                        coli += 1
                        continue

                    elif board[rowi][coli] and coli != col:
                        return 0
                        
                    coli += 1

            else:
                coli = self.col + 1
                for rowi in range(self.row - 1, row - 1, -1):
                    if not board[rowi][coli]:
                        coli += 1
                        continue

                    elif board[rowi][coli] and coli != col:
                        return 0

                    coli += 1

            
        else:
            if deltaCol < 0:
                coli = col
                for rowi in range(row, self.row, -1):
                    if not board[rowi][coli]:
                        coli += 1
                        continue

                    elif board[rowi][coli] and coli != col:
                        return 0
                    
                    coli += 1

            else:
                coli = self.col + 1
                for rowi in range(self.row + 1, row + 1):
                    if not board[rowi][coli]:
                        coli += 1
                        continue

                    elif board[rowi][coli] and coli != col:
                        return 0

                    coli += 1

        return 1
                  
    def checkboardLimit(self, row, col):
        if row >= len(board) or row < 0 or col >= len(board[0] or col < 0):
           # print("SIGSEG")
            return 0
        return 1

    def checkRook(self, row, col):
        if not self.checkboardLimit(row, col):
            return 0

        if(row != self.row and col != self.col) or (row == self.row and col == self.col):
            return 0

        elif row == self.row:
            return self.checkSubRow(col)
        
        return self.checkSubVert(row)

    def checkBishop(self, row, col):
        if not self.checkboardLimit(row, col):
            return 0
            
        return self.checkSubDiag(row, col)

    def checkQueen(self, row, col):
        if not self.checkboardLimit(row, col):
            return 0

        elif row == self.row:
            return self.checkSubRow(col)  #So the problem was that I am returning self.checkSubrow (the address), instead of the return value. Interesting..

        elif row != self.row and col == self.col:
            return self.checkSubVert(row)

        else:
            return self.checkSubDiag(row, col)

    def checkPawn(self, row, col):
        deltaRow = row - self.row
        deltaCol = abs(col - self.col)

        if not self.checkboardLimit(row, col):
            return 0
        
        if self.row == row:
            return 0  

        if self.color == "Black":
            if deltaRow > 0 or deltaRow == -2 and not self.firstMove:
                return 0

            elif deltaRow < -2:
                return 0
            
        else: 
            if deltaRow < 0 or deltaRow == 2 and not self.firstMove:
                return 0
            
            elif deltaRow > 2:
                return 0


        if deltaCol == 1 and not board[row][col]:
            return 0

        elif deltaCol > 1:
            return 0
        
        if not board[row][col]:
            return 1

        elif board[row][col].color == self.color:
                return 0

        if row == 7 or row == 0:
            self.convertPawn()
 
        return 1
                
    def checkKnight(self, row, col):
        if not self.checkboardLimit(row, col):
            return 0

        deltaRow = abs(row - self.row)
        deltaCol = abs(col - self.col)
        

        if deltaRow > 2 or deltaCol > 2:
            return 0

        if board[row][col]:
            if board[row][col].color == self.color:
                return 0
            
        if deltaRow == 1 and deltaCol == 2:
            return 1

        elif deltaCol == 1 and deltaRow == 2:
            return 1

        return 0

    def checkKing(self, row, col):
        if not self.checkboardLimit(row, col):
            return 0

        deltaRow = abs(row - self.row)
        deltaCol = abs(col - self.col)

        if deltaRow > 1 or deltaCol > 1:
            return 0

        if not board[row][col]:
            return 1
        
        elif board[row][col].color == self.color:
            return 0

        return 1

    def findKing(self, color):
        for row in range(8):
            for col in range(8):
                if not board[row][col]:
                    continue

                elif board[row][col].type == "King" and board[row][col].color == color:
                    return board[row][col]


    def isKingDetectedAfter(self, row, col):
        
        board[self.row][self.col] = 0 #This should happen first, so that if row == self.row and col == self.col -> the piece does not dissapear
        old = board[row][col]
        board[row][col] = self
        
        #Temporarily, in order to pass the checking logic
        #This should be assigned before king, so that is self == king, then the king variabe is updated with the latest values
        col0, self.col = self.col, col
        row0, self.row = self.row, row

        king = self.findKing(self.color) 

        if not king:
            pass


        for i in range(8):
            for j in range(8):
                if not board[i][j]:
                    continue

                elif board[i][j].color == self.color:
                    continue

                elif board[i][j].isValidMove(king.row, king.col) and (row != i or col != j):
                    other = board[i][j]
                    self.col = col0
                    self.row = row0
                    board[row][col] = old 
                    board[self.row][self.col] = self

                    return board[i][j]
                
        self.col = col0
        self.row = row0
        board[row][col] = old
        board[self.row][self.col] = self

        return 0

    def isPieceDetected(self):
        detectors = []

        for row in range(8):
            for col in range(8):
                if not board[row][col]:
                    continue

                if board[row][col].color == self.color:
                    continue

                if board[row][col].isValidMove(self.row, self.col):
                    detectors.append(board[row][col])

        
        return detectors
    

    def isKingMovable(king):
        escape = 0
        for row in range(king.row - 1, king.row + 2):
            for col in range(king.col - 1, king.col + 2):
                if king.isValidMove(row, col) and not king.isKingDetectedAfter(row, col):
                    escape = 1
                    break

            if escape:
                break

        return escape


    def isValidMove(self, row, col):
        match self.type:
            case "Rook":
                return self.checkRook(row, col)
            case "Bishop":
                return self.checkBishop(row, col)
            case "King":
                return self.checkKing(row, col)
            case "Queen":
                return self.checkQueen(row, col)
            case "Knight":
                return self.checkKnight(row, col)
            case "Pawn":
                return self.checkPawn(row, col)
        
    def convertPawn(self):
        n = int(input("Convert Pawn to:\n1. Queen\n2. Rook\n3. Bishop\n4. Knight"))
        match n:
            case 1:
                self.type = "Queen"
                if self.color == "White":
                    self.emoji = white[4]
                    return
                self.emoji = black[4]

            case 2:
                self.type = "Rook"
                if self.color == "White":
                    self.emoji = white[0]
                    return
                self.emoji = black[0]

            case 3:
                self.type = "Bishop"
                if self.color == "White":
                    self.emoji = white[2]
                    return
                self.emoji = black[2]  

            case 4:
                self.type = "Knight"
                if self.color == "White":
                    self.emoji = white[1]
                    return
                self.emoji = black[1]

            case _:
                return self.convertPawn()

    def checkWin(self):
        whiteKing = self.findKing("White")
        blackKing = self.findKing("Black")
        kings = [whiteKing, blackKing]


        for king in kings:

            kingDetectors = king.isPieceDetected()
            movable = king.isKingMovable()

            if not kingDetectors:
                continue

            elif len(kingDetectors) > 1 and not movable:
                print(f"{king.color} King had no way to escape!")
                return 1
            
            else:
                attackerDetectors = kingDetectors[0].isPieceDetected()

                if not attackerDetectors:
                    if not movable:
                        print(f"{king.color} King had no way to escape!")
                        return 1
                    break
                
                break
        
        return 0

                


            
def initBoard():
    board = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append(0)
        board.append(row)

    for i in range(8):
        piece1 = Piece(types[i], "White", 0, i, white[i])
        piece2 = Piece(types[i], "Black", 7, i, black[i])
        
        board[0][i] = piece1
        board[-1][i] = piece2

    for i in range(8):
        piece1 = Piece("Pawn", "White", 1, i, white[-1])
        piece2 = Piece("Pawn", "Black", 6, i, black[-1])

        board[1][i] = piece1
        board[-2][i] = piece2

    for row in range(2, 8 - 2):
        for col in board[row]:
            board[row][col] = 0

    return board

def printBoard(board):
    pad = 10

    cols = ""
    for i in range(0, len(cors)):
        cols += cors[i].rjust(10)

    print(cols)

    for row in range(len(board)-1, -1, -1):
        print("_" * 81)
        figure = str(row + 1)
        for col in range(len(board[0])):
            if board[row][col]:
                figure += board[row][col].emoji.rjust(pad//2) + "|".rjust(pad//2)
                continue
            figure += "|".rjust(pad)
        
        print(figure)

def getRow(text):
    try:
        res = int(input(text))
        if res > 8:
            return getRow(text)
        return res - 1  #since the printed board is indexed from 0
    except:
        return getRow(text)

def getCol(text):
    global cors
    res = input(text)
    if len(res) == 1:    # I could use a dictionary to more more efficient, but no need in this case
        for i in range(len(cors)):
            if cors[i] == res.upper():
                return i
        
    return getCol(text)

def main():
    global board
    board = initBoard()

    i = 0
    row0, col0, row1, col1 = 0, 0, 0, 0
    
    printBoard(board)
    
    while True:

        if i % 2 == 0:
            row0 = getRow("Whites Turn:\n\tRow: ")
            col0 = getCol("\tCol: ")

            if not board[row0][col0]:
                continue

            elif board[row0][col0].color == "Black":
                continue

        else:
            row0 = getRow("Blacks Turn:\n\tRow: ")
            col0 = getCol("\tCol: ")

            if not board[row0][col0]:
                continue

            elif board[row0][col0].color == "White":
                continue

        row1 = getRow("Move To:\n\tRow: ")
        col1 = getCol("\tCol: ")

        if board[row0][col0].type == "King":
            pass

        if not board[row0][col0].isValidMove(row1, col1):
            continue

        elif board[row0][col0].isKingDetectedAfter(row1, col1):
            continue

        board[row0][col0].move(row1, col1)

        printBoard(board)

        if board[row1][col1].checkWin():
            break

        i += 1

    return 0



main()

