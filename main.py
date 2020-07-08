import pygame

# Please note: I am using a python interpreter with a conda environement...

# TODO: bring to front the selected piece (move to bottom of the list)

class ChessPiece(object):
    def __init__(self, image, idxX, idxY):
        self.image = image
        pos = getPosFromIndex(idxX, idxY)
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
rectangle_draging = False

def drawLines():
    for x in range(0,9):
        pygame.draw.line(win, WHITE, (cb_bx1, cb_by1 + w_per_sq * x), (cb_bx2, cb_by1 + w_per_sq * x))
        pygame.draw.line(win, WHITE, (cb_bx1 + w_per_sq * x, cb_by1), (cb_bx1 + w_per_sq * x, cb_by2))

def draw():
    for i in range(len(myReactangles)):
        pygame.draw.rect(win, myColours[i], myReactangles[i])

    win.blit(rook.image, (rook.posX, rook.posY))
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

def checkIfPieceAlreadyThere(posX, posY, rect):
    for i in range(len(myReactangles)):
        if posX == myReactangles[i].x and posY == myReactangles[i].y and rect is not myReactangles[i]:
            myReactangles.remove(myReactangles[i])
            myColours.remove(myColours[i])
            break

pos = getPosFromIndex(0,0)
rectangle = pygame.rect.Rect(pos[0], pos[1], w_per_sq, w_per_sq)
pos = getPosFromIndex(0,1)
rectangle2 = pygame.rect.Rect(pos[0], pos[1], w_per_sq, w_per_sq)
pos = getPosFromIndex(0,6)
rectangle3 = pygame.rect.Rect(pos[0], pos[1], w_per_sq, w_per_sq)

rook_image = pygame.image.load(".\images\white_rook.png")
rook_image = pygame.transform.scale(rook_image, (100,100))
rook = ChessPiece(rook_image, 0, 0)

# Initialisations dont matter tbh
dragged_rect = rectangle
original_idx_x = 0
original_idx_y = 1

myReactangles = [rectangle, rectangle2, rectangle3]
myColours = [RED, BLUE, GREEN]

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   
                for r in myReactangles:
                    if r.collidepoint(event.pos):
                        rectangle_draging = True
                        dragged_rect = r
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    dragged_rect.x = mouse_x - rectangle.w/2
                    dragged_rect.y = mouse_y - rectangle.h/2
                    offset_x = dragged_rect.x - mouse_x
                    offset_y = dragged_rect.y - mouse_y
                    original_idx_x, original_idx_y = getIndexFromPos(mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                if rectangle_draging:
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    if(idx[0] == -1):
                        pos = getPosFromIndex(original_idx_x, original_idx_y)
                    rectangle_draging = False
                    dragged_rect.x = pos[0]
                    dragged_rect.y = pos[1]
                    checkIfPieceAlreadyThere(pos[0], pos[1], dragged_rect)
        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                dragged_rect.x = mouse_x + offset_x
                dragged_rect.y = mouse_y + offset_y

    win.fill(BLACK)
    draw()
    pygame.display.update()

pygame.quit()
