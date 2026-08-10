from char_helper import *
# from requirements.txt  import *

pygame.display.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Racoon game')

bin = Bins(100, 100)
racoon = Racoon(100, 100)
bg = pygame.image.load("pictures/img.png").convert_alpha()

flag = True
while flag:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] #keys = walking
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    racoon.animate(direction_x=dx, direction_y=dy)
    racoon.update()


    screen.blit(bg, (0, 0))
    racoon.draw(screen)

    pygame.display.flip()

pygame.quit()




#helper:


class Bins:
    def __init__(self, pos_x=0, pos_y=100):
        self.bin_frames = [
            self.load_frame(f"pictures/bin/bn{i}.png") for i in (0, 1, 2, 3)
        ]

        self.frame_index = 0
        self.animation_speed = 8
        self.animation_timer = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.bin_frames[0].get_rect(center=(self.pos_x, self.pos_y)).inflate(-350, -350)

    def animate(self, direction_x=-1, direction_y=0):
        self.is_moving = bool(direction_x or direction_y)

        self.pos_x += direction_x
        self.pos_y += direction_y
        self.rect.center = (self.pos_x + 200, self.pos_y + 200)

    def load_frame(self, path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (300, 300))

    def update(self):
        self.animation_timer += 1  # ticks through animation
        if self.animation_timer >= self.animation_speed:  # check if enough time has passed to progress animation
            self.animation_timer = 0  # reset timer
            self.frame_index = (self.frame_index + 1) % len(
                self.bin_frames)  # next animation + loop back to 1 if at 3

    def draw(self, screen):
        screen.blit(self.bin_frames[self.frame_index], (self.pos_x, self.pos_y))

    def check_interaction(racoon, bin, screen):
        if racoon.rect.colliderect(bin.rect):
            bin.update()
            bin.draw(screen)
            return True
        else:
            screen.blit('pictures/bin/bin.png', (bin.pos_x, bin.pos_y))
        return False
