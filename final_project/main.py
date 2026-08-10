from start import *
# from requirements.txt  import *
from map_helper import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')


def new_game():
    racoon = Racoon(100, 100)
    bike = Bikes(pos_x=800, pos_y=-random.randint(0, 200))
    bike2 = Bikes(pos_x=800, pos_y=-random.randint(200, 300))
    bg = ScrollingBackground("map/road.tmx", SCREEN_WIDTH, SCREEN_HEIGHT, speed=1)
    return racoon, bike, bike2, bg


racoon, bike, bike2, bg = new_game()

start_screen(screen)
flag = True
while flag:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] #walking
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    racoon.animate(direction_x=dx, direction_y=dy)
    racoon.update()

    bg.update()
    racoon.sync_screen_position(bg.scroll_x)

    if racoon.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
        #placeholdee!!!!!
        racoon, bike, bike2, bg = new_game()
        start_screen(screen)
        continue

    bike.animate(direction_x=-5, direction_y=0)
    bike2.animate(direction_x=-5, direction_y=0)
    bike.update()
    bike2.update()
    check_collision(racoon, bike)
    check_collision(racoon, bike2)

    bg.draw(screen)
    racoon.draw(screen)
    bike.draw(screen)
    bike2.draw(screen)
    pygame.display.flip()

pygame.quit()