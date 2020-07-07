import pygame

# Please note: I am using a python interpreter with a conda enrivonement...

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Chess Game")

x = 50
y = 50
w = 20
h = 20
vel = 5

run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, w, h))
    pygame.display.update()


pygame.quit()
