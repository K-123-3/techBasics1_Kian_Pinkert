import time
import sys

def delay (text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
print()

delay("""In front of you is a door, leading to a small antique shop. Do you go in?
""")
time.sleep(1)
while True:
    ShopChoice = input("Enter the shop? ").strip().lower()
    if ShopChoice =='yes':
        break
    elif ShopChoice == 'no' :
        print("Well... you leave.")
        exit()
    else:
        print("yes or no?")

delay("You enter the shop")
time.sleep(1)
#first choice, you can continue or stop immediatly

delay("""
The Shopkeeper is an older woman with gray hair. 
Her appearance is almost witch-like.
'✵ Oh Hello! I haven't seen you around before.. """)
time.sleep(1)
name = input("What's your name? ✵' ")
time.sleep(1)
print("'✵ Why Hello", name, "! Welcome to my shop. Please, take a look around. ✵'")
#user input for name

time.sleep(2) 
delay("""You look around. The Shelves are labeled with antique lettering:
 ➀: A- Art, carved and painted
 ➁: B- Books, from astrology to witchcraft
 ➂: C- Candles, Flames in all colours available
 ➃: D- Decoration, small Items of many origins
 """)
time.sleep(3) #to have enough time for user to read

Shelves_done = set()
Shelves = {'1' , '2' , '3' , '4'}
while len(Shelves_done) < 4:
    shelf = input("What do you look at? 1, 2, 3 or 4?")
    if shelf in Shelves:
        if shelf in Shelves_done:
            print("You already saw that...")
            time.sleep(1)#not allowing endless loop with same shelf
        else:
            print(f"You examine shelf {shelf}")
            if shelf == '1':
                delay("""
                A- Arwork
                You look at the beautiful artwork on display.
                There are some marbled slabs with colorful painted swirls that
                almost look hypnotizing. You force yourself to look away.
                  
                 """)
                time.sleep(0.05)
            elif shelf == '2':
                delay("""
                B- Books
                The books on the shelf are dusty and the paper seems stained.
                All books cover topics of spiritual nature.
                The books almost seem to draw you in, in a weird way.
                You decide its best not to linger on them too long.
                
                """)
                time.sleep(0.05)
            elif shelf == '3':
                delay("""
                C- Candles
                The clearly handmade candles come in mostly wonky, curved shapes.
                The colors and scents seem to match, the bright yellow candle
                promising a smelll of 'a sunny day' whilst the black candle
                already emits a deep charcoal-akin smell.
                You decide to move on before you get a headache.
                
                """)
                time.sleep(0.05)
            else: delay("""
            D- Decoration
            You examine the Decorations. You cant really make out what
            they are supposed to be but there are horse-like wooden figures
            with wings and horns aswell as small bowls and cups that seem both 
            translucent and solid at the same time. You could swear the horse-
            figure moved an inch in your periphery.
            
            """)
            time.sleep(0.05)
            Shelves_done.add(shelf) #once shelf has been examined, You can't recheck it
    else: print('Please enter 1, 2, 3, or 4!')
#examination of shelves with different contents

time.sleep(2)
print('''
You looked at all Shelves. The Shopkeeper looks up.''')
time.sleep(1)
delay("'✵ Well? Want anything? ✵'")


while True:
  answer = input("Please tell me yes...✵'").strip().upper()
  time.sleep(1)
  if answer == 'YES':
      delay("""You want to say yes but you couldn't possibly decide on one thing!
    The items draw you in more and more... it takes all of your strength to move
    from where you stand as you stumble out of the door, your heart pounding as the
    strange shop tries to draw you in...
    """)
      time.sleep(3)
      break
  elif answer == 'NO':
       delay("""You don't want anything- this place is strange.
    You feel the Items calling to you as you need an unusual amount
    of strength to stumble out of the shop.
    """)
       time.sleep(3)
       break
  else: print('"Yes or No?')

delay("""As you turn around to take a last look inside, the shop is gone.
Thanks for playing!""")

#i have also updated the README to include info about making this code
