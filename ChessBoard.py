# list of numbers associated to specific type
KING = 0
QUEEN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
PAWN = 5

# return tuples of indexes e.g. (2, 3)
def getAllLegalMoves(x, y, yourPcs, oppoPcs, piece, isWhite):

    # TODO: complete this with chess logic
    switcher = {
        KING: getKingMoves(x, y, yourPcs, oppoPcs, piece),
        QUEEN: [(2,0), (2,3)], 
        # ROOK:  [(2,2), (7,3)],
        ROOK: getRookMoves(x, y, yourPcs, oppoPcs, piece), 
        KNIGHT: [(2,2), (7,3)], 
        BISHOP: [(2,5), (5,3)], 
        PAWN: getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite)
    }
    return switcher.get(piece.pType, (-1, -1))

def getRookMoves(x, y, yourPcs, oppoPcs, piece):
    moves = []
    ix = x
    while ix <= 7:
        ix += 1
        if ix <= 7:
            # TODO: if piece already there then return
            moves.append((ix, y))
    ix = x
    while ix >= 0:
        ix -= 1
        if ix >= 0:
            moves.append((ix, y))
    iy = y
    while iy <=  7:
        iy += 1
        if iy <= 7:
            moves.append((x, iy))
    iy = y
    while iy >= 0:
        iy -= 1
        if iy >= 0:
            moves.append((x, iy))

    return moves

def getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite):
    moves = []
    if isWhite:
        if y == 6:
            moves.append((x,y-1))
            moves.append((x,y-2))
        # elif y == 1:
            # promote?
        else:
            moves.append((x,y-1))

        # TODO: account for taking, and then en passant
    else:
        if y == 1:
            moves.append((x,y+1))
            moves.append((x,y+2))
        else:
            moves.append((x,y+1))
    return moves


def getKingMoves(x, y, yourPcs, oppoPcs, piece):
    moves = []
    if y > 0:
        moves.append((x,y-1))
    if y < 7:
        moves.append((x,y+1))
    if x > 0:
        moves.append((x-1,y))
        if y > 0:
            moves.append((x-1,y-1))
        if y < 7:
            moves.append((x-1,y+1))
    if x < 7:
        moves.append((x+1,y))
        if y > 0:
            moves.append((x+1,y-1))
        if y < 7:
            moves.append((x+1,y+1))

    return checkYourPieces(moves, yourPcs)

# input: moves possible by piece, all your chess pieces on the board
# returns list of valid moves if chess piece isnt on that square
def checkYourPieces(moves, yourPcs):
    piecesPositions = [(piece.idxX,piece.idxY) for piece in yourPcs]
    myList = [x for x in moves if x not in piecesPositions]
    return myList