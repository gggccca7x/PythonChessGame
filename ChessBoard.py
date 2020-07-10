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
            if pieceNotThere((ix, y), yourPcs):
                moves.append((ix, y))
                if not pieceNotThere((ix, y), oppoPcs): break
            else:
                break
    ix = x
    while ix >= 0:
        ix -= 1
        if ix >= 0:
            if pieceNotThere((ix, y), yourPcs):
                moves.append((ix, y))
                if not pieceNotThere((ix, y), oppoPcs): break
            else:
                break
    iy = y
    while iy <= 7:
        iy += 1
        if iy <= 7:
            if pieceNotThere((x, iy), yourPcs):
                moves.append((x, iy))
                if not pieceNotThere((x, iy), oppoPcs): break
            else:
                break
    iy = y
    while iy >= 0:
        iy -= 1
        if iy >= 0:
            if pieceNotThere((x, iy), yourPcs):
                moves.append((x, iy))
                if not pieceNotThere((x, iy), oppoPcs): break
            else:
                break

    return moves

def getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite):
    moves = []
    if isWhite:
        if pieceNotThere((x,y-1), yourPcs): moves.append((x,y-1))
        if y == 6:
            if pieceNotThere((x,y-2), yourPcs) and pieceNotThere((x,y-1), yourPcs): moves.append((x,y-2))
        # elif y == 1:
            # promote?
        # TODO: account for taking, and then en passant
    else:
        if pieceNotThere((x,y+1), yourPcs): moves.append((x,y+1))
        if y == 1:
            if pieceNotThere((x,y+2), yourPcs) and pieceNotThere((x,y+1), yourPcs): moves.append((x,y+2))
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
    piecesPositions = [(piece.idxX, piece.idxY) for piece in yourPcs]
    myList = [x for x in moves if x not in piecesPositions]
    return myList

# inputs an index tuple (x,y) and your pieces and returns true if your piece isnt there
# or opponenet pieces depending which list put in
def pieceNotThere(pos, pcs):
    piecesPositions = [(piece.idxX, piece.idxY) for piece in pcs]
    return True if pos not in piecesPositions else False
