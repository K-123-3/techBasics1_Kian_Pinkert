## Where did you find the code and why did you choose it? (Provide the link)

I found the code through the old projects that were presented
Link: 
https://github.com/Nestorbruno01/ChewbaccasAdventure/blob/main/Helper.py
I chose it because i also want to create a game with a movable protagonists and elements of colliosion- here the collision is with bullets whilst in my game i want it to be with bikes.

## What does the program do? What's the general structure of the program?

Fist, multiple classes are created.
For the Chewbaccca class and the Stormtrooper class the image is imported and positioned, then animated and then put on screen via a draw function that blits it on the screen.
Same is done for a Bullet class, which is then used with the Stormtrooper to define the isCollided function. A score, a Game over and a start screen and an increase_difficulty function are also defined. 
The game over screen also gives the player the ability to restart the game and the start screen also features instructions for the game.
The code serves as a helper for the main code, which uses the classes and functions defined here. 

## Function analysis: pick one function and analyze it in detail:

# function from the Helper.py

def isCollided(Bullet, Stormtrooper):
    #finding the center coordinates
    bx = Bullet.pos_x + Bullet.img.get_width()  / 2
    by = Bullet.pos_y + Bullet.img.get_height() / 2
    tx = Stormtrooper.pos_x + Stormtrooper.img.get_width()  / 2
    ty = Stormtrooper.pos_y + Stormtrooper.img.get_height() / 2

    distance = math.sqrt(math.pow(bx - tx, 2) + math.pow(by - ty, 2))

    if distance < 60:
        return True
    else:
        return False

  #  and from the Main.py code to also analyse the use of the function:

    for b in bullets:
        for st in stormtroops:
            if isCollided(b, st):
                bullets.remove(b)
                stormtroops.remove(st)
                score += 1
                break


