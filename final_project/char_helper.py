import pygame
import random
import time
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

#----------racooon/player class--------------
class Racoon:
    def __init__(self, pos_x=0, pos_y=100):  # default value for start position
        self.idle_frame = self.load_frame("media/pictures/racoon/0.png")
        self.walk_frames = [
            self.load_frame(f"media/pictures/racoon/{i}.png") for i in (1, 2, 3) #for all frames apply load and scale function
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
        self.rect = self.rac.get_rect(center=(self.pos_x, self.pos_y)) #rect setup for collisions
        self.mask = pygame.mask.from_surface(self.walk_frames[0])

        self.hit_timer = 0
        self.hit_duration = 45

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (350, 350)) #load and scale all images

    def animate(self, direction_x, direction_y, collision_rects, speed=3):
        self.is_moving = bool(direction_x or direction_y)
        if direction_x > 0:
            self.facing_left = False
        elif direction_x < 0:
            self.facing_left = True

        hitbox = self.rect.inflate(-300, -300)  # inflate because of transparent pxls

        self.pos_x += direction_x * speed  # check if racoon hits wall
        hitbox.center = (self.pos_x, self.pos_y)
        if any(hitbox.colliderect(wall) for wall in collision_rects):
            self.pos_x -= direction_x * speed

        self.pos_y += direction_y * speed
        hitbox.center = (self.pos_x, self.pos_y)
        if any(hitbox.colliderect(wall) for wall in collision_rects):
            self.pos_y -= direction_y * speed

    def sync_screen_position(self, scroll_x=0):
   #so racoon stays still
        self.rect.center = (self.pos_x - scroll_x, self.pos_y)

    def update(self):
     #see what frsme is showing and move it to next
        if self.is_moving:
            self.animation_timer += 1 #ticks through animation
            if self.animation_timer >= self.animation_speed: #check if enough time has passed to progress animation
                self.animation_timer = 0 #reset timer
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames) #next animation + loop back to 1 if at 3
            self.rac = self.walk_frames[self.frame_index]
            image = pygame.transform.flip(self.rac, self.facing_left, False)
        else:
            self.rac = self.idle_frame
            self.frame_index = 0
            self.animation_timer = 0

        image = pygame.transform.flip(self.rac, self.facing_left, False)
        head_height = int(image.get_height() * 0.3)  #exclude very top of racoon
        self.mask_offset = (0, head_height)
        body_area = image.subsurface((
            0,
            head_height,
            image.get_width(),
            image.get_height() - head_height
        ))
        self.mask = pygame.mask.from_surface(body_area)

        if self.hit_timer > 0:
            self.hit_timer -= 1

    def hit(self):
        self.hit_timer = self.hit_duration

    def draw(self, screen): #draw racoon
        image = pygame.transform.flip(self.rac, self.facing_left, False)
        screen.blit(image, self.rect)

        if self.hit_timer > 0: #red if hit
            image = image.copy()
            red_tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            red_tint.fill((255, 0, 0, 255))
            image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(image, self.rect)

#----------bikes--------------
class Bikes:
    BIKES_CAR = ("a", "b", "c", "d") #account for the 3 types, d is the car
    BIKES_ONLY = ("a", "b", "c")
    CAR_PERCENTAGE = 0.08 #how likely is a car to spawn
    frame_cache = {}

    def __init__(self, pos_x=-100, pos_y=200, variant=None, allow_car=False):
        if variant:
            self.variant = variant
        elif allow_car and random.random() < self.CAR_PERCENTAGE:
            self.variant = "d"
        else:
            self.variant = random.choice(self.BIKES_ONLY)
        self.bikes_frames = self.get_frames(self.variant)
        self.frame_index = 0
        self.animation_speed = 10
        self.animation_timer = 0
        self.is_moving = True
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.bikes_frames[0].get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.bikes_frames[0])
        self.speed = random.randint(5, 13)

    def get_frames(self, variant):
        if variant not in Bikes.frame_cache:  # dictionary to store frames and ensure no reloading
            Bikes.frame_cache[variant] = [
                self.load_frame(f"media/pictures/bikes/{variant}{i}.png") for i in (1, 2, 3)
            ]
        return Bikes.frame_cache[variant]

    def animate(self, direction_y=0, allow_car=False):
        direction_x = -self.speed
        self.is_moving = bool(direction_x or direction_y)
        self.pos_x += direction_x
        self.pos_y += direction_y

        self.rect.center = (self.pos_x, self.pos_y)
        if self.pos_x < -200:
            self.pos_x = SCREEN_WIDTH + random.randint(0, 400)
            self.pos_y = random.randint(100, 400)
            if allow_car and random.random() < self.CAR_PERCENTAGE:
                self.variant = "d"
            else:
                self.variant = random.choice(self.BIKES_ONLY)
            self.bikes_frames = self.get_frames(self.variant)
            self.frame_index = 0
            self.speed = random.randint(5, 13)

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        bounds = img.get_bounding_rect()
        cropped = img.subsurface(bounds).copy()  #remove transparent pxls

        bike_height = 150
        scale_factor = bike_height / cropped.get_height()
        bike_width = int(cropped.get_width() * scale_factor)

        return pygame.transform.scale(cropped, (bike_width, bike_height))

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

        frame = self.bikes_frames[self.frame_index]
        wheel_height = max(10, int(frame.get_height() * 0.2))
        self.mask_offset = (0, frame.get_height() - wheel_height) # offset for wheel

        wheel_area = frame.subsurface(( # crop wheel area
            self.mask_offset[0],
            self.mask_offset[1],
            frame.get_width(),
            wheel_height
        ))

        self.mask = pygame.mask.from_surface(wheel_area)

    def draw(self, screen):
        rect = self.bikes_frames[self.frame_index].get_rect(center=(self.pos_x, self.pos_y))
        screen.blit(self.bikes_frames[self.frame_index], rect)

