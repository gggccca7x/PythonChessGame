import pygame

# TODO: Have a REDAME.MD
# Include something like: Please note - I am using a python interpreter with a conda environement...

# TODO: bring to front the selected piece (move to bottom of the list)
# TODO: fix bug cant move piece if goes off screen - i think done, double check
# TODO: better naming conventions such as the validMoves in the unclick mouse in the game loop

class ChessPiece(object):
    def __init__(self, image, idxX, idxY):
        self.image = image
        pos = getPosFromIndex(idxX, idxY)
        self.idxX = idxX
        self.idxY = idxY
        self.posX = pos[0]
        self.posY = pos[1]

pygame.init()
win = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Chess Game")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Chess Board bound constants
cb_bx1, cb_bx2, cb_by1, cb_by2 = 50, 850, 50, 850
w_per_sq = 100
list_sq_end = [cb_bx1 + w_per_sq , cb_bx1 + w_per_sq * 2, 
                cb_bx1 + w_per_sq * 3, cb_bx1 + w_per_sq * 4,
                cb_bx1 + w_per_sq * 5, cb_bx1 + w_per_sq * 6,
                cb_bx1 + w_per_sq * 7, cb_bx1 + w_per_sq * 8]

def drawLines():
    for x in range(0,9):
        pygame.draw.line(win, WHITE, (cb_bx1, cb_by1 + w_per_sq * x), (cb_bx2, cb_by1 + w_per_sq * x))
        pygame.draw.line(win, WHITE, (cb_bx1 + w_per_sq * x, cb_by1), (cb_bx1 + w_per_sq * x, cb_by2))

def draw():
    for c in whiteChessPieces:
        win.blit(c.image, (c.posX, c.posY))
    for c in blackChessPieces:
        win.blit(c.image, (c.posX, c.posY))
    drawLines()

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

def checkIfPieceAlreadyThere(posX, posY, piece, whiteTurn):
    yourPieces = blackChessPieces
    opponentPieces = whiteChessPieces
    if whiteTurn:
        yourPieces = whiteChessPieces
        opponentPieces = blackChessPieces

    for i in range(len(yourPieces)):
        if posX == yourPieces[i].posX and posY == yourPieces[i].posY and piece is not yourPieces[i]:
            return False
    for i in range(len(opponentPieces)):
        if posX == opponentPieces[i].posX and posY == opponentPieces[i].posY and piece is not opponentPieces[i]:
            opponentPieces.remove(opponentPieces[i])
            return True
    return True

#indexes of from and to squares to confirm if valid move - need actual chess rules
def confirmValidity(xFrom, yFrom, xTo, yTo):
    if xFrom == xTo and yFrom == yTo:
        return False
    return True

w_rook_image = pygame.image.load(".\images\white_rook.png")
w_rook_image = pygame.transform.scale(w_rook_image, (100,100))
w_knight_image = pygame.image.load(".\images\white_knight.png")
w_knight_image = pygame.transform.scale(w_knight_image, (100,100))
w_rook = ChessPiece(w_rook_image, 0, 0)
w_rook2 = ChessPiece(w_rook_image, 1, 1)
w_knight = ChessPiece(w_knight_image, 2, 2)
w_knight2 = ChessPiece(w_knight_image, 2, 3)
whiteChessPieces = [w_rook, w_rook2, w_knight, w_knight2]

b_rook_image = pygame.image.load(".\images\\black_rook.png")
b_rook_image = pygame.transform.scale(b_rook_image, (100,100))
b_knight_image = pygame.image.load(".\images\\black_knight.png")
b_knight_image = pygame.transform.scale(b_knight_image, (100,100))
b_rook = ChessPiece(b_rook_image, 7, 0)
b_rook2 = ChessPiece(b_rook_image, 7, 1)
b_knight = ChessPiece(b_knight_image, 7, 2)
b_knight2 = ChessPiece(b_knight_image, 7, 3)
blackChessPieces = [b_rook, b_rook2, b_knight, b_knight2]

# Initialisations dont matter tbh
original_idx_x = 0
original_idx_y = 1
dragged_piece = w_rook
is_dragging_piece = False

run = True
isWhitesMove = True

while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                index = getIndexFromPos(mouse_x, mouse_y)
                chessPieces = whiteChessPieces if isWhitesMove else blackChessPieces
                for c in chessPieces:
                    if index[0] == c.idxX and index[1] == c.idxY:
                        dragged_piece = c
                        is_dragging_piece = True
                        break
                if is_dragging_piece:
                    dragged_piece.posX = mouse_x - w_per_sq/2
                    dragged_piece.posY = mouse_y - w_per_sq/2
                    offset_x = dragged_piece.posX - mouse_x
                    offset_y = dragged_piece.posY - mouse_y
                    original_idx_x, original_idx_y = getIndexFromPos(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if is_dragging_piece:
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    validMove = checkIfPieceAlreadyThere(pos[0], pos[1], dragged_piece, isWhitesMove)
                    if idx[0] == -1 or not validMove:
                        pos = getPosFromIndex(original_idx_x, original_idx_y)
                        idx = (original_idx_x, original_idx_y)
                        validMove = False
                    is_dragging_piece = False
                    dragged_piece.posX = pos[0]
                    dragged_piece.idxX = idx[0]
                    dragged_piece.posY = pos[1]
                    dragged_piece.idxY = idx[1]
                    validReposition = confirmValidity(original_idx_x, original_idx_y, idx[0], idx[1])
                    if validMove and validReposition:
                        # TODO: check actual valid move, i.e. not clicking the same square as currently on
                        isWhitesMove = not isWhitesMove
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging_piece:
                mouse_x, mouse_y = event.pos
                dragged_piece.posX = mouse_x + offset_x
                dragged_piece.posY = mouse_y + offset_y

    win.fill(BLUE)
    draw()
    pygame.display.update()

pygame.quit()
