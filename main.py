import pygame
from ChessLogic import getAllLegalMoves
from ChessLogic import opponentLastMovePawn2Spaces
from ChessLogic import opponentLastMovePawnLocation
from ChessLogic import ChessPiece
from ChessLogic import ChessPieceTypes
from ChessLogic import CastlingLogic

# TODO: complete the readme

# TODO: finish off castling mechanics by changing bools in CastlingLogic bool when rooks move, etc..
# TODO: have some sort of take back mechanism
# TODO: dragging shows legal moves
# TODO: fix clicking to move piece - needs minor adjustment
# TODO: add opacity to legal move rectangles
# TODO: promoting option, not only queen

pygame.init()
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Chess Game")
#Chess Board bound constants
# cb_bx2 = 8*w_per_sq + cb_bx1
cb_bx1, cb_bx2, cb_by1, cb_by2 = 20, 660, 20, 660
w_per_sq = 80
list_sq_end = [cb_bx1 + w_per_sq , cb_bx1 + w_per_sq * 2, 
                cb_bx1 + w_per_sq * 3, cb_bx1 + w_per_sq * 4,
                cb_bx1 + w_per_sq * 5, cb_bx1 + w_per_sq * 6,
                cb_bx1 + w_per_sq * 7, cb_bx1 + w_per_sq * 8]

BLACK = (20, 20, 20)
WHITE = (230, 230, 230)
BROWN = (165, 42, 42)
GREEN = (40, 220, 40)
YELLOW = (180, 180, 30)

# squares and lines - however, lines look a little ugly so maybe dont draw them anymore
def drawBoard():
    # border
    pygame.draw.line(win, BLACK, (cb_bx1, cb_by1), (cb_bx2, cb_by1))
    pygame.draw.line(win, BLACK, (cb_bx1, cb_by1), (cb_bx1, cb_by2))
    pygame.draw.line(win, BLACK, (cb_bx2, cb_by1), (cb_bx2, cb_by2))
    pygame.draw.line(win, BLACK, (cb_bx1, cb_by2), (cb_bx2, cb_by2))

    # colour every other square black or white
    for x in range(0,8):
        for y in range(0,8):
            if (x+y)%2 == 1:
                pygame.draw.rect(win, BROWN, (x * w_per_sq + cb_bx1, y * w_per_sq + cb_by1, w_per_sq, w_per_sq))

def draw():
    drawBoard()

    if isPieceClicked:
        colourSelectedIndex(dragged_piece.idxX, dragged_piece.idxY, GREEN)
        for idx in legalMovesList:
            colourSelectedIndex(idx[0], idx[1], YELLOW)

    # checking to draw the white pieces after so they appear on top if whites move
    if not isWhitesMove:
        for c in whiteChessPieces:
            win.blit(c.image, (c.posX, c.posY))
    for c in blackChessPieces:
        win.blit(c.image, (c.posX, c.posY))
    if isWhitesMove:
        for c in whiteChessPieces:
            win.blit(c.image, (c.posX, c.posY))

def colourSelectedIndex(x, y, color):
    pygame.draw.rect(win, color, (x * w_per_sq + cb_bx1, y * w_per_sq + cb_by1, w_per_sq, w_per_sq))

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

def checkIfYourPieceAlreadyThere(posX, posY, piece, whiteTurn):
    yourPieces = whiteChessPieces if whiteTurn else blackChessPieces

    for i in range(len(yourPieces)):
        if posX == yourPieces[i].posX and posY == yourPieces[i].posY and piece is not yourPieces[i]:
            return True
    return False 

# check if this square has an opponent piece, and remove piece if so
def checkTakeOpponentPiece(idxX, idxY, piece, whiteTurn):
    opponentPieces = blackChessPieces if whiteTurn else whiteChessPieces

    for oppoPiece in opponentPieces:
        if idxX == oppoPiece.idxX and idxY == oppoPiece.idxY:
            opponentPieces.remove(oppoPiece)
            break

# handle if en passant is played and therefore removes an opponent piece not on the same square
def checkTakeWithEnPassant(idxX, idxY, whiteTurn, opponentLastMovePawnLocation):
    opponentPieces = blackChessPieces if whiteTurn else whiteChessPieces
    change = 1 if whiteTurn else -1
    for oppoPiece in opponentPieces:
        if opponentLastMovePawnLocation[0] == oppoPiece.idxX and opponentLastMovePawnLocation[1] == oppoPiece.idxY:
            if idxX == opponentLastMovePawnLocation[0] and idxY+change == opponentLastMovePawnLocation[1]:
                opponentPieces.remove(oppoPiece)
                break

