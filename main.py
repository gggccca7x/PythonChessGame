import pygame

# Please note: I am using a python interpreter with a conda enrivonement...

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chess Game")

RED = (255, 0, 0)

x = 50
y = 50
w = 20
h = 20
vel = 5

run = True
rectangle_draging = False
rectangle = pygame.rect.Rect(x, y, w, h)

while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    rectangle.x = mouse_x - rectangle.w/2
                    rectangle.y = mouse_y - rectangle.h/2
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False
        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    win.fill((0, 0, 0))
    pygame.draw.rect(win, RED, rectangle)
    pygame.display.update()

pygame.quit()
