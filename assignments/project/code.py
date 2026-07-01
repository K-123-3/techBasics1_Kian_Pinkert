import pygame
import sprite

pygame.display.init()

WHITE = (255, 255, 255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# create the display object of specific dimension (X, Y).


bg = pygame.image.load("media/bg.png").convert_alpha()
racoon = pygame.image.load("media/racoon.png").convert_alpha()
racoon_sprite = sprite.Sprite(racoon)

# create list for animation
animation_list = []
animation_steps = [1, 4] #1 frame in sitting, 3 frames in moving
movement = 1  #movement 0 is sitting, 1 is running
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_rac_list = []
    for i in range (animation):
        temp_rac_list.append(racoon_sprite.get_image(step_counter, 500, 500, 0.7, WHITE))
        step_counter += 1
    animation_list.append(temp_rac_list)


# paint screen one time
pygame.display.flip()
flag = True
# quit pygame
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    screen.blit(bg, (0,0))
    clock.tick(60)


    # update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown: #if cooldown ms have passed, next frame
        frame += 1
        last_update = current_time #reset cooldown
        if frame > len(animation_steps):
            frame = 1

    #show animation
    screen.blit(animation_list[movement][frame], (0, 0))


    pygame.display.flip()
pygame.quit()
exit(0)

