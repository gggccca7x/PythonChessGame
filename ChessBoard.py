class ChessPiece(object):
    def __init__(self, image, idxX, idxY):
        self.image = image
        pos = getPosFromIndex(idxX, idxY)
        self.idxX = idxX
        self.idxY = idxY
        self.posX = pos[0]
        self.posY = pos[1]

#input index (0-7) as chessboard is 8x8
def getPosFromIndex(x, y):
    return (cb_bx1 + x * w_per_sq, cb_by1 + y * w_per_sq)

def getIndexFromPos(x, y):
    posX, posY = -1, -1
    for i in range(len(list_sq_end)):
        if x <= list_sq_end[i]:
            posX = i
            break
    for i in range(len(list_sq_end)):
        if y <= list_sq_end[i]:
            posY = i
            break
    if posX == -1 or posY == -1 or x < cb_bx1 or y < cb_by1:
        posX, posY = -1, -1
    return (posX, posY)

def getAllLegalMoves(oX, oY, toX, toY, yourPcs, oppoPcs, piece):
    

    return []