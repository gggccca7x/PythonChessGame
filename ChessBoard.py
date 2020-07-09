# list of numbers associated to specific type
KING = 0
QUEEN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
PAWN = 5

# return tuples of indexes e.g. (2, 3)
def getAllLegalMoves(oX, oY, yourPcs, oppoPcs, piece):

    # TODO: complete this with chess logic
    switcher = {
        KING: [(0,0), (1,0)],
        QUEEN: [(2,0), (2,3)], 
        ROOK: [(2,2), (2,4)], 
        KNIGHT: [(2,2), (7,3)], 
        BISHOP: [(2,5), (5,3)], 
        PAWN: [(2,7), (7,7)]
    }
    return switcher.get(piece.pType, (-1, -1))