#-----------collisions :( --------------
def check_collision(racoon, bike):
    bike_mask_x = bike.rect.x + getattr(bike, "mask_offset", (0, 0))[0]
    bike_mask_y = bike.rect.y + getattr(bike, "mask_offset", (0, 0))[1]

    racoon_mask_x = racoon.rect.x + getattr(racoon, "mask_offset", (0, 0))[0]
    racoon_mask_y = racoon.rect.y + getattr(racoon, "mask_offset", (0, 0))[1]

    offset = (racoon_mask_x - bike_mask_x, racoon_mask_y - bike_mask_y)

    if bike.mask.overlap(racoon.mask, offset):
        if racoon.hit_timer == 0:
            racoon.hit()
            return True
    return False

#-----bins----
class Bins:
    def __init__(self, pos_x=0, pos_y=100):
        self.default_frame = self.load_frame("media/pictures/bin/bin.png")
        self.anim_frames = [
            self.load_frame(f"media/pictures/bin/bn{i}.png") for i in range(4)
        ]

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.frame_index = 0
        self.animation_speed = 6
        self.animation_timer = 0
        self.anim_duration = 80
        self.anim_time_left = 0
        self.is_animating = False #for default frame
        self.collected = False        #1 use

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (350, 350))

    def check_interaction(self, racoon):
        if not self.collected and self.interaction(racoon.pos_x, racoon.pos_y):
            return self.animate()
        return False

    def interaction(self, target_x, target_y, tolerance=30): #when racoon is touching bin, interation
        return abs(self.pos_x - target_x) < tolerance and abs(self.pos_y - target_y) < tolerance

    def animate(self):
        if self.collected or self.is_animating:
            return False
        self.collected = True
        self.is_animating = True
        self.frame_index = 0
        self.animation_timer = 0
        self.anim_time_left = self.anim_duration
        return True

    def update(self):
        if not self.is_animating:
            return

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = min(self.frame_index + 1, len(self.anim_frames) - 1)

        self.anim_time_left -= 1
        if self.anim_time_left <= 0:
            self.is_animating = False  # default frame

    def draw(self, screen, pos=None):
        image = self.anim_frames[self.frame_index] if self.is_animating else self.default_frame
        draw_pos = pos if pos is not None else (self.pos_x, self.pos_y)
        rect = image.get_rect(center=draw_pos)
        screen.blit(image, rect)


# -----apple----
class Apple:
    def __init__(self, pos_x=0, pos_y=random.randint(100, 400)):
        self.frame = self.load_frame("media/pictures/apple.png")
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.collected = False

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (60, 60))

    def check_interaction(self, racoon, tolerance=40):  # like bins, closeness
        if self.collected:
            return False
        if abs(self.pos_x - racoon.pos_x) < tolerance and abs(self.pos_y - racoon.pos_y) < tolerance:
            self.collected = True
            return True
        return False

    def is_off_screen(self, scroll_x, screen_width=SCREEN_WIDTH):  # so it can be cleared once passed
        return (self.pos_x - scroll_x) < -100

    def draw(self, screen, scroll_x=0):
        if self.collected:
            return
        screen_x = self.pos_x - scroll_x
        rect = self.frame.get_rect(center=(screen_x, self.pos_y))
        screen.blit(self.frame, rect)