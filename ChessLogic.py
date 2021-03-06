class ChessPiece(object):
    def __init__(self, image, idx, pos, pType):
        self.image = image
        self.idxX = idx[0]
        self.idxY = idx[1]
        self.posX = pos[0]
        self.posY = pos[1]
        self.pType = pType

    def setNewPosition(self, idx, pos):
        self.idxX = idx[0]
        self.idxY = idx[1]
        self.posX = pos[0]
        self.posY = pos[1]

# list of numbers associated to specific type
class ChessPieceTypes:
    KING = 0
    QUEEN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    PAWN = 5

class CastlingLogic:
     def __init__(self):
        # to check for castling
        self.hasWhiteCastled = False
        self.hasWhiteMoved_A_Rook = False
        self.hasWhiteMoved_H_Rook = False
        self.hasWhiteMovedKing = False

        self.hasBlackCastled = False
        self.hasBlackMoved_A_Rook = False
        self.hasBlackMoved_H_Rook = False
        self.hasBlackMovedKing = False

# to check for en passant
opponentLastMovePawn2Spaces = False
opponentLastMovePawnLocation = (-1,-1)

# returns list of tuples of indexes e.g. [(3, 3), (4, 4)]
def getAllLegalMoves(x, y, yourPcs, oppoPcs, piece, isWhite, oppLasMovPaw2, oppLasMovPawIdx, castlingLogic):

    validPieceMoves = []

    king = piece
    for p in yourPcs:
        if p.pType == ChessPieceTypes.KING:
            king = p
            break

    # All pieces putting king in check
    # if 2 pieces checking the king, he is FORCED to move
    inCheckList = checkKingInCheck((king.idxX, king.idxY), yourPcs, oppoPcs, isWhite, [], oppLasMovPaw2, oppLasMovPawIdx)
    numCheckingPcs = len(inCheckList)

    # to account for castling
    allOppMoves = getAllOpponentNextTurnMoves(yourPcs, oppoPcs, isWhite, [], oppLasMovPaw2, oppLasMovPawIdx)
    if numCheckingPcs < 1:
        if piece.pType == ChessPieceTypes.KING:
            if isWhite:
                if not castlingLogic.hasWhiteCastled and not castlingLogic.hasWhiteMovedKing:
                    validPieceMoves.extend(checkCastlingPossible(yourPcs, oppoPcs, isWhite, castlingLogic.hasWhiteMoved_A_Rook, castlingLogic.hasWhiteMoved_H_Rook, allOppMoves))
            else:
                if not castlingLogic.hasBlackCastled and not castlingLogic.hasBlackMovedKing:
                    validPieceMoves.extend(checkCastlingPossible(yourPcs, oppoPcs, isWhite, castlingLogic.hasBlackMoved_A_Rook, castlingLogic.hasBlackMoved_H_Rook, allOppMoves))

    if numCheckingPcs == 2:
        if piece.pType == ChessPieceTypes.KING:
            return getKingMoves(x, y, yourPcs, oppoPcs, piece, [])
        else:
            return []
    else: 
        switcher = {
            ChessPieceTypes.KING: getKingMoves(x, y, yourPcs, oppoPcs, piece, inCheckList),
            ChessPieceTypes.QUEEN: getQueenMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            ChessPieceTypes.ROOK: getRookMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            ChessPieceTypes.KNIGHT: getKnightMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            ChessPieceTypes.BISHOP: getBishopMoves(x, y, yourPcs, oppoPcs, piece, inCheckList), 
            ChessPieceTypes.PAWN: getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite, inCheckList, oppLasMovPaw2, oppLasMovPawIdx)
        }
        pieceMoves =  switcher.get(piece.pType, (-1, -1))

        # Loop through every move, make the move in a copied array and confirm if the king is in check after it
        for move in pieceMoves:
            yourPcsCopy = yourPcs
            for p in yourPcsCopy:
                if p.idxX == piece.idxX and p.idxY == piece.idxY:
                    p.idxX = move[0]
                    p.idxY = move[1]
            isKingInCheckStill = checkKingInCheck((king.idxX, king.idxY), yourPcsCopy, oppoPcs, isWhite, [], oppLasMovPaw2, oppLasMovPawIdx)
            if len(isKingInCheckStill) == 0 or (isKingInCheckStill[0].idxX == move[0] and isKingInCheckStill[0].idxY == move[1]):
                validPieceMoves.append(move)

        return validPieceMoves

