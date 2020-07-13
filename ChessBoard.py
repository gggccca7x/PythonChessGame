# TODO: rename to "ChessLogic" maybe?

# list of numbers associated to specific type
KING = 0
QUEEN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
PAWN = 5

# return tuples of indexes e.g. (2, 3)
def getAllLegalMoves(x, y, yourPcs, oppoPcs, piece, isWhite):

    king = piece
    for p in yourPcs:
        if p.pType == KING:
            king = p
            break
    inCheck = checkKingInCheck((king.idxX, king.idxY), yourPcs, oppoPcs, isWhite)

    # TODO: complete this with chess logic
    switcher = {
        KING: getKingMoves(x, y, yourPcs, oppoPcs, piece),
        QUEEN: getQueenMoves(x, y, yourPcs, oppoPcs, piece), 
        ROOK: getRookMoves(x, y, yourPcs, oppoPcs, piece), 
        KNIGHT: getKnightMoves(x, y, yourPcs, oppoPcs, piece), 
        BISHOP: getBishopMoves(x, y, yourPcs, oppoPcs, piece), 
        PAWN: getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite)
    }
    return switcher.get(piece.pType, (-1, -1))

# Returns true if king in check, theres probs a better way to do this entire function though tbh
def checkKingInCheck(kPos, yourPcs, oppoPcs, isWhite):
    oppoMoves = []
    inCheck = False
    for p in oppoPcs:
        switcher = {
            # note: had to switch over oppoPcs and yourPcs in these methods
            KING: getKingMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p),
            QUEEN: getQueenMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p), 
            ROOK: getRookMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p), 
            KNIGHT: getKnightMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p), 
            BISHOP: getBishopMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p), 
            PAWN: getPawnMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, not isWhite)
        }
        pieceMoves = switcher.get(p.pType)
        oppoMoves = oppoMoves + pieceMoves
        if (kPos[0], kPos[1]) in pieceMoves:
            print("piece putting them in check: " + str(p.pType))
            inCheck = True

    return inCheck

# TODO: complete except castroling and checks
def getRookMoves(x, y, yourPcs, oppoPcs, piece):
    moves = []
    ix = x
    while ix <= 7:
        ix += 1
        if ix <= 7:
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

# TODO: bishop working perfectly except checks
def getBishopMoves(x, y, yourPcs, oppoPcs, piece):
    moves = []
    ix = x
    iy = y
    while ix <= 7 and iy <= 7:
        ix += 1
        iy += 1
        if ix <= 7 and iy <= 7:
            if pieceNotThere((ix, iy), yourPcs):
                moves.append((ix, iy))
                if not pieceNotThere((ix, iy), oppoPcs): break
            else:
                break
    ix = x
    iy = y
    while ix <= 7 and iy >= 0:
        ix += 1
        iy -= 1
        if ix <= 7 and iy >= 0:
            if pieceNotThere((ix, iy), yourPcs):
                moves.append((ix, iy))
                if not pieceNotThere((ix, iy), oppoPcs): break
            else:
                break
    ix = x
    iy = y
    while ix >= 0 and iy <= 7:
        ix -= 1
        iy += 1
        if ix >= 0 and iy <= 7:
            if pieceNotThere((ix, iy), yourPcs):
                moves.append((ix, iy))
                if not pieceNotThere((ix, iy), oppoPcs): break
            else:
                break
    ix = x
    iy = y
    while ix >= 0 and iy >= 0:
        ix -= 1
        iy -= 1
        if ix >= 0 and iy >= 0:
            if pieceNotThere((ix, iy), yourPcs):
                moves.append((ix, iy))
                if not pieceNotThere((ix, iy), oppoPcs): break
            else:
                break

    return moves

# TODO: knight working perfectly except checks
def getKnightMoves(x, y, yourPcs, oppoPcs, piece):
    moves = []
    ix = x - 2
    iy = y - 1
    if ix >= 0 and iy >= 0 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x - 1
    iy = y - 2
    if ix >= 0 and iy >= 0 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x + 1
    iy = y - 2
    if ix <= 7 and iy >= 0 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x + 2
    iy = y - 1
    if ix <= 7 and iy >= 0 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x + 2
    iy = y + 1
    if ix <= 7 and iy <= 7 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x + 1
    iy = y + 2
    if ix <= 7 and iy <= 7 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x - 2
    iy = y + 1
    if ix >= 0 and iy <= 7 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    ix = x - 1
    iy = y + 2
    if ix >= 0 and iy <= 7 and pieceNotThere((ix,iy), yourPcs):
        moves.append((ix, iy))
    return moves

# TODO: complete except accounting for castling unlike rook this cannot do it and checks
def getQueenMoves(x, y, yourPcs, oppoPcs, piece):
    return getBishopMoves(x, y, yourPcs, oppoPcs, piece) + getRookMoves(x, y, yourPcs, oppoPcs, piece)

# TODO: checks, taking, enpassant
def getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite):
    moves = []
    if isWhite:
        if pieceNotThere((x,y-1), yourPcs) and pieceNotThere((x,y-1), oppoPcs): moves.append((x,y-1))
        # Note: dont need to worry about out of bounds i dont think?
        if not pieceNotThere((x+1,y-1), oppoPcs):
            moves.append((x+1,y-1))
        if not pieceNotThere((x-1,y-1), oppoPcs):
            moves.append((x-1,y-1))
        if y == 6:
            if (pieceNotThere((x,y-2), yourPcs) and pieceNotThere((x,y-1), yourPcs) 
                and pieceNotThere((x,y-2), oppoPcs) and pieceNotThere((x,y-1), oppoPcs)): 
                moves.append((x,y-2))
        # elif y == 1:
            # promote?
        # TODO: account for taking, and then en passant
    else:
        if pieceNotThere((x,y+1), yourPcs) and pieceNotThere((x,y+1), oppoPcs): moves.append((x,y+1))
        # Note: dont need to worry about out of bounds i dont think?
        if not pieceNotThere((x+1,y+1), oppoPcs):
                moves.append((x+1,y+1))
        if not pieceNotThere((x-1,y+1), oppoPcs):
            moves.append((x-1,y+1))
        if y == 1:
            if (pieceNotThere((x,y+2), yourPcs) and pieceNotThere((x,y+1), yourPcs)
                and pieceNotThere((x,y+2), oppoPcs) and pieceNotThere((x,y+1), oppoPcs)): 
                moves.append((x,y+2))
    return moves

# TODO: complete except castroling and checks
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
