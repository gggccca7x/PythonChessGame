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
def getPos(x, y):
    return (cb_bx1 + x * w_per_sq, cb_by1 + y * w_per_sq)

pos = getPos(0,0)
rectangle = pygame.rect.Rect(pos[0], pos[1], w, h)
pos = getPos(0,1)
rectangle2 = pygame.rect.Rect(pos[0], pos[1], w, h)
pos = getPos(0,6)
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
