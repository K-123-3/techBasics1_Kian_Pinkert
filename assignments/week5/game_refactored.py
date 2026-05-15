import time
import sys


def delay(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
print()

SHELVES = ('1', '2', '3', '4')
SHELF_CONTENT = {
    '1': (
        "➀  A – Art",
        """\
        You look at the beautiful artwork on display.
        There are some marbled slabs with colorful painted swirls that
        almost look hypnotizing. You force yourself to look away.\
        """
    ),
    '2': (
        "➁  B – Books",
        """\
       The books on the shelf are dusty and the paper seems stained.
       All books cover topics of spiritual nature.
       The books almost seem to draw you in, in a weird way.
       You decide its best not to linger on them too long..\
        """
    ),
    '3': (
        "➂  C – Candles",
        """\
        The clearly handmade candles come in mostly wonky, curved shapes.
        The colors and scents seem to match, the bright yellow candle
        promising a smelll of 'a sunny day' whilst the black candle
        already emits a deep charcoal-akin smell.
        You decide to move on before you get a headache..\
        """
    ),
    '4': (
        "➃  D – Decoration, small items of many origins",
        """\
        You examine the Decorations. You cant really make out what
        they are supposed to be but there are horse-like wooden figures
        with wings and horns aswell as small bowls and cups that seem both 
        translucent and solid at the same time. You could swear the horse-
        figure moved an inch in your periphery.\
        """
    )} #shelf content as constant to keep function short
DEBUG = False


def door_scene():
    delay("""In front of you is a door, leading to a small antique shop. Do you go in?
""")
    time.sleep(1)
    while True:
        enter = input("Enter the shop? ").strip().lower()
        if enter == 'yes':
            break
        elif enter == 'no':
            print("Well... you leave.")
            exit()
        else:
            print("yes or no?")

    delay("You enter the shop")
    time.sleep(1)
# first choice, you can continue or stop immediatly


def name_scene():
    delay("""
The Shopkeeper is an older woman with gray hair. 
Her appearance is almost witch-like.
'✵ Oh Hello! I haven't seen you around before.. """)
    time.sleep(1)
    name = input("What's your name? ✵' ")
    time.sleep(1)
    print("'✵ Why Hello", name, "! Welcome to my shop. Please, take a look around. ✵'")
# user input for name


def shelf_scene():
    time.sleep(2)
    delay("""You look around. The Shelves are labeled with antique lettering:
 ➀: A- Art, carved and painted
 ➁: B- Books, from astrology to witchcraft
 ➂: C- Candles, Flames in all colours available
 ➃: D- Decoration, small Items of many origins
 """)
    time.sleep(2)  # to have enough time for user to read

    Shelves_done = set()
    while len(Shelves_done) < len(SHELVES):
        remaining = [k for k in SHELVES if
                     k not in Shelves_done]  # this line i asked ChatAI for help with as i couldnt get it to work
        shelf = input(f"Which shelf do you examine? {remaining}: ").strip()

        if shelf not in SHELVES:
            delay("""Please enter 1, 2, 3 or 4
            """)
            continue #ask again for input incase user enters something else

        if shelf in Shelves_done:
            print("You already looked at that one…")
            time.sleep(0.5)
            continue

        label, description = examine_shelf(shelf) #takes from variable to insert shelf content
        print(f"\n  {label}") #label and content seperately so only content is delayed
        delay(description)
        print()
        time.sleep(0.5)
        Shelves_done.add(shelf)


def examine_shelf(Shelves):
    return SHELF_CONTENT[Shelves]


# return argument function for the examining

def done_scene():
    time.sleep(1)
    print('''
 You looked at all Shelves. The Shopkeeper looks up.''')
    time.sleep(1)
    delay("'✵ Well? Want anything? ✵'")


def buy_scene():
    while True:
        answer = input("Please tell me yes...✵'").strip().upper()
        time.sleep(1)
        if answer == 'YES':
            delay("""You want to say yes but you couldn't possibly decide on one thing!
    The items draw you in more and more... it takes all of your strength to move
    from where you stand as you stumble out of the door, your heart pounding as the
    strange shop tries to draw you in...
    """)
            time.sleep(2)
            break
        elif answer == 'NO':
            delay("""You don't want anything- this place is strange.
    You feel the Items calling to you as you need an unusual amount
    of strength to stumble out of the shop.
    """)
            time.sleep(2)
            break
        else:
            print('"Yes or No?')


def end():
    delay("""As you turn around to take a last look inside, the shop is gone.
 Thanks for playing!""")


def main():
    door_scene()
    name_scene()
    shelf_scene()
    done_scene()
    buy_scene()
    end()


if __name__ == "__main__":
    main()
