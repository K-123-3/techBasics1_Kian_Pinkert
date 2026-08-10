import pygame

WHITE=(255,255,255)
class Sprite:
    def __init__(self, sheet, frame_width, frame_height, scale=1.0, colorkey=WHITE, speed = 4):
        self.sheet = sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.colorkey = colorkey
        self.speed = speed
        self.facing_right = True

        #pos of sprite
        self.x = 0
        self.y = 0

        #animation
        self.frame_index = 0          #first frame (0) is sitting (so when not moving)
        self.move_frames = [1, 2, 3]  #frame 1,2,3 is walking
        self.animation_cooldown = 100 #100ms
        self._last_update = pygame.time.get_ticks()
        self.moving = False

        self.frames = {} #dict that remembers what frames were cut

    def get_image(self, frame, flip=False):
        #cut frames from sheet and call them

        pic = (frame, flip)
        if pic not in self.frames:
            image = pygame.Surface((self.frame_width, self.frame_height))  # create blank surface
            image.blit(self.sheet, (0, 0),
                       (frame * self.frame_width, 0, self.frame_width, self.frame_height))  # cut racoon
            image = pygame.transform.scale(
                image, (int(self.frame_width * self.scale), int(self.frame_height * self.scale))
            )  # rezised
            if self.colorkey is not None:
                image.set_colorkey(self.colorkey)
            if flip:  # flip sprite if facing left
                image = pygame.transform.flip(image, True, False)  # mirror horizontally
            self.frames[pic] = image
        return self.frames[pic]

    def animate(self, dx, dy):
        #move sprite
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.moving = dx != 0 or dy != 0

        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False #account for backwards moving

        #update animation if cooldown is done
        now = pygame.time.get_ticks()
        if now - self._last_update < self.animation_cooldown:
            return
        self._last_update = now

        if self.moving:
            pos = self.move_frames.index(self.frame_index) if self.frame_index in self.move_frames else -1
            self.frame_index = self.move_frames[(pos + 1) % len(self.move_frames)] #cycles thourgh animations
        else:
            self.frame_index = 0

    def draw(self, surface):
        flip = not self.facing_right
        surface.blit(self.get_image(self.frame_index, flip), (self.x, self.y))