def handlePawnPromotion(piece):
    # TODO: Pawn only promotes to a queen
    piece.pType = ChessPieceTypes.QUEEN
    # note: I was using whites turn for the check, but because I'm changing the turn before this it was creating wrong coloured piece
    piece.image = w_queen_image if piece.idxY == 0 else b_queen_image

def confirmValidity(xFrom, yFrom, xTo, yTo):
    for pos in legalMovesList:
        if(xTo, yTo) == pos:
            return True
    return False

def checkDifferentSquare(xFrom, yFrom, xTo, yTo):
    if xFrom == xTo and yFrom == yTo:
        return True
    return False

def checkCastled(idx, o_idx, whiteTurn):
    if whiteTurn:
        castlingLogic.hasWhiteMovedKing = True
    else:
        castlingLogic.hasBlackMovedKing = True

    yourPieces = whiteChessPieces if whiteTurn else blackChessPieces
    if abs(idx[0] - o_idx[0]) == 2:
        if idx[0] == 2 and idx[1] == 0:
            for p in yourPieces:
                if p.idxX == 0 and p.idxY == 0:
                    p.setNewPosition((3, 0), getPosFromIndex(3, 0))
                    castlingLogic.hasBlackCastled = True
                    break
        elif idx[0] == 2 and idx[1] == 7:
            for p in yourPieces:
                if p.idxX == 0 and p.idxY == 7:
                    castlingLogic.hasWhiteCastled = True
                    p.setNewPosition((3, 7), getPosFromIndex(3, 7))
                    break
        elif idx[0] == 6 and idx[1] == 0:
            for p in yourPieces:
                if p.idxX == 7 and p.idxY == 0:
                    castlingLogic.hasBlackCastled = True
                    p.setNewPosition((5, 0), getPosFromIndex(5, 0))
                    break
        elif idx[0] == 6 and idx[1] == 7:
            for p in yourPieces:
                if p.idxX == 7 and p.idxY == 7:
                    castlingLogic.hasWhiteCastled = True
                    p.setNewPosition((5, 7), getPosFromIndex(5, 7))
                    break

def movedRook(x, y):
    if x == 0 and y == 0:
        castlingLogic.hasBlackMoved_A_Rook = True
    elif x == 7 and y == 0:
        castlingLogic.hasBlackMoved_H_Rook = True
    elif x == 0 and y == 7:
        castlingLogic.hasWhiteMoved_A_Rook = True
    elif x == 7 and y == 7:
        castlingLogic.hasWhiteMoved_H_Rook = True

w_rook_image = pygame.image.load(".\images\white_rook.png")
w_rook_image = pygame.transform.scale(w_rook_image, (w_per_sq,w_per_sq))
w_knight_image = pygame.image.load(".\images\white_knight.png")
w_knight_image = pygame.transform.scale(w_knight_image, (w_per_sq,w_per_sq))
w_bishop_image = pygame.image.load(".\images\white_bishop.png")
w_bishop_image = pygame.transform.scale(w_bishop_image, (w_per_sq,w_per_sq))
w_king_image = pygame.image.load(".\images\white_king.png")
w_king_image = pygame.transform.scale(w_king_image, (w_per_sq,w_per_sq))
w_queen_image = pygame.image.load(".\images\white_queen.png")
w_queen_image = pygame.transform.scale(w_queen_image, (w_per_sq,w_per_sq))
w_pawn_image = pygame.image.load(".\images\white_pawn.png")
w_pawn_image = pygame.transform.scale(w_pawn_image, (w_per_sq,w_per_sq))
whiteChessPieces = [ChessPiece(w_rook_image, (7,7), getPosFromIndex(7,7), ChessPieceTypes.ROOK), ChessPiece(w_rook_image, (0,7), getPosFromIndex(0,7), ChessPieceTypes.ROOK), 
        ChessPiece(w_knight_image, (1,7), getPosFromIndex(1,7), ChessPieceTypes.KNIGHT), ChessPiece(w_knight_image, (6,7), getPosFromIndex(6,7), ChessPieceTypes.KNIGHT), 
        ChessPiece(w_bishop_image, (5,7), getPosFromIndex(5,7), ChessPieceTypes.BISHOP), ChessPiece(w_bishop_image, (2,7), getPosFromIndex(2,7), ChessPieceTypes.BISHOP), 
        ChessPiece(w_king_image, (4,7), getPosFromIndex(4,7), ChessPieceTypes.KING), ChessPiece(w_queen_image, (3,7), getPosFromIndex(3,7), ChessPieceTypes.QUEEN),
        ChessPiece(w_pawn_image, (0,6), getPosFromIndex(0,6), ChessPieceTypes.PAWN), ChessPiece(w_pawn_image, (1,6), getPosFromIndex(1,6), ChessPieceTypes.PAWN), 
        ChessPiece(w_pawn_image, (2,6), getPosFromIndex(2,6), ChessPieceTypes.PAWN), ChessPiece(w_pawn_image, (3,6), getPosFromIndex(3,6), ChessPieceTypes.PAWN), 
        ChessPiece(w_pawn_image, (4,6), getPosFromIndex(4,6), ChessPieceTypes.PAWN), ChessPiece(w_pawn_image, (5,6), getPosFromIndex(5,6), ChessPieceTypes.PAWN), 
        ChessPiece(w_pawn_image, (6,6), getPosFromIndex(6,6), ChessPieceTypes.PAWN), ChessPiece(w_pawn_image, (7,6), getPosFromIndex(7,6), ChessPieceTypes.PAWN)]

