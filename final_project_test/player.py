import pygame
import random
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

class Bikes:
    def __init__(self, pos_x=0, pos_y=100):
        self.bikes_frames = [
            self.load_frame(f"pictures/bikes/a{i}.png") for i in (1, 2, 3)
        ]

        self.frame_index = 0
        self.animation_speed = 8
        self.animation_timer = 0
        self.is_moving = True
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.bikes_frames[0].get_rect(center=(self.pos_x, self.pos_y)).inflate(-350, -350)

    def animate(self, direction_x=-1, direction_y=0):
        self.is_moving = bool(direction_x or direction_y)

        self.pos_x += direction_x
        self.pos_y += direction_y
        self.rect.center = (self.pos_x + 200, self.pos_y + 200)

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (400, 400))

    def update(self):
        if self.is_moving:
            self.animation_timer += 1  # ticks through animation
            if self.animation_timer >= self.animation_speed:  # check if enough time has passed to progress animation
                self.animation_timer = 0  # reset timer
                self.frame_index = (self.frame_index + 1) % len(
                    self.bikes_frames)  # next animation + loop back to 1 if at 3
        else:
            self.frame_index = 0
            self.animation_timer = 0

    def draw(self, screen):
        screen.blit(self.bikes_frames[self.frame_index], (self.pos_x, self.pos_y))



#racooon/player class
class Racoon:
    def __init__(self, pos_x=0, pos_y=100):  # default value for start position
        self.idle_frame = self.load_frame("pictures/racoon/0.png")
        self.walk_frames = [
            self.load_frame(f"pictures/racoon/{i}.png") for i in (1, 2, 3) #for all frames apply load and scale function
        ]

        self.frame_index = 0
        self.animation_speed = 8
        self.animation_timer = 0
        self.is_moving = False #start still
        self.facing_left = False #start facing right
        # init position
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rac = self.idle_frame
        self.rect = self.rac.get_rect(center=(self.pos_x, self.pos_y)).inflate(-150, -150)

        self.hit_timer = 0
        self.hit_duration = 1

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (300, 300)) #load and scale all images

    def animate(self, direction_x=0, direction_y=0):
        self.is_moving = bool(direction_x or direction_y)

        self.pos_x += direction_x * 3 #walking speed
        self.pos_y += direction_y * 3

        self.pos_x = max(0, min(SCREEN_WIDTH, self.pos_x))
        self.pos_y = max(0, min(SCREEN_HEIGHT, self.pos_y))

        self.rect.center = (self.pos_x, self.pos_y)

        if direction_x > 0:
            self.facing_left = False
        elif direction_x < 0:
            self.facing_left = True

    def update(self):
     #see what frsme is showing and move it to next
        if self.is_moving:
            self.animation_timer += 1 #ticks through animation
            if self.animation_timer >= self.animation_speed: #check if enough time has passed to progress animation
                self.animation_timer = 0 #reset timer
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames) #next animation + loop back to 1 if at 3
            self.rac = self.walk_frames[self.frame_index]
        else:
            self.rac = self.idle_frame
            self.frame_index = 0
            self.animation_timer = 0

        if self.hit_timer > 0:
             self.hit_timer -= 1

    def hit(self):
        self.hit_timer = self.hit_duration

    def draw(self, screen):
        image = pygame.transform.flip(self.rac, self.facing_left, False)
        screen.blit(image, self.rect)

        if self.hit_timer > 0:
            image = image.copy()
            red_tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            red_tint.fill((255, 0, 0, 255))
            image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(image, self.rect)




def check_collision(racoon, bike):

    if racoon.rect.colliderect(bike.rect):
        racoon.hit()
        return True
    return False
