import random
from turtle import *

width = 500
height = 500
setup(width, height)

tracer(0, 0)
bgcolor('skyblue')
color('#ffffff')

#cloud positions
positions = []

while len(positions) < random.randint(5, 8):
    x = random.randint(-250, 250)
    y = random.randint(-250, 250)

    #positions shouldnt bee too close to one another
    too_close = False
    for (px, py) in positions:
        if abs(x - px) < 80 and abs(y - py) < 70:
            too_close = True

    if not too_close:
        positions.append((x, y))

for (x, y) in positions:
    num_puffs = random.randint(6, 9) #randomly big clouds

    for i in range(num_puffs):
        px = x + random.randint(-45, 40) #offset the puffs
        py = y + random.randint(-15, 20)
        radius = random.randint(20, 30) #random puffsize
        penup()
        goto(px, py - radius) #move to bottom of cloud so it will be in desired position
        pendown()
        begin_fill()
        circle(radius)
        end_fill()

penup()
exitonclick()

#I asked ChatAI for help regarding questions for the positions, line 20-26, to ensure the clouds have space between them