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

### function from the Helper.py


def isCollided(Bullet, Stormtrooper):
   
    bx = Bullet.pos_x + Bullet.img.get_width()  / 2   #This gets the center of the image as its x position, which will be at its left corner, is added to half of its width
    by = Bullet.pos_y + Bullet.img.get_height() / 2   # same just woth the y position
    tx = Stormtrooper.pos_x + Stormtrooper.img.get_width()  / 2
    ty = Stormtrooper.pos_y + Stormtrooper.img.get_height() / 2

    distance = math.sqrt(math.pow(bx - tx, 2) + math.pow(by - ty, 2))  #calculate distance using Pythagorean theorem

    if distance < 60:
        return True  #if less than 60 is between bullet and stormtrooper center, it detects as a collision
    else:
        return False

  ### and from Main.py to also analyse its use:
  
    for b in bullets:
        for st in stormtroops:
            if isCollided(b, st):
                bullets.remove(b) #bullet and stormtrooper dissapear
                stormtroops.remove(st)  
                score += 1   #you get a point
                break

The isCollided function always requires two arguments, Bullet and Stormtrooper. In the Main code these are shortened to b and st.
In the isCollided function it is checked wether the collision is true or not. To find this out, the coordinates of the bullet (bx and by) 
are retrieved and the image width or height is halved to have the coordinate of the center of the image.
Same is done for the Stormtrooper (tx and ty).
The distance of the two is calculated using the Pythagorean theorem to get the hypotenuse between bullet center and stormtrooper center, which is the distance-
If the distance is less than 60, the collision is true, otherwise it is false.
In the Main code, if the collision is true, the bullet and the stormtrooper are removed and the users score increases by 1.

## Takeaways: are there anything you can learn from the code? (How to structure your code, a clean solution for some function you might also need...)

I will likely also structure my code with a helper and a main to keep things cleaner and more organized. The calculation of the distance between two objects to measure when a collision happens also was not something i knew how to do so that will be very helpful. 

## What parts of the code were confusing or difficult at the beginning to understand?
##   - Were you able to understand what it is doing after your own research?

I had to reread the Game over and Start screen function a few times to fully understand what was happening in for example this part:
prompt = font.render("SPACE : RESTART | Q: QUIT", True, (255, 255, 255))
    prompt_rect = prompt.get_rect(midtop=(sw / 2, rect.bottom + 16))

The most difficult for me was the

distance = math.sqrt(math.pow(bx - tx, 2) + math.pow(by - ty, 2))

because i didnt at first connect it to the Pythagoream theory but with some research i saw the connection and found it much simpler to grasp.


## Extra Notes

In the game over screen i found the 

frozen = screen.copy()

screen.blit(frozen, (0, 0))

 code very interesting because having the screen freeze behind the game over screen is something i wanted to implement aswell and didnt know how to.
 
