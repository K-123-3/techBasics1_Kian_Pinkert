from screens import *
# from requirements.txt import *
from map_helper import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')

# constants
ICON_SIZE = 30
ICON_MARGIN = 4
APPLE_PERCENTAGE = 0.2
BIN_POSITIONS = [
        (1100, 125),
        (200,400),
        (1000,300),
    ]
BIKE_POSITIONS = [
    (800, random.randint(-300, -100)),
    (900, random.randint(-300, -100)),
    (600, random.randint(-300, -200)),
    (1000, random.randint(-300, -150)),
]

SCENES = [
    {"path": "media/map/road.tmx", "bg_speed": 1, "racoon_speed": 3, "allow_car": False},
    {"path": "media/map/road2.tmx", "bg_speed": 2, "racoon_speed": 4, "allow_car": True},
    {"path": "media/map/road2.tmx", "bg_speed": 3, "racoon_speed": 5, "allow_car": True},
]

DEBUG_SCENES = 0 #set to scene number to debug - 0 = road, 1 = road2, 2 = road3
#audio
hit_sfx = pygame.mixer.Sound('media/music_sfx/hit_sfx.mp3')
apple_sfx = pygame.mixer.Sound('media/music_sfx/apple_sfx.mp3')
trash_sfx = pygame.mixer.Sound('media/music_sfx/trash_sfx.mp3')
#----score
def load_icon(path, size):
    img = pygame.image.load(path).convert_alpha()
    bounds = img.get_bounding_rect()
    cropped = img.subsurface(bounds).copy() #remove transparent pixles
    return pygame.transform.scale(cropped, (size, size))

face_alive = load_icon("media/pictures/racoon/face.png", ICON_SIZE)
face_dead = load_icon("media/pictures/racoon/score.png", ICON_SIZE)


def draw_score(screen, score, max_lives=3):
    for i in range(max_lives):
        x = ICON_MARGIN + i * (ICON_SIZE + ICON_MARGIN)
        y = ICON_MARGIN
        icon = face_alive if i < score else face_dead # show dead face when score goes down
        screen.blit(icon, (x, y))

#game setup
def new_game():
    racoon = Racoon(200, 125)
    city_bg = CityCamera("media/map/city.tmx", SCREEN_WIDTH, SCREEN_HEIGHT)
    road_stages = [
        ScrollingBackground(cfg["path"], SCREEN_WIDTH, SCREEN_HEIGHT, speed=cfg["bg_speed"])
        for cfg in SCENES
    ]

    bins = [Bins(pos_x=x, pos_y=y) for x, y in BIN_POSITIONS]
    bikes = [Bikes(pos_x=x, pos_y=y) for x, y in BIKE_POSITIONS]

    return racoon, bikes, city_bg, road_stages, bins

def apple_spawn(apple, score, scroll_x, screen_width=SCREEN_WIDTH):
    if apple is not None or score >= 3:
        return apple
    if random.random() < APPLE_PERCENTAGE:
        spawn_x = scroll_x + screen_width + random.randint(100, 400)
        spawn_y = random.randint(100, 400)
        return Apple(spawn_x, spawn_y)
    return apple

def enter_road(racoon, road_stages, stage_index):
    racoon.pos_x, racoon.pos_y = 100, 250
    stage_bg = road_stages[stage_index]
    stage_bg.scroll_x = 0
    stage_bg.finished = stage_bg.max_scroll == 0
    racoon.sync_screen_position(stage_bg.scroll_x)


#running game
racoon, bikes, city_bg, road_stages, bins = new_game()
apple = None
score = 3

if DEBUG_SCENES is not None:
    scene = "road"
    road_index = DEBUG_SCENES
    enter_road(racoon, road_stages, road_index)
else:
    scene = "city"
    road_index = 0

start_screen(screen)
flag = True
while flag:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
#control setup
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

#scene setup

    if scene == "city":
        racoon.wall_collision(dx, dy, city_bg.collision_rects)
        racoon.update()
        city_bg.draw_camera(screen, racoon)

        for bin in bins:
            bin.update()
            if bin.check_interaction(racoon):
                trash_sfx.play()
                score = min(score + 1, 3)
            bin.draw(screen, city_bg.to_screen_pos(bin.pos_x, bin.pos_y))

        screen_x, screen_y = city_bg.player_screen_pos(racoon)
        racoon.rect.center = (screen_x, screen_y)
        racoon.draw(screen)

        draw_score(screen, score)
        pygame.display.flip()

        if racoon.pos_x >= city_bg.world_width:
            scene = "road"
            road_index = 0
            enter_road(racoon, road_stages, road_index)
        continue
    stage_cfg = SCENES[road_index]
    current_bg = road_stages[road_index]
    racoon_speed = stage_cfg["racoon_speed"]

    if racoon.rect.centerx > SCREEN_WIDTH:
        apple = None
        road_index += 1
        if road_index >= len(road_stages):
            win_screen(screen)
            road_index = len(road_stages) - 1  # stay clamped if win_screen ever returns
        else:
            enter_road(racoon, road_stages, road_index)
        continue

    if (racoon.rect.centerx < 0
            or racoon.rect.centery < 0
            or racoon.rect.centery > SCREEN_HEIGHT):
        racoon.pos_x, racoon.pos_y = 100, 250
        racoon.sync_screen_position(current_bg.scroll_x)

#object setup
    for bike in bikes:
        bike.animate(allow_car=stage_cfg["allow_car"])
        bike.update()
        if check_collision(racoon, bike):
            hit_sfx.play()
            score -= 1

    apple = apple_spawn(apple, score, current_bg.scroll_x)
    if apple:
        if apple.check_interaction(racoon):
            apple_sfx.play()
            score += 1
            apple = None
        elif apple.is_off_screen(current_bg.scroll_x):
            apple = None

#score
    if score <= 0:
        racoon, bikes, city_bg, road_stages, bins = new_game()
        score = 1
        scene = "city"
        game_over_screen(screen)
        continue

    current_bg.update()
    racoon.wall_collision(dx, dy, current_bg.collision_rects, speed=racoon_speed)
    racoon.update()
    racoon.sync_screen_position(current_bg.scroll_x)

#draw
    current_bg.draw(screen)
    racoon.draw(screen)
    for bike in bikes:
        bike.draw(screen)
    if apple:
        apple.draw(screen, current_bg.scroll_x)
    draw_score(screen, score)
    pygame.display.flip()

pygame.quit()