import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 300
BACKGROUND_COLOR = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('image')

car = pygame.image.load("car.jpeg").convert_alpha()
car2 = pygame.image.load("car.jpeg").convert_alpha()
car = pygame.transform.scale(car, (200, 100)) #played around with this until it didnt look stretched anymore and the images dont overlap
car2 = pygame.transform.scale(car2, (200, 100))

clock = pygame.time.Clock()

#when the car is quick it should start flashing (mario cart star inspired)
def apply_flash(image):
    flash = image.copy()
    intensity = random.randint(100, 300)#random intensity of the flashes
    flicker = random.randint(-30, 30)
    flash.fill((   #to figure this flash.fill out, i used ChatAI
        max(0, min(255, intensity + flicker)),
        max(0, min(60, 60 - flicker)),
        0
    ), special_flags=pygame.BLEND_RGB_ADD)
    return flash


class Race:
    def __init__(self, car_x, car_y, car2_x, car2_y):
        self.car_x = car_x
        self.car_y = car_y
        self.car2_x = car2_x
        self.car2_y = car2_y
        self.car_speed = random.uniform(1, 8) #random car speeds
        self.car2_speed = random.uniform(1, 8)

    def moving(self):
        self.car_x += self.car_speed
        self.car2_x += self.car2_speed
        if self.car_x > SCREEN_WIDTH: #make sure it goes back to other side
            self.car_x = -200
        if self.car2_x > SCREEN_WIDTH:
            self.car2_x = -200


class CarColour:
    def __init__(self, car, car2):
        self.car = car
        self.car2 = car2
#random colours for the cars
    def randomize(self):
        r, g, b = random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)
        r2, g2, b2 = random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)
        self.car.fill((r, g, b), special_flags=pygame.BLEND_RGB_ADD)
        self.car2.fill((r2, g2, b2), special_flags=pygame.BLEND_RGB_ADD)
        return self.car, self.car2


race = Race(car_x=100, car_y=150, car2_x=50, car2_y=50)
colour = CarColour(car, car2)
car, car2 = colour.randomize()

tick = 0
flag = True
while flag:
    clock.tick(60)
    tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    # flash effect when speed above 5
    if race.car2_speed > 5:
        car2_display = apply_flash(car2)
    else:
        car2_display = car2

    if race.car_speed > 5:
        car_display = apply_flash(car)
    else:
        car_display = car

    race.moving()
    screen.fill(BACKGROUND_COLOR)
    screen.blit(car_display, (race.car_x, race.car_y))
    screen.blit(car2_display, (race.car2_x, race.car2_y))

    pygame.display.flip()

pygame.quit()
exit(0)