b_rook_image = pygame.image.load(".\images\\black_rook.png")
b_rook_image = pygame.transform.scale(b_rook_image, (w_per_sq,w_per_sq))
b_knight_image = pygame.image.load(".\images\\black_knight.png")
b_knight_image = pygame.transform.scale(b_knight_image, (w_per_sq,w_per_sq))
b_bishop_image = pygame.image.load(".\images\\black_bishop.png")
b_bishop_image = pygame.transform.scale(b_bishop_image, (w_per_sq,w_per_sq))
b_king_image = pygame.image.load(".\images\\black_king.png")
b_king_image = pygame.transform.scale(b_king_image, (w_per_sq,w_per_sq))
b_queen_image = pygame.image.load(".\images\\black_queen.png")
b_queen_image = pygame.transform.scale(b_queen_image, (w_per_sq,w_per_sq))
b_pawn_image = pygame.image.load(".\images\\black_pawn.png")
b_pawn_image = pygame.transform.scale(b_pawn_image, (w_per_sq,w_per_sq))
blackChessPieces = [ChessPiece(b_rook_image, (7,0), getPosFromIndex(7,0), ChessPieceTypes.ROOK), ChessPiece(b_rook_image, (0,0), getPosFromIndex(0,0), ChessPieceTypes.ROOK), 
        ChessPiece(b_knight_image, (1,0), getPosFromIndex(1,0), ChessPieceTypes.KNIGHT), ChessPiece(b_knight_image, (6,0), getPosFromIndex(6,0), ChessPieceTypes.KNIGHT), 
        ChessPiece(b_bishop_image, (5,0), getPosFromIndex(5,0), ChessPieceTypes.BISHOP), ChessPiece(b_bishop_image, (2,0), getPosFromIndex(2,0), ChessPieceTypes.BISHOP), 
        ChessPiece(b_king_image, (4,0), getPosFromIndex(4,0), ChessPieceTypes.KING), ChessPiece(b_queen_image, (3,0), getPosFromIndex(3,0), ChessPieceTypes.QUEEN),
        ChessPiece(b_pawn_image, (0,1), getPosFromIndex(0,1), ChessPieceTypes.PAWN), ChessPiece(b_pawn_image, (1,1), getPosFromIndex(1,1), ChessPieceTypes.PAWN),
        ChessPiece(b_pawn_image, (2,1), getPosFromIndex(2,1), ChessPieceTypes.PAWN), ChessPiece(b_pawn_image, (3,1), getPosFromIndex(3,1), ChessPieceTypes.PAWN), 
        ChessPiece(b_pawn_image, (4,1), getPosFromIndex(4,1), ChessPieceTypes.PAWN), ChessPiece(b_pawn_image, (5,1), getPosFromIndex(5,1), ChessPieceTypes.PAWN), 
        ChessPiece(b_pawn_image, (6,1), getPosFromIndex(6,1), ChessPieceTypes.PAWN), ChessPiece(b_pawn_image, (7,1), getPosFromIndex(7,1), ChessPieceTypes.PAWN)]

# Initialisations dont matter tbh
original_idx_x = 0
original_idx_y = 1
dragged_piece = whiteChessPieces[0]
is_dragging_piece = False

castlingLogic = CastlingLogic()

run = True
isWhitesMove = True
isPieceClicked = False # Specifically Clicked, and not held and dragged

