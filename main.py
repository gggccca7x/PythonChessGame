import pygame

# Please note: I am using a python interpreter with a conda enrivonement...

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
list_sq_start = [cb_bx1, cb_bx1 + w_per_sq, 
                cb_bx1 + w_per_sq * 2, cb_bx1 + w_per_sq * 3,
                cb_bx1 + w_per_sq * 4, cb_bx1 + w_per_sq * 7,
                cb_bx1 + w_per_sq * 6, cb_bx1 + w_per_sq * 8]
# list_sq_start = [100, 200, 300, 400, 500, 600, 700, 800]

w, h = 100, 100

run = True
rectangle_draging = False

def draw():
    pygame.draw.rect(win, RED, rectangle)
    pygame.draw.rect(win, GREEN, rectangle2)
    pygame.draw.rect(win, BLUE, rectangle3)
    pygame.draw.line(win, WHITE, (cb_bx1, cb_by1), (cb_bx1, cb_by2))
    pygame.draw.line(win, WHITE, (cb_bx2, cb_by1), (cb_bx2, cb_by2))
    pygame.draw.line(win, WHITE, (cb_bx1, cb_by1), (cb_bx2, cb_by1))
    pygame.draw.line(win, WHITE, (cb_bx1, cb_by2), (cb_bx2, cb_by2))

#input index (0-7) as chessboard is 8x8
def getPosFromIndex(x, y):
    return (cb_bx1 + x * w_per_sq, cb_by1 + y * w_per_sq)

def getIndexFromPos(x, y):
    posX, posY = -1, -1
    for i in range(len(list_sq_start)):
        print("x is : " + str(x))
        print("list is : " + str(list_sq_start[i]))
        if x <= list_sq_start[i]:
            posX = i-1
            print("set posX to " + str(posX))
            break
    for i in range(len(list_sq_start)):
        if y <= list_sq_start[i]:
            posY = i-1
            break
    if posX == -1 or posY == -1:
        posX, posY = -1, -1
    return (posX, posY)

pos = getPosFromIndex(0,0)
rectangle = pygame.rect.Rect(pos[0], pos[1], w, h)
pos = getPosFromIndex(0,1)
rectangle2 = pygame.rect.Rect(pos[0], pos[1], w, h)
pos = getPosFromIndex(0,6)
rectangle3 = pygame.rect.Rect(pos[0], pos[1], w, h)
dragged_rect = rectangle

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    dragged_rect = rectangle
                elif rectangle2.collidepoint(event.pos):
                    rectangle_draging = True
                    dragged_rect = rectangle2
                elif rectangle3.collidepoint(event.pos):
                    rectangle_draging = True
                    dragged_rect = rectangle3
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    dragged_rect.x = mouse_x - rectangle.w/2
                    dragged_rect.y = mouse_y - rectangle.h/2
                    offset_x = dragged_rect.x - mouse_x
                    offset_y = dragged_rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                if rectangle_draging:
                    idx = getIndexFromPos(mouse_x, mouse_y)
                    pos = getPosFromIndex(idx[0], idx[1])
                    #TODO: if pos is -1 then set to original square, which currently isnt tracked
                    dragged_rect.x = pos[0]
                    dragged_rect.y = pos[1]
                    rectangle_draging = False
        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                dragged_rect.x = mouse_x + offset_x
                dragged_rect.y = mouse_y + offset_y

    win.fill(BLACK)
    draw()
    pygame.display.update()

pygame.quit()
