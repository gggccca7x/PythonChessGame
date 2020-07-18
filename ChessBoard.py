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

    # All pieces putting king in check
    # TODO: surely if 2 pieces checking the king, he is FORCED to move?
    # and if 0 pieces checking king, it is fine
    inCheckList = checkKingInCheck((king.idxX, king.idxY), yourPcs, oppoPcs, isWhite, [])
    numCheckingPcs = len(inCheckList)

    if numCheckingPcs == 2:
        if piece.pType == KING:
            return getKingMoves(x, y, yourPcs, oppoPcs, piece, [])
        else:
            return []
    else: 
        # TODO: complete this with chess logic
        switcher = {
            KING: getKingMoves(x, y, yourPcs, oppoPcs, piece, inCheckList),
            QUEEN: getQueenMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            ROOK: getRookMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            KNIGHT: getKnightMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            BISHOP: getBishopMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            PAWN: getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite,inCheckList)
        }
        pieceMoves =  switcher.get(piece.pType, (-1, -1))

        # Loop through every move, make the move in a copied array and confirm if the king is in check after it
        validPieceMoves = []
        for move in pieceMoves:
            yourPcsCopy = yourPcs
            for p in yourPcsCopy:
                if p.idxX == piece.idxX and p.idxY == piece.idxY:
                    p.idxX = move[0]
                    p.idxY = move[1]
            isKingInCheckStill = checkKingInCheck((king.idxX, king.idxY), yourPcsCopy, oppoPcs, isWhite, [])
            print("is king in check: " + str(len(isKingInCheckStill)))
            if len(isKingInCheckStill) == 0:
                validPieceMoves.append(move)

        return validPieceMoves

def returnAllMoves(x, y, yourPcs, oppoPcs, piece, isWhite, inCheckList):
    switcher = {
        KING: getKingMoves(x, y, yourPcs, oppoPcs, piece, inCheckList),
        QUEEN: getQueenMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
        ROOK: getRookMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
        KNIGHT: getKnightMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
        BISHOP: getBishopMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
        PAWN: getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite,inCheckList)
    }
    return switcher.get(piece.pType, (-1, -1))

# Returns true if king in check, theres probs a better way to do this entire function though tbh
def checkKingInCheck(kPos, yourPcs, oppoPcs, isWhite, oppoCheckingPcs):
    oppoPieces = []
    inCheck = False
    for p in oppoPcs:
        switcher = {
            # note: had to switch over oppoPcs and yourPcs in these methods
            KING: getKingMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            QUEEN: getQueenMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ROOK: getRookMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            KNIGHT: getKnightMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            BISHOP: getBishopMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            PAWN: getPawnMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, not isWhite, oppoCheckingPcs)
        }
        pieceMoves = switcher.get(p.pType, (-1, -1))
        if (kPos[0], kPos[1]) in pieceMoves:
            oppoPieces.append(p)

    return oppoPieces

# TODO: complete except castroling and checks
def getRookMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPc):
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
def getBishopMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs):
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
def getKnightMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs):
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
def getQueenMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs):
    return getBishopMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs) + getRookMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs)

# TODO: checks, taking, enpassant
def getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite, oppoCheckingPcs):
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
def getKingMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs):
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
