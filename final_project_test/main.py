from player import *
# from requirements.txt  import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')

bike = Bikes(pos_x=800, pos_y=-random.randint(0, 200))
racoon = Racoon(100, 100)
bg = pygame.image.load("pictures/img.png").convert_alpha()

flag = True
while flag:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] #keys = walking
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    racoon.animate(direction_x=dx, direction_y=dy)
    racoon.update()

    bike.animate(direction_x=-5, direction_y=0)
    bike.update()
    check_collision(racoon, bike)

    screen.blit(bg, (0, 0))
    racoon.draw(screen)
    bike.draw(screen)
    pygame.display.flip()

pygame.quit()