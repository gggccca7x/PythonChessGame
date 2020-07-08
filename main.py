import pygame

# TODO: Have a REDAME.MD
# Include something like: Please note - I am using a python interpreter with a conda environement...

# TODO: bring to front the selected piece (move to bottom of the list)
# TODO: make pieces selectable and draggable like the coloured rectangles are

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

run = True

def drawLines():
    for x in range(0,9):
        pygame.draw.line(win, WHITE, (cb_bx1, cb_by1 + w_per_sq * x), (cb_bx2, cb_by1 + w_per_sq * x))
        pygame.draw.line(win, WHITE, (cb_bx1 + w_per_sq * x, cb_by1), (cb_bx1 + w_per_sq * x, cb_by2))

def draw():
    for c in chessPieces:
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

def checkIfPieceAlreadyThere(posX, posY, piece):
    for i in range(len(chessPieces)):
        if posX == chessPieces[i].posX and posY == chessPieces[i].posY and piece is not chessPieces[i]:
            chessPieces.remove(chessPieces[i])
            break

rook_image = pygame.image.load(".\images\white_rook.png")
rook_image = pygame.transform.scale(rook_image, (100,100))
rook = ChessPiece(rook_image, 0, 0)
rook2 = ChessPiece(rook_image, 1, 1)
rook3 = ChessPiece(rook_image, 2, 2)

# Initialisations dont matter tbh
original_idx_x = 0
original_idx_y = 1

chessPieces = [rook, rook2, rook3]
dragged_piece = rook
dragging_piece = False

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                index = getIndexFromPos(mouse_x, mouse_y)
                for c in chessPieces:
                    if index[0] == c.idxX and index[1] == c.idxY:
                        print("piece selected")
                        dragged_piece = c
                        dragging_piece = True
                        break
                if dragging_piece:
                    dragged_piece.posX = mouse_x - w_per_sq/2
                    dragged_piece.posY = mouse_y - w_per_sq/2
                    offset_x = dragged_piece.posX - mouse_x
                    offset_y = dragged_piece.posY - mouse_y
                    original_idx_x, original_idx_y = getIndexFromPos(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                if dragging_piece:
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    if(idx[0] == -1):
                        pos = getPosFromIndex(original_idx_x, original_idx_y)
                    dragging_piece = False
                    dragged_piece.posX = pos[0]
                    dragged_piece.idxX = idx[0]
                    dragged_piece.posY = pos[1]
                    dragged_piece.idxY = idx[1]
                    checkIfPieceAlreadyThere(pos[0], pos[1], dragged_piece)
        elif event.type == pygame.MOUSEMOTION:
            if dragging_piece:
                mouse_x, mouse_y = event.pos
                dragged_piece.posX = mouse_x + offset_x
                dragged_piece.posY = mouse_y + offset_y

    win.fill(BLUE)
    draw()
    pygame.display.update()

pygame.quit()
