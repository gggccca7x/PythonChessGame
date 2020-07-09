# list of numbers associated to specific type
KING = 0
QUEEN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
PAWN = 5

# return tuples of indexes e.g. (2, 3)
def getAllLegalMoves(x, y, yourPcs, oppoPcs, piece):

    # TODO: complete this with chess logic
    print("position x: " + str(x))
    print("position y: " + str(y))
    switcher = {
        KING: getKingMoves(x, y, yourPcs, oppoPcs, piece),
        QUEEN: [(2,0), (2,3)], 
        ROOK: [(2,2), (2,4)], 
        KNIGHT: [(2,2), (7,3)], 
        BISHOP: [(2,5), (5,3)], 
        PAWN: [(2,7), (7,7)]
    }
    return switcher.get(piece.pType, (-1, -1))

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

    # TODO: remove copies - create a new list maybe?
    return moves
