import pygame

# Please note: I am using a python interpreter with a conda enrivonement...

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chess Game")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

x, y, w, h = 50, 50, 20, 20

run = True
rectangle_draging = False

rectangle = pygame.rect.Rect(x, y, w, h)
rectangle2 = pygame.rect.Rect(x, y, w, h)
rectangle3 = pygame.rect.Rect(x, y, w, h)

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

    win.fill((0, 0, 0))
    pygame.draw.rect(win, RED, rectangle)
    pygame.draw.rect(win, GREEN, rectangle2)
    pygame.draw.rect(win, BLUE, rectangle3)
    pygame.display.update()

pygame.quit()
