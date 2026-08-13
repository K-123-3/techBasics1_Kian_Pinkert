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
    city_bg = CityCamera("map/city.tmx", SCREEN_WIDTH, SCREEN_HEIGHT)
    road_bg = ScrollingBackground("map/road.tmx", SCREEN_WIDTH, SCREEN_HEIGHT, speed=1)

    bin_positions = [
        (200, 300),
        (400,200),
        (400,400),
    ]
    bins = [Bins(pos_x=x, pos_y=y) for x, y in bin_positions]


    bike_positions = [
        (800, random.randint(-300, 100)),
        (900, random.randint(-100, 50)),
        (600, random.randint(-400, -200)),
    ]
    bikes = [Bikes(pos_x=x, pos_y=y) for x, y in bike_positions]


    return racoon, bikes, city_bg, road_bg, bins
racoon, bikes, city_bg, road_bg, bins = new_game()

'''score = 0
scene = "city"'''

#to check road:
score = 3
scene = "road"

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

        for bin in bins:
            bin.update()
            if bin.check_interaction(racoon):
                score = min(score + 1, 3)
            bin.draw(screen, city_bg.to_screen_pos(bin.pos_x, bin.pos_y))

        screen_x, screen_y = city_bg.player_screen_pos(racoon)
        racoon.rect.center = (screen_x, screen_y)
        racoon.draw(screen)

        draw_score(screen, score)
        pygame.display.flip()

        if racoon.pos_x >= city_bg.world_width:
            scene = "road"
            road_bg.update()
            racoon.wall_collision(dx, dy, road_bg.collision_rects)
            racoon.update()
            racoon.sync_screen_position(road_bg.scroll_x)
        continue

    road_bg.update()
    racoon.wall_collision(dx, dy, road_bg.collision_rects)
    racoon.update()
    racoon.sync_screen_position(road_bg.scroll_x)

    if racoon.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
        racoon.pos_x, racoon.pos_y = 100, 250

    for bike in bikes:
        bike.animate(direction_x=random.randint(-13, -3), direction_y=0)
        bike.update()

        if check_collision(racoon, bike):
            score -= 1

    if score <= 0:
        racoon, bikes, city_bg, road_bg, bins = new_game()
        score = 3
        scene = "city"
        game_over_screen(screen)
        continue

    if road_bg.finished and scene == "road":
        scene = "city"

    road_bg.draw(screen)
    racoon.draw(screen)
    for bike in bikes:
        bike.draw(screen)
    draw_score(screen, score)
    pygame.display.flip()

pygame.quit()