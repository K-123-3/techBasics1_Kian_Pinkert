import pygame
import random
import math
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

#----------racooon/player class--------------
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
        self.rect = self.rac.get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.walk_frames[0])

        self.hit_timer = 0
        self.hit_duration = 45

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (350, 350)) #load and scale all images

    def animate(self, direction_x=0, direction_y=0):
        self.is_moving = bool(direction_x or direction_y)
        self.pos_x += direction_x * 3
        self.pos_y += direction_y * 3

        if direction_x > 0:
            self.facing_left = False
        elif direction_x < 0:
            self.facing_left = True

    def wall_collision(self, direction_x, direction_y, collision_rects):
        self.is_moving = bool(direction_x or direction_y)
        if direction_x > 0:
            self.facing_left = False
        elif direction_x < 0:
            self.facing_left = True

        hitbox = self.rect.inflate(-300, -300) #inflate because of transparent pxls

        self.pos_x += direction_x * 3 #check if racoon hits wall
        hitbox.center = (self.pos_x, self.pos_y)
        if any(hitbox.colliderect(wall) for wall in collision_rects):
            self.pos_x -= direction_x * 3

        self.pos_y += direction_y * 3
        hitbox.center = (self.pos_x, self.pos_y)
        if any(hitbox.colliderect(wall) for wall in collision_rects):
            self.pos_y -= direction_y * 3

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
            self.mask = pygame.mask.from_surface(image)
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

    def is_off_screen(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        return (
                self.rect.centerx < 0 or self.rect.centerx > width
                or self.rect.centery < 0 or self.rect.centery > height
        )

#----------bikes--------------
class Bikes:
    BIKES = ("a", "b", "c") #account for the 3 types
    frame_cache = {}
    spawn_margin = 150

    def __init__(self, pos_x=0, pos_y=200, variant=None):
        self.variant = variant if variant else random.choice(self.BIKES) #variant for testing purposes
        self.bikes_frames = self.get_frames(self.variant)

        self.frame_index = 0
        self.animation_speed = 10
        self.animation_timer = 0
        self.is_moving = True
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.bikes_frames[0].get_rect(center=(self.pos_x, self.pos_y))
        self.mask = pygame.mask.from_surface(self.bikes_frames[0])

    def get_frames(self, variant):
        if variant not in Bikes.frame_cache: #dictionary to store frames and ensure no reloading
            Bikes.frame_cache[variant] = [
                self.load_frame(f"pictures/bikes/{variant}{i}.png") for i in (1, 2, 3)
            ]
        return Bikes.frame_cache[variant]

    def animate(self, direction_x=-1, direction_y=0):
        self.is_moving = bool(direction_x or direction_y)
        self.pos_x += direction_x
        self.pos_y += direction_y

        frame = self.bikes_frames[self.frame_index]
        self.rect.topleft = (self.pos_x, self.pos_y)  # match draw()'s blit position
        if self.pos_x < -200:
            self.pos_x = SCREEN_WIDTH + random.randint(0, 400)
            self.pos_y = random.randint(100, 400)
            self.variant = random.choice(self.BIKES)
            self.bikes_frames = self.get_frames(self.variant)
            self.frame_index = 0

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

        wheel_area = frame.subsurface((
            self.mask_offset[0],
            self.mask_offset[1],
            frame.get_width(),
            wheel_height
        ))

        self.mask = pygame.mask.from_surface(wheel_area)

    def draw(self, screen):
        screen.blit(self.bikes_frames[self.frame_index], (self.pos_x, self.pos_y))


#-----------collisions :( --------------
def check_collision(racoon, bike):
    bike_mask_x = bike.rect.x + getattr(bike, "mask_offset", (0, 0))[0]
    bike_mask_y = bike.rect.y + getattr(bike, "mask_offset", (0, 0))[1]

    offset = (racoon.rect.x - bike_mask_x, racoon.rect.y - bike_mask_y)

    if bike.mask.overlap(racoon.mask, offset):
        if racoon.hit_timer == 0: #count hits
            racoon.hit()
            return True
    return False


#-----bins----
class Bins:
    def __init__(self, pos_x=0, pos_y=100):
        self.default_frame = self.load_frame("pictures/bin/bin.png")
        self.anim_frames = [
            self.load_frame(f"pictures/bin/bn{i}.png") for i in range(4)
        ]

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.frame_index = 0
        self.animation_speed = 6
        self.animation_timer = 0
        self.anim_duration = 80
        self.anim_time_left = 0
        self.is_animating = False
        self.collected = False        #1 use

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (130, 130))

    def interaction(self, target_x, target_y, tolerance=70):
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

    def check_interaction(self, racoon):
        if not self.collected and self.interaction(racoon.pos_x, racoon.pos_y):
            return self.animate()
        return False

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