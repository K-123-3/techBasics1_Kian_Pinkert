import time
import sys


def delay(text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


print()

inventory = []
items_in_forest = [
    {"name": "rope", "type": "tool", "description": "A bundle of rope."},
    {"name": "mushrooms", "type": "food..?", "description": "Are you sure you want to use that?"},
    {"name": "axe", "type": "tool/weapon", "description": "It doesnt look that sharp but may still be usable"},
    {"name": "stick", "type": "tool", "description": "A dry wooden stick."},
    {"name": "berries", "type": "food",
     "description": "You saw some birds taking some of these berries off of a bush. Seems safe enough"},
    {"name": "flint", "type": "tool", "description": "Some sharp, shiny flintstones"}
]
# length shall be larger than max inventory size if there is only one room
MAX_INVENTORY_SIZE = 5


# Functions

def find_item(name, collection):
    for item in collection:
        if item["name"] == name:
            return item
    return None #i used ChatAI to help with this function


def show_inventory():
    if len(inventory) == 0:
        print("Your inventory is empty.")
    elif len(inventory) == MAX_INVENTORY_SIZE:
        print("Your inventory is full.")
        for items in inventory:
            print(f'{items["name"]}')
    else:
        for items in inventory:
          print(f'{items["name"]}')
                # list all names of items in the inventory, consider the case when the list is empty -> refer to constant


def show_room_items():
    if not items_in_forest:
        print("Nothing to see here.")
    else:
        print("You see:")
        for item in items_in_forest:
            print(f'  - {item["name"]}')
    # list all items in current room, when empty then nothing to see


def pick_up(item_name):
    if len(inventory) >= MAX_INVENTORY_SIZE:
        print("Your inventory is full. Maybe you can drop or use something?")
        return
    item = find_item(item_name, items_in_forest)
    if item:
        items_in_forest.remove(item)
        inventory.append(item)
        print(f'You pick up the {item["name"]}.')
    else:
        print(f"There is no '{item_name}' here.")
    # pick up an item from the room if inventory limit is not met yet. removes item from forest too


def drop(item_name):
    item = find_item(item_name, inventory)
    if item:
        inventory.remove(item)
        items_in_forest.append(item)
        print(f'You drop the {item["name"]}.')
    else:
        print(f"You don't have that")
# drop an item from your inventory, at the same time append it back to the list of items for the room


def examine(item_name):
    item = find_item(item_name, inventory) or find_item(item_name, items_in_forest)
    if item:
        print(item["description"])
    else:
        print("You don't see that here.")
# examining returns description (if the item is there)

def use(item_name):
    item = find_item(item_name, inventory)
    if not item:
        print(f"You don't have '{item_name}'.")
        return
    name = item["name"] #to make it easier to write

    if name == "axe":
        inventory.remove(item)
        delay("You use the axe to chop down a small tree. Now you have some wood, but the axe broke...and its hard to carry loose logs...")
        inventory.append({"name": "wood", "type": "material", "description": "some chopped logs."}) #axe breaks but wood is added to inventory

    elif name == "rope":
        wood = find_item("wood", inventory)
        if wood is not None: #i used chatai for these two lines as i tried to work with boolean, which wasnt possible
            inventory.remove(item)
            inventory.remove(wood)
            delay("You bundle the logs. Great Job! but its getting dark now-you can hardly see the way...")
            inventory.append({"name": "bundle", "type": "material", "description": "Bundled wood"}) #"merges" wood and rope to bundle
        else:
            print("This isnt useful right now")

    elif name == "mushrooms":
        delay("""You eat a strange mushroom. You start feeling dizzy and colours appear in your vision. 
        you stumble around dazedly... what were you here for again? If you forgot, it cant be that important. 
        The forest makes you feel smaller and smaller- are the trees growing?
        You run, scared by the looming trees.
        You eventually come down from your trip... its dark but you can see the village in the distance. 
        You return with no wood...embarassing
        ==================
        You Lost!
        ==================
         """) #ends the game
        exit()

    elif name == "stick":
        bundle = find_item("bundle", inventory)
        if bundle is not None: #it only gets dark once bundle is aquired, no use before then
            flint = find_item("flint", inventory)
            if flint is not None: #flint needed to make torch work
                inventory.remove(item)
                inventory.remove(flint)
                delay("""You use the flint to light the stick. You can see now! 
                But you are also REALLY hungry- you will need some energy for the way back""")
                inventory.append({"name": "torch", "type": "tool", "description": "A makeshift torch to light the way"})
            else:
                print("You need something to light it with...")
        else:
            print("No use for that right now")

    elif name == "flint": #make it possible to also use flint instead of stick to recieve torch
        bundle = find_item("bundle", inventory)
        if bundle is not None:
            stick = find_item("stick", inventory)
            if stick is not None:
                inventory.remove(item)
                inventory.remove(stick)
                delay("""You use the flint to light the stick. You can see now! 
                But you are also REALLY hungry- you will need some energy for the way back""")
                inventory.append({"name": "torch", "type": "tool", "description": "A makeshift torch to light the way"})
            else:
                print("You need something to light up...")
        else:
            print("No use for that right now")

    elif name == "berries": #only needed once its dark and you're hungry, also ends the game
        torch = find_item("torch", inventory)
        if torch is not None:
            delay("""You eat some berries. much better! You start your journey back.
            Good job! You accomplished your objective.
            =========================
            You win!!!
            =========================""")
            exit()

        else:
            print("You dont feel hungry right now")

    else:
        print("This isnt useful right now!")



def game_loop():
    delay("""You are a simple villager of ralzica. It is getting close to winter and you want to gather some wood. 
    You go into the forest near your house, where you have already layed out some useful items this morning and left them here """)
    print("""
        ========================================================================
        Objective: gather some wood and get home safely before nightfall.
        ========================================================================
        """)
    print("Tip: You can always type 'help' for a list of commands.")

    while True:
        command = input("\n> ").strip().lower()

        match command.split():
            case ["help"]:
                print("Commands: inventory, look, pickup [item], drop [item], use [item], examine [item], quit")
            case ["inventory"]:
                show_inventory()
            case ["look"]:
                show_room_items()
            case ["pickup", item_name]:
                pick_up(item_name)
            case ["drop", item_name]:
                drop(item_name)
            case ["use", item_name]:
                use(item_name)
            case ["examine", item_name]:
                examine(item_name)
            case ["quit"]:
                print("Thanks for playing!")
                break
            case _:  # else
                print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    game_loop()