# Returns list of pieces which are checking opponents king
def checkKingInCheck(kPos, yourPcs, oppoPcs, isWhite, oppoCheckingPcs, oppLasMovPaw2, oppLasMovPawIdx):
    oppoPieces = []
    inCheck = False
    for p in oppoPcs:
        switcher = {
            # note: had to switch over oppoPcs and yourPcs in these methods
            ChessPieceTypes.KING: getKingMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            ChessPieceTypes.QUEEN: getQueenMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.ROOK: getRookMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.KNIGHT: getKnightMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.BISHOP: getBishopMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            ChessPieceTypes.PAWN: getPawnMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, not isWhite, oppoCheckingPcs, oppLasMovPaw2, oppLasMovPawIdx)
        }
        pieceMoves = switcher.get(p.pType, (-1, -1))
        if (kPos[0], kPos[1]) in pieceMoves:
            oppoPieces.append(p)

    return oppoPieces

def getAllOpponentNextTurnMoves(yourPcs, oppoPcs, isWhite, oppoCheckingPcs, oppLasMovPaw2, oppLasMovPawIdx):
    oppoPieces = []
    for p in oppoPcs:
        switcher = {
            # note: had to switch over oppoPcs and yourPcs in these methods
            ChessPieceTypes.KING: getKingMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            ChessPieceTypes.QUEEN: getQueenMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.ROOK: getRookMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.KNIGHT: getKnightMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs), 
            ChessPieceTypes.BISHOP: getBishopMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, oppoCheckingPcs),
            ChessPieceTypes.PAWN: getPawnMoves(p.idxX, p.idxY, oppoPcs, yourPcs, p, not isWhite, oppoCheckingPcs, oppLasMovPaw2, oppLasMovPawIdx)
        }
        pieceMoves = switcher.get(p.pType, (-1, -1))
        oppoPieces.extend(pieceMoves)

    return oppoPieces

def checkCastlingPossible(yourPcs, oppoPcs, isWhite, moved_A_Rook, moved_H_Rook, allOppMoves):
    castlingMoves = []
    if not moved_A_Rook:
        if isWhite:
            if (pieceNotThere((1,7), yourPcs) and pieceNotThere((1,7), oppoPcs)
                and pieceNotThere((2,7), yourPcs) and pieceNotThere((2,7), oppoPcs)
                and pieceNotThere((3,7), yourPcs) and pieceNotThere((3,7), oppoPcs)
                and itemNotInList((1,7), allOppMoves) and itemNotInList((2,7), allOppMoves) and itemNotInList((3,7), allOppMoves)):
                    castlingMoves.append((2,7))
        else:
            if (pieceNotThere((1,0), yourPcs) and pieceNotThere((1,0), oppoPcs)
                and pieceNotThere((2,0), yourPcs) and pieceNotThere((2,0), oppoPcs)
                and pieceNotThere((3,0), yourPcs) and pieceNotThere((3,0), oppoPcs)
                and itemNotInList((1,0), allOppMoves) and itemNotInList((2,0), allOppMoves) and itemNotInList((3,0), allOppMoves)):
                    castlingMoves.append((2,0))
    if not moved_H_Rook:
        if isWhite:
            if (pieceNotThere((5,7), yourPcs) and pieceNotThere((5,7), oppoPcs)
                and pieceNotThere((6,7), yourPcs) and pieceNotThere((6,7), oppoPcs)
                and itemNotInList((5,7), allOppMoves) and itemNotInList((6,7), allOppMoves)):
                    castlingMoves.append((6,7))
        else:
            if (pieceNotThere((5,0), yourPcs) and pieceNotThere((5,0), oppoPcs)
                and pieceNotThere((6,0), yourPcs) and pieceNotThere((6,0), oppoPcs)
                and itemNotInList((5,0), allOppMoves) and itemNotInList((6,0), allOppMoves)):
                    castlingMoves.append((6,0))

    return castlingMoves


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

def getQueenMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs):
    return getBishopMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs) + getRookMoves(x, y, yourPcs, oppoPcs, piece, oppoCheckingPcs)

def getPawnMoves(x, y, yourPcs, oppoPcs, piece, isWhite, oppoCheckingPcs, oppLasMovPaw2, oppLasMovPawIdx):
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
        if y == 3 and oppLasMovPaw2:
            if abs(x - oppLasMovPawIdx[0]) == 1:
                moves.append((oppLasMovPawIdx[0],y-1))
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
        if y == 4 and oppLasMovPaw2:
            if abs(x - oppLasMovPawIdx[0]) == 1:
                moves.append((oppLasMovPawIdx[0],y+1))
    return moves

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

# check if item in list or not
def itemNotInList(pos, lis):
    return True if pos not in lis else False
