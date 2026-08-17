# from requirements.txt import *
from map_helper import *
from screens import *
from constants import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')


#audio
hit_sfx = safe_sound('media/music_sfx/hit_sfx.mp3')
apple_sfx = safe_sound('media/music_sfx/apple_sfx.mp3')
trash_sfx = safe_sound('media/music_sfx/trash_sfx.mp3')
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


#objectives

objectives_font = pygame.font.SysFont("Arial", 20, bold=True)
objective1 = objectives_font.render("Get some food" , False, (200, 200, 200))
obj1_rect = objective1.get_rect(center = (900, 20))

objective2 = objectives_font.render("Get to the train station", False, (200, 200, 200))
obj2_rect = objective2.get_rect(center = (850, 20))

objective3 = objectives_font.render("Hurry!!", False, (250, 250, 250))
obj3_rect = objective3.get_rect(center = (900, 20))

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
def main():
    racoon, bikes, city_bg, road_stages, bins = new_game()
    apple = None
    score = 0  # set to MAX_LIVES if scene is road for debug
    welcome = True
    game_time = None
    DEBUG_SCENES = 2  # set to scene number to debug None = city, 0 = road, 1 = road2, 2 = road3

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and welcome:
                welcome = False
                game_time = pygame.time.get_ticks()
    #control setup
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    #scene setup

        if scene == "city":
            if not welcome:
                racoon.animate(dx, dy, city_bg.collision_rects)
                racoon.update()
            city_bg.draw_camera(screen, racoon)

            for trash_bin in bins:
                trash_bin.update()
                if trash_bin.check_interaction(racoon):
                    trash_sfx.play()
                    score = min(score + 1, MAX_LIVES)
                trash_bin.draw(screen, city_bg.to_screen_pos(trash_bin.pos_x, trash_bin.pos_y))

            screen_x, screen_y = city_bg.player_screen_pos(racoon)
            racoon.rect.center = (screen_x, screen_y)
            racoon.draw(screen)
            draw_score(screen, score)
            if welcome:
                welcome_box(screen)
            screen.blit(objective1, obj1_rect)
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
                elapsed_ms = pygame.time.get_ticks() - game_time if game_time else 0
                win_screen(screen, score=score, time_taken=elapsed_ms / 1000)
                racoon, bikes, city_bg, road_stages, bins = new_game()
                score = 1
                scene = "city"
            else:
                enter_road(racoon, road_stages, road_index)
            continue

        if racoon.rect.centerx < 0: #when off screen -> loose a life
            score -= 1
            hit_sfx.play()
            racoon.pos_x = current_bg.scroll_x + SCREEN_WIDTH // 2
            racoon.pos_y = SCREEN_HEIGHT // 2
            racoon.sync_screen_position(current_bg.scroll_x)
        elif (racoon.rect.centery < 0
              or racoon.rect.centery > SCREEN_HEIGHT):
            racoon.pos_x, racoon.pos_y = 100, 250
            racoon.sync_screen_position(current_bg.scroll_x)

        current_bg.update()
        racoon.animate(dx, dy, current_bg.collision_rects, speed=racoon_speed)
        racoon.update()
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
                score = min(score + 1, MAX_LIVES)
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

    #draw
        current_bg.draw(screen)
        racoon.draw(screen)
        for bike in bikes:
            bike.draw(screen)
        if apple:
            apple.draw(screen, current_bg.scroll_x)
        draw_score(screen, score)
        if road_index == 0:
            screen.blit(objective2, obj2_rect)
        else:
            screen.blit(objective3, obj3_rect)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()