legalMovesList = []

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if isPieceClicked:
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    sameSquare = checkDifferentSquare(original_idx_x, original_idx_y, idx[0], idx[1])
                    if sameSquare:
                        isPieceClicked = False
                    else:
                        validMove = not checkIfYourPieceAlreadyThere(pos[0], pos[1], dragged_piece, isWhitesMove) and confirmValidity(original_idx_x, original_idx_y, idx[0], idx[1])
                        if idx[0] == -1 or not validMove:
                            pos = getPosFromIndex(original_idx_x, original_idx_y)
                            idx = (original_idx_x, original_idx_y)
                            validMove = False
                        if validMove:

                            # TODO: Tidy up following repeated 7 lines
                            if dragged_piece.pType == ChessPieceTypes.PAWN and opponentLastMovePawn2Spaces == True:
                                checkTakeWithEnPassant(idx[0], idx[1], isWhitesMove, opponentLastMovePawnLocation)
                            elif dragged_piece.pType == ChessPieceTypes.KING:
                                checkCastled(idx, (original_idx_x, original_idx_y), isWhitesMove)
                            elif dragged_piece.pType == ChessPieceTypes.ROOK:
                                movedRook(original_idx_x, original_idx_y)
                            checkTakeOpponentPiece(idx[0], idx[1], dragged_piece, isWhitesMove)

                            # TODO: Tidy up following repeated 6 lines
                            isWhitesMove = not isWhitesMove
                            opponentLastMovePawn2Spaces = False
                            if dragged_piece.pType == ChessPieceTypes.PAWN:
                                if original_idx_x == idx[0] and abs(original_idx_y - idx[1]) == 2:
                                    opponentLastMovePawn2Spaces = True
                                    opponentLastMovePawnLocation = idx

                            isPieceClicked = False

                    # TODO: Tidy up repeated 3 lines                            
                    dragged_piece.setNewPosition(idx, pos)
                    if dragged_piece.pType == ChessPieceTypes.PAWN and (idx[1] == 0 or idx[1] == 7):
                        handlePawnPromotion(dragged_piece)

                else:
                    index = getIndexFromPos(mouse_x, mouse_y)
                    chessPieces = whiteChessPieces if isWhitesMove else blackChessPieces
                    for c in chessPieces:
                        if index[0] == c.idxX and index[1] == c.idxY:
                            dragged_piece = c
                            # Test here to see if works as inteded
                            # print("inputting opponentLastMovePawnLocation: ", opponentLastMovePawnLocation, " true/false: ", opponentLastMovePawn2Spaces)
                            legalMovesList = getAllLegalMoves(dragged_piece.idxX, dragged_piece.idxY, 
                                    whiteChessPieces if isWhitesMove else blackChessPieces, 
                                    blackChessPieces if isWhitesMove else whiteChessPieces, 
                                    dragged_piece, isWhitesMove,
                                    opponentLastMovePawn2Spaces, opponentLastMovePawnLocation,
                                    castlingLogic)
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
                    is_dragging_piece = False
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    sameSquare = checkDifferentSquare(original_idx_x, original_idx_y, idx[0], idx[1])
                    if sameSquare:
                        isPieceClicked = True
                    else:
                        validMove = not checkIfYourPieceAlreadyThere(pos[0], pos[1], dragged_piece, isWhitesMove) and confirmValidity(original_idx_x, original_idx_y, idx[0], idx[1])
                        if idx[0] == -1 or not validMove:
                            pos = getPosFromIndex(original_idx_x, original_idx_y)
                            idx = (original_idx_x, original_idx_y)
                            validMove = False
                        if validMove:
                            # TODO: Tidy up following repeated 7 lines
                            if dragged_piece.pType == ChessPieceTypes.PAWN and opponentLastMovePawn2Spaces == True:
                                checkTakeWithEnPassant(idx[0], idx[1], isWhitesMove, opponentLastMovePawnLocation)
                            elif dragged_piece.pType == ChessPieceTypes.KING:
                                checkCastled(idx, (original_idx_x, original_idx_y), isWhitesMove)
                            elif dragged_piece.pType == ChessPieceTypes.ROOK:
                                movedRook(original_idx_x, original_idx_y)
                            checkTakeOpponentPiece(idx[0], idx[1], dragged_piece, isWhitesMove)

                            # TODO: Tidy up following repeated 6 lines
                            isWhitesMove = not isWhitesMove
                            opponentLastMovePawn2Spaces = False
                            if dragged_piece.pType == ChessPieceTypes.PAWN:
                                if original_idx_x == idx[0] and abs(original_idx_y - idx[1]) == 2:
                                    opponentLastMovePawn2Spaces = True
                                    opponentLastMovePawnLocation = idx

                    # note i am setting set position or original index above if not a valid move, this doesnt always move it to a new square
                    # TODO: Tidy up repeated 3 lines
                    dragged_piece.setNewPosition(idx, pos)
                    if dragged_piece.pType == ChessPieceTypes.PAWN and (idx[1] == 0 or idx[1] == 7):
                        handlePawnPromotion(dragged_piece)

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging_piece:
                # there should be no logic here, only visual moving of piece
                mouse_x, mouse_y = event.pos
                dragged_piece.posX = mouse_x + offset_x
                dragged_piece.posY = mouse_y + offset_y

    win.fill(WHITE)
    draw()
    pygame.display.update()

pygame.quit()
