from copy import deepcopy
from random import shuffle

#Movement offset arrays
knightOffset = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
bishopOffset = [(1,1),(-1,-1),(-1,1),(1,-1)]
rookOffset = [(1,0),(-1,0),(0,1),(0,-1)]
kingOffset = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
promotionPieces = ['Queen', 'Rook', 'Knight', 'Bishop']
#Pawn, Knight, Bishop, Rook, Queen
pieceVals = {'p':1, 'b':3, 'n':3, 'r':5, 'q':8}

class Action:
    def __init__(self, piece, x1, y1, x2, y2, promotion=''):
        self.val = 0
        self.piece = piece
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.promotion = promotion

    def __eq__(self, other):
        return self.piece == other.piece and self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2 and self.promotion == other.promotion

    def __hash__(self):
        p = 0
        if self.promotion:
            for i in self.promotion+self.piece:
                p += ord(i)
            return p+self.x1+self.x2+self.y1+self.y2
        else:
            for i in self.piece:
                p += ord(i)
            return p+self.x1+self.x2+self.y1+self.y2


class State:

    def __init__(self, color):
        self.color = color
        self.board = [[' '] * 8 for i in range(8)]
        self.WKingSideCastle = False
        self.WQueenSideCastle = False
        self.BKingSideCastle = False
        self.BQueenSideCastle = False
        self.enPass = ''

    def init_fen(self, fen):
        x = 0
        y = 7
        end = 0
        for char in fen:
            if char.isalpha():
                self.board[x][y] = char
                x += 1
                end += 1
            elif char.isdigit():
                for _ in range(int(char)):
                    self.board[x][y] = ' '
                    x += 1
                end += 1
            elif char == '/':
                y -= 1
                x = 0
                end += 1
            else:
                end += 3
                break

        if fen[end] == 'K':
            self.WKingSideCastle = True
            end += 1
        if fen[end] == 'Q':
            self.WQueenSideCastle = True
            end += 1
        if fen[end] == 'k':
            self.BKingSideCastle = True
            end += 1
        if fen[end] == 'q':
            self.BQueenSideCastle = True
            end += 1
    
    def actions(self):
        list = []
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece == ' ':
                    continue
                #White
                elif self.color == 'White' and piece.isupper():
                    #Gives Pawn actions
                    if piece == 'P':
                        list += self.getPawnActions(x, y)
                    #Gives Knight actions
                    if piece == 'N':
                        list += self.getKnightActions(x, y)
                    #Gives Bishop actions
                    if piece == 'B':
                        list += self.getBishopActions(x, y,)
                    #Gives Rook actions
                    if piece == 'R':
                        list += self.getRookActions(x, y)
                    #Gives Queen actions
                    if piece == 'Q':
                        list += self.getQueenActions(x, y)
                    #Gives King actions
                    if piece == 'K':
                        list += self.getKingActions(x, y)
                    
                #Black
                elif self.color == 'Black' and piece.islower():
                    #Gives Pawn actions
                    if piece == 'p':
                        list += self.getPawnActions(x, y)
                    #Gives Knight actions
                    if piece == 'n':
                        list += self.getKnightActions(x, y)
                    #Gives Bishop actions
                    if piece == 'b':
                        list += self.getBishopActions(x, y)
                    #Gives Rook actions
                    if piece == 'r':
                        list += self.getRookActions(x, y)
                    #Gives Queen actions
                    if piece == 'q':
                        list += self.getQueenActions(x, y)
                    #Gives King actions
                    if piece == 'k':
                        list += self.getKingActions(x, y)
        shuffle(list)
        return list

    def getPawnActions(self, x, y):
        list = []
        dir = 1 if self.color == 'White' else -1
        #Single Move
        if self.isEmpty(x, y+(1*dir)):
            #Check promotion
            if self.color == 'White' and y+1 == 7:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x, y+(1*dir), p))
            elif self.color == 'Black' and y-1 == 0:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x, y+(1*dir), p))
            else:
                self.addAction(list, Action('Pawn', x, y, x, y+(1*dir)))
            #Double Move
            #White
            if y == 1 and dir == 1 and self.isEmpty(x, y+(2*dir)):
                self.addAction(list, Action('Pawn', x, y, x, y+(2*dir)))
            #Black
            elif y == 6 and dir == -1 and self.isEmpty(x, y+(2*dir)):
                self.addAction(list, Action('Pawn', x, y, x, y+(2*dir)))
        #Capture left(a side)
        if self.isOpponent(x-1, y+(1*dir)):
            #Check promotion
            if self.color == 'White' and y+1 == 7:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x-1, y+(1*dir), p))
            elif self.color == 'Black' and y-1 == 0:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x-1, y+(1*dir), p))
            else:
                self.addAction(list, Action('Pawn', x, y, x-1, y+(1*dir)))
        #Capture right(h side)
        if self.isOpponent(x+1, y+(1*dir)):
            #Check promotion
            if self.color == 'White' and y+1 == 7:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x+1, y+(1*dir), p))
            elif self.color == 'Black' and y-1 == 0:
                for p in promotionPieces:
                    self.addAction(list, Action('Pawn', x, y, x+1, y+(1*dir), p))
            else:
                self.addAction(list, Action('Pawn', x, y, x+1, y+(1*dir)))
        
        #En passant left white
        if y == 4 and self.enPass == (x-1, y+1):
            self.addAction(list, Action('Pawn', x, y, x-1, y+1))
        #En passant right white
        if y == 4 and self.enPass == (x+1, y+1):
            self.addAction(list, Action('Pawn', x, y, x+1, y+1))
        #En passant left black
        if y == 3 and self.enPass == (x-1, y-1):
            self.addAction(list, Action('Pawn', x, y, x-1, y-1))
        #En passant right black
        if y == 3 and self.enPass == (x+1, y-1):
            self.addAction(list, Action('Pawn', x, y, x+1, y-1))
        return list

    def getKnightActions(self, x, y):
        list = []
        for offset in knightOffset:
            if self.isEmpty(x+offset[0], y+offset[1]) or self.isOpponent(x+offset[0], y+offset[1]):
                self.addAction(list, Action('Knight', x, y, x+offset[0], y+offset[1]))
        return list

    def getBishopActions(self, x, y):
        list = []
        for offset in bishopOffset:
            tempx = offset[0]
            tempy = offset[1]
            while self.isEmpty(x+tempx, y+tempy):
                self.addAction(list, Action('Bishop', x, y, x+tempx, y+tempy))
                tempx += offset[0]
                tempy += offset[1]
            if self.isOpponent(x+tempx, y+tempy):
                self.addAction(list, Action('Bishop', x, y, x+tempx, y+tempy))
        return list

    def getRookActions(self, x, y):
        list = []
        for offset in rookOffset:
            tempx = offset[0]
            tempy = offset[1]
            while self.isEmpty(x+tempx, y+tempy):
                self.addAction(list, Action('Rook', x, y, x+tempx, y+tempy))
                tempx += offset[0]
                tempy += offset[1]
            if self.isOpponent(x+tempx, y+tempy):
                self.addAction(list, Action('Rook', x, y, x+tempx, y+tempy))
        return list

    def getQueenActions(self, x, y):
        list = []
        for offset in bishopOffset + rookOffset:
            tempx = offset[0]
            tempy = offset[1]
            while self.isEmpty(x+tempx, y+tempy):
                self.addAction(list, Action('Queen', x, y, x+tempx, y+tempy))
                tempx += offset[0]
                tempy += offset[1]
            if self.isOpponent(x+tempx, y+tempy):
                self.addAction(list, Action('Queen', x, y, x+tempx, y+tempy))
        return list

    def getKingActions(self, x, y):
        list = []
        for offset in kingOffset:
            if (self.isEmpty(x+offset[0], y+offset[1]) or self.isOpponent(x+offset[0], y+offset[1])) and not self.nearKing(x+offset[0], y+offset[1]):
                self.addAction(list, Action('King', x, y, x+offset[0], y+offset[1]))
        #Castling logic
        if self.color == 'White':
            if self.WKingSideCastle and self.isEmpty(x+1, y) and self.isEmpty(x+2, y):
                if not self.isCheck(Action('King', x, y, x, y)) and not self.isCheck(Action('King', x, y, x+1, y)):
                    self.addAction(list, Action('King', x, y, x+2, y))
            if self.WQueenSideCastle and self.isEmpty(x-1, y) and self.isEmpty(x-2, y) and self.isEmpty(x-3, y):
                if not self.isCheck(Action('King', x, y, x, y)) and not self.isCheck(Action('King', x, y, x-1, y)):
                    self.addAction(list, Action('King', x, y, x-2, y))
        else:
            if self.BKingSideCastle and self.isEmpty(x+1, y) and self.isEmpty(x+2, y):
                if not self.isCheck(Action('King', x, y, x, y)) and not self.isCheck(Action('King', x, y, x+1, y)):
                    self.addAction(list, Action('King', x, y, x+2, y))
            if self.BQueenSideCastle and self.isEmpty(x-1, y) and self.isEmpty(x-2, y) and self.isEmpty(x-3, y):
                if not self.isCheck(Action('King', x, y, x, y)) and not self.isCheck(Action('King', x, y, x-1, y)):
                    self.addAction(list, Action('King', x, y, x-2, y))
        return list

    def isCheck(self, action):
        x1, y1 = action.x1, action.y1
        x2, y2 = action.x2, action.y2
        origPiece = self.board[x2][y2]
        #Makes swap
        self.board[x1][y1], self.board[x2][y2] = ' ', self.board[x1][y1]

        #Gets king location of player
        king_x = 0
        king_y = 0
        for y in range(8):
            for x in range(8):
                #if white
                if self.board[x][y] == 'K' and self.color == 'White':
                    king_x, king_y = x, y
                if self.board[x][y] == 'k' and self.color == 'Black':
                    king_x, king_y = x, y
        
        #Checks Pawn checks
        if self.color == 'White':
            if isInBoard(king_x-1, king_y+1) and self.board[king_x-1][king_y+1] == 'p':
                self.board[x1][y1] = self.board[x2][y2]
                self.board[x2][y2] = origPiece
                return True
            if isInBoard(king_x+1, king_y+1) and self.board[king_x+1][king_y+1] == 'p':
                self.board[x1][y1] = self.board[x2][y2]
                self.board[x2][y2] = origPiece
                return True
        else:
            if isInBoard(king_x-1, king_y-1) and self.board[king_x-1][king_y-1] == 'P':
                self.board[x1][y1] = self.board[x2][y2]
                self.board[x2][y2] = origPiece
                return True
            if isInBoard(king_x+1, king_y-1) and self.board[king_x+1][king_y-1] == 'P':
                self.board[x1][y1] = self.board[x2][y2]
                self.board[x2][y2] = origPiece
                return True

        #Checks Knight checks
        for offset in knightOffset:
            if isInBoard(king_x+offset[0], king_y+offset[1]):
                piece = self.board[king_x+offset[0]][king_y+offset[1]]
                #For White
                if piece != ' ' and piece == 'n' and self.color == 'White':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True
                #For Black
                elif piece != ' ' and piece == 'N' and self.color == 'Black':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True

        #Checks Bishop/Queen checks
        for offset in bishopOffset:
            tempx = offset[0]
            tempy = offset[1]
            while self.isEmpty(king_x+tempx, king_y+tempy):
                tempx += offset[0]
                tempy += offset[1]
            if isInBoard(king_x+tempx, king_y+tempy):
                piece = self.board[king_x+tempx][king_y+tempy]
                #For White
                if (piece == 'q' or piece == 'b') and self.color == 'White':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True
                elif (piece == 'Q' or piece == 'B') and self.color == 'Black':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True

        #Checks Rook/Queen checks
        for offset in rookOffset:
            tempx = offset[0]
            tempy = offset[1]
            while self.isEmpty(king_x+tempx, king_y+tempy):
                tempx += offset[0]
                tempy += offset[1]
            if isInBoard(king_x+tempx, king_y+tempy):
                piece = self.board[king_x+tempx][king_y+tempy]
                #For White
                if (piece == 'q' or piece == 'r') and self.color == 'White':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True
                elif (piece == 'Q' or piece == 'R') and self.color == 'Black':
                    self.board[x1][y1] = self.board[x2][y2]
                    self.board[x2][y2] = origPiece
                    return True

        #Swap back
        self.board[x1][y1] = self.board[x2][y2]
        self.board[x2][y2] = origPiece
        return False

    def isDraw(self):
        #Black bishops are even adds, white are odd adds
        mypieces = {'p':0, 'bw':0, 'bb':0, 'n':0, 'r':0, 'q':0}
        oppieces = {'p':0, 'bw':0, 'bb':0, 'n':0, 'r':0, 'q':0}
        for x in range(8):
            for y in range(8):
                char = self.board[x][y]
                if char == ' ' or char == 'K' or char == 'k':
                    continue
                elif char.islower():
                    if char == 'b':
                        if (x+y) % 2 == 0:
                            char += 'b'
                        else:
                            char += 'w'
                    if self.color == 'White':
                        oppieces[char] += 1
                    else:
                        mypieces[char] += 1
                elif char.isupper():
                    char = char.lower()
                    if char == 'b':
                        if (x+y) % 2 == 0:
                            char += 'b'
                        else:
                            char += 'w'
                    if self.color == 'White':
                        mypieces[char] += 1
                    else:
                        oppieces[char] += 1
        mytemp = 0
        optemp = 0
        for k, v in mypieces.items():
            mytemp += v
        for k, v in oppieces.items():
            optemp += v
        #If only kings
        if mytemp == 0 and optemp == 0:
            return True
        #If king bishop
        elif (mytemp == 0 and optemp == 1 and (oppieces['bb'] == 1 or oppieces['bw'] == 1)) or (optemp == 0 and mytemp == 1 and (mypieces['bb'] == 1 or mypieces['bw'] == 1)):
            return True
        #If king knight
        elif (mytemp == 0 and optemp == 1 and oppieces['n'] == 1) or (optemp == 0 and mytemp == 1 and mypieces['n'] == 1):
            return True
        #If king with 2 same color bishops
        elif (mytemp == 0 and optemp == 2 and (oppieces['bw'] == 2 or oppieces['bb'] == 2)) or (optemp == 0 and mytemp == 2 and (mypieces['bw'] == 2 or mypieces['bb'] == 2)):
            return True
        return False

    def isCheckmated(self):
        #Gets king
        king_x, king_y = 0, 0
        for x in range(8):
            for y in range(8):
                if self.color == 'White' and self.board[x][y] == 'K':
                    king_x, king_y = x, y
                elif self.color == 'Black' and self.board[x][y] == 'k':
                    king_x, king_y = x, y
        list = self.actions()
        #If Check and no moves
        if self.isCheck(Action('King', x, y, x, y)) and not list:
            return True
        return False

    def isCheckmating(self):
        #Gets king
        king_x, king_y = 0, 0
        opstate = None
        for x in range(8):
            for y in range(8):
                if self.color == 'White' and self.board[x][y] == 'k':
                    king_x, king_y = x, y
                    opstate = deepcopy(self)
                    opstate.color = 'Black'
                elif self.color == 'Black' and self.board[x][y] == 'K':
                    king_x, king_y = x, y
                    opstate = deepcopy(self)
                    opstate.color = 'White'
        
        list = opstate.actions()
        #If Check and no moves
        if opstate.isCheck(Action('King', x, y, x, y)) and not list:
            return True
        return False

    def isStalemate(self):
        #Gets king
        king_x, king_y = 0, 0
        for x in range(8):
            for y in range(8):
                if self.color == 'White' and self.board[x][y] == 'K':
                    king_x, king_y = x, y
                elif self.color == 'Black' and self.board[x][y] == 'k':
                    king_x, king_y = x, y
        list = self.actions()
        #If Check and no moves
        if not self.isCheck(Action('King', x, y, x, y)) and not list:
            return True
        return False

    def addAction(self, list, action):
        if not self.isCheck(action):
            #Gets piece type
            list.append(action)

    def isOpponent(self, x, y):
        #Is in board?
        if not isInBoard(x, y) or self.board[x][y] == ' ':
            return False
        else:
            if self.color == 'White':
                return self.board[x][y].islower()
            else:
                return self.board[x][y].isupper()

    def isEmpty(self, x, y):
        #Is in board?
        if not isInBoard(x, y):
            return False
        else:
            return self.board[x][y] == ' '

    def nearKing(self, x, y):
        if self.color == 'White':
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'k':
                        list = []
                        for offset in kingOffset:
                            list.append((i+offset[0], j+offset[1]))
                        return (x, y) in list
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'K':
                        list = []
                        for offset in kingOffset:
                            list.append((i+offset[0], j+offset[1]))
                        return (x, y) in list

    def isQuiessant(self):
        #For check
        king_x, king_y = 0, 0
        for x in range(8):
            for y in range(8):
                if self.color == 'White' and self.board[x][y] == 'K':
                    king_x, king_y = x, y
                elif self.color == 'Black' and self.board[x][y] == 'k':
                    king_x, king_y = x, y
        list = self.actions()
        #If Check
        if self.isCheck(Action('King', x, y, x, y)) and list:
            return False
        return True

    #Returns player's value - opponent's value
    def heuristic(self):
        #If Checkmated
        if self.isCheckmated():
            return -100
        #If Checkmating
        elif self.isCheckmating():
            return 100
        #If draw/stalemate
        elif self.isDraw() or self.isStalemate():
            return -50
        else:
            val = 0
            for x in range(8):
                for y in range(8):
                    char = self.board[x][y]
                    if char == ' ' or char == 'K' or char == 'k':
                        continue
                    elif char.islower():
                        if self.color == 'White':
                            val -= pieceVals[char]
                        else:
                            val += pieceVals[char]
                    else:
                        if self.color == 'White':
                            val += pieceVals[char.lower()]
                        else:
                            val -= pieceVals[char.lower()]
            return val

    #Checks for checkmate/stalemate/draw
    def isterminal(self):
        #Draw
        if self.isDraw():
            return True
        #If Checkmates
        elif self.isCheckmated() or self.isCheckmating():
            return True
        #If Stalemate
        elif self.isStalemate():
            return True
        return False

#Returns whether the file/rank of a piece is within the board
#and file/rank is 0-7/0-7
def isInBoard(x, y):
    return (x >= 0 and x <= 7 and y >= 0 and y <= 7)
