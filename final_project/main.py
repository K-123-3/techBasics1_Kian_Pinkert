from screens import *
# from requirements.txt  import *
from map_helper import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')

#----score
ICON_SIZE = 30
ICON_MARGIN = 4

def load_icon(path, size):
    img = pygame.image.load(path).convert_alpha()
    bounds = img.get_bounding_rect()
    cropped = img.subsurface(bounds).copy() #remove transparent pixles
    return pygame.transform.scale(cropped, (size, size))

face_alive = load_icon("pictures/racoon/face.png", ICON_SIZE)
face_dead = load_icon("pictures/racoon/score.png", ICON_SIZE)


def draw_score(screen, score, max_lives=3):
    for i in range(max_lives):
        x = ICON_MARGIN + i * (ICON_SIZE + ICON_MARGIN)
        y = ICON_MARGIN
        icon = face_alive if i < score else face_dead # show dead face when score goes down
        screen.blit(icon, (x, y))


def new_game():
    racoon = Racoon(200, 125)
    trash = Bins(pos_x=100, pos_y=250)
    bike = Bikes(pos_x=800, pos_y=random.randint(-300, 100))
    bike2 = Bikes(pos_x=800, pos_y=random.randint(-300, 100))
    bike3 = Bikes(pos_x=800, pos_y=random.randint(-300,  100))
    city_bg = CityCamera("map/city.tmx", SCREEN_WIDTH, SCREEN_HEIGHT)
    road_bg = ScrollingBackground("map/road.tmx", SCREEN_WIDTH, SCREEN_HEIGHT, speed=1)
    return racoon, trash, bike, bike2, bike3, city_bg, road_bg


racoon, trash, bike, bike2, bike3, city_bg, road_bg = new_game()
score = 3
scene = "road"  #change to road if you want to check road only
start_screen(screen)
flag = True
while flag:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if scene == "city":
        racoon.wall_collision(dx, dy, city_bg.collision_rects)
        racoon.update()
        city_bg.draw_camera(screen, racoon)

        screen_x, screen_y = city_bg.player_screen_pos(racoon)
        racoon.rect.center = (screen_x, screen_y)  # temporary: for drawing only
        racoon.draw(screen)
        trash.draw(screen)

        draw_score(screen, score)
        pygame.display.flip()

        if racoon.pos_x >= city_bg.world_width:
            scene = "road"
            racoon.pos_x, racoon.pos_y = 100, 250
            racoon.rect.center = (racoon.pos_x, racoon.pos_y)
        continue

    road_bg.update()
    racoon.animate(direction_x=dx, direction_y=dy)
    racoon.update()
    racoon.sync_screen_position(road_bg.scroll_x)

    if racoon.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
        score -= 1

    bike.animate(direction_x=-5, direction_y=0)
    bike.update()
    bike2.animate(direction_x=-5, direction_y=0)
    bike2.update()
    bike3.animate(direction_x=-5, direction_y=0)
    bike3.update()

    if check_collision(racoon, bike):
        score -= 1
    if check_collision(racoon, bike2):
        score -= 1
    if check_collision(racoon, bike3):
        score -= 1

    if score <= 0:
        racoon, trash, bike, bike2, bike3, city_bg, road_bg = new_game()
        score = 3
        scene = "city"
        game_over_screen(screen)
        continue

    road_bg.draw(screen)
    racoon.draw(screen)
    bike.draw(screen)
    bike2.draw(screen)
    bike3.draw(screen)
    draw_score(screen, score)
    pygame.display.flip()

pygame.quit()