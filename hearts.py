#-----------------------------------------------------------------------------#
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|/
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# HEARTS (GAME)                                                          2026 |
#  <3 =^w^=                                       /\  /\                      |
#                                                 \ \/ /                      |
# PLEASE PLAY THE GAME FIRST !!!                   \  /                       |
# Run: python hearts.py                             \/           PYTHON:UTF-8 |
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|/
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#--IMPORTS--------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# Built in python modules used:

import random # for dice rolls,, riddle selectionn, garble text shuffling
import time # slow print delays and scene pauses, and dramatic effect
import os # clears terminal/console screen between scenes and subscenes

#--CONFIGURATIONS-------------------------------------------------------------#

SLOW_PRINT_DELAY = 0.017 # default configuration for slow print effect

#--GLOBAL_VARIABLES_AND_STATES------------------------------------------------#

player_name = ""
hearts = 1              # <3
berries = 0
attack_strength = 1     # starts at 1, upgraded to 4 after sword warrior, 10 after chess cave
fantasii_pets = 0       # tracks player has petted cat, used as damage in dragon fight
cat_went_right = True   # Act 3 encounter order after the path split
inventory = []
Fantasii = False        # True after cat save, node_2_Fantasii, =^w^=
                        # Fantasii is a Norwegian Forest Cat

#--END_GAME_GLOBAL_VARIABLES_AND_STATES---------------------------------------#

berries_acquired = 0
berries_eaten = 0
scroll_results = []     # stores (warrior_name, roll) tuples, for ending_stats
dice_rolls = 0
crow_rescues = 0
warriors_faced = []
berries_offered_to = [] # tracks who received berries, checked for secret ending
queen_restored = False  # True if player uses gesture on queen, unlock queen alliance
queen_fights = False    # True if player accepts queen's offer to fight dragon together

#--SCROLL_NARRATIVES----------------------------------------------------------#
# Dice roll (1-6) maps to Scroll narrative outcome.
# Rolls 1-3: lose, 4-6 win

SWORD_SCROLL  = {
    1:"The Scroll Darkens... you battle blind (lose)",
    2:"The Scroll Glooms... you battle slow (lose)",
    3:"The Scroll Hastens... you battle tired (lose)",
    4:"The Scroll Glows.. you battle fast (win)",
    5:"The Scroll Shines... you battle with clarity (win)",
    6:"The Scroll Blazes... you strike with fury (win)",
}

SHIELD_SCROLL = {
    1: "The Scroll Darkens... your arms grow heavy (lose)",
    2: "The Scroll Glooms... your grip weakens (lose)",
    3: "The Scroll Hastens... you are overpowered (lose)",
    4: "The Scroll Glows... you find a gap (win)",
    5: "The Scroll Shines... you push through (win)",
    6: "The Scroll Blazes... you break the shield (win)",
}

# Dragon Scroll changes stats for buff, for turn-based fight
DRAGON_SCROLL = {
    1: "The Scroll Ignites... your sword surges (win)",
    2: "The Scroll Radiates... ETHEREAL POWER!  (win)",
    3: "The Scroll Lights... light strikes armour (win)",
    4: "The Scroll Flickers... surge fades  (lose)",
    5: "The Scroll Dims... your strength wavers (lose)",
    6: "The Scroll Withers... nothing stirs (lose)",
}

#--GHOST_RIDDLES--------------------------------------------------------------#
# List of tuplles: (question: answer), randomly picks 3 for each game

RIDDLES = [
    ("I have cities but no houses, forests but no trees. What am I?", "MAP"),
    ("The more you take, the more you leave behind. What am I?", "FOOTSTEPS"),
    ("I speak without a mouth and hear without ears. What am I?", "ECHO"),
    ("What has keys but no locks?", "KEYBOARD"),
    ("I am not alive, but I grow. What am I?", "FIRE"),
    ("What can travel the world while staying in a corner?", "STAMP"),
]

#--QUEEN_DIALOGUE-------------------------------------------------------------#
# Night Queen's dialogue stored as list, garlbe_text() looop through each line

QUEEN_LINES = [
    "I am the Night Queen of this quiet dark land.",
    "There is no peace here though... ",
    "You will never understand me, its my curse.",
]

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#
#--HELPER_FUNCTIONS-----------------------------------------------------------#
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#
# Functions that can be called anywhere in the code, to reduce code duplication
# and make processes that returns results

def clear():
    """"Clears the terminal/console screen/command line interface(CLI)."""
    os.system("cls" if os.name == "nt" else "clear")    # clears console/terminal (Windows or Mac/Linux)

def typed_input(prompt, options, hide_options=False):
    """
    Will keep prompting the user for input until a valid option is entered.

    Parameters:
        prompt (str): The text displayed to the user asking for input.
        options (list): A list of valid string choices the user is allowed to type.
        hide_options (bool, optional): If True, hides the list of choices
        when user types an invalid answer. Defaults to False.

    Returns:
        (str): The validated, lowercase string that the user typed.
    """
    lower = [v.lower() for v in options]        # make all options lowercase
    while True:                                 # keep asking until valid
        choice = input(prompt).strip().lower()  # get input, clean it
        if choice in lower:                     # is it one of the options?
            return choice                       # yes: return it, exit loop
        if hide_options:
            print("  Try again")
        else:
            print(f"  Try: {', '.join(options)}") # no: show valid options

def print_slow(text, delay=None):
    """
    Print text character by character with a short delay.
    Parameters:
        text (str): The text to display.
        delay (float): Time in seconds between characters.
                       Uses default if not provided.

    """
    if delay is None:
        delay = SLOW_PRINT_DELAY           # uses global default so all text prints at same speed

    for char in text:                      # char for individual characters it prints
        print(char, end='', flush=True)    # prints character, no newline
        time.sleep(delay)                  # delays time before printing next character
    print()                                # moves to new line after looping

def show_stats():
    """Display player stats."""
    W = 48  # inner width between the two | borders

    divider(1)
    print(f"|{player_name:^{W}}|")           # centered name
    print(f"|{'':^{W}}|")                     # empty line
    print(f"|{'Hearts:  ' + str(hearts) + '/3':^{W}}|")
    print(f"|{'Sword:   ' + str(attack_strength):^{W}}|")
    print(f"|{'Berries: ' + str(berries):^{W}}|")
    if fantasii_pets > 0:
        print(f"|{'Purr Buff: ' + str(fantasii_pets):^{W}}|")
    if Fantasii == True:
        print(f"|{'Companion: Fantasii =^w^=':^{W}}|")
    divider(2)
    print()

def options_menu():
    """Show utility/options menu: Pet, Eat, Stats, Inventory, Walk Forward."""
    while True:
        print("  [P] Pet  [E] Eat  [S] Stats [I] Inventory [W] Walk forward")
        choice = typed_input("  What do you do? --<3-->> ", ["p", "e", "s", "i", "w"])
        if choice == "p":
            pet_fantasii()
        elif choice == "e":
            eat_berry()
        elif choice == "s":
            show_stats()
        elif choice == "i":
            view_inventory()
        elif choice == "w":
            break               # exit menu loop, returns to scene that called it

def view_inventory():
    """Display the player's collected items and if empty."""
    if inventory:
        print("  Your inventory:", ", ".join(inventory))
    else:
        print("Your inventory is empty.")

def pet_fantasii(): #meow
    """Pet's Fantasii. Cycles through 8 cat responses."""
    global fantasii_pets
    fantasii_pets += 1
    responses = [
        "  *meow* :3\n",
        "  *purrrr* =^w^=\n",
        "  *meow meow purrrr* >.<",
        "  *meeeeow* Fantasii rolls over belly up.\n",
        "  *mlem* sticks tongue out :P\n",
        "  *purrrrrrrrrrrr* \n",
        "  *meow meow meow meow meow meow :3\n",
        "  *meOW* Fantasii head butts your hand.\n",
    ]
    index = (fantasii_pets - 1) % len(responses)
    print(responses[index])

def eat_berry():
    """Eats a berry to restore to maximum 3 hearts."""
    global hearts, berries, berries_eaten
    if berries <= 0:
        print("  You have no berries left ")
        return                                  # nothing to eat and returns
    if hearts >= 3:
        print("  Heart is already restored ")
        return                                  # max health and returns
    berries -= 1
    hearts = 3
    berries_eaten += 1
    print(f"  You eat a berry. Hearts: {hearts}/3 Berries: {berries}")

def offer_berries(name):
    """
    Offers berry to named character, and tracks for secret ending.

    Parameters:
        name (str): The name of the character receiving the berry.
    """

    global berries
    if berries <= 0:
        print("  You have no berries to offer ")
        return
    choice = typed_input("  Offer berries? --<3-->> ", ["give berries", "walk forward"])
    if choice == "give berries":
        berries -= 1
        berries_offered_to.append(name)
        print(f"  You offer a berry to {name}. ")
        print(f"  Berries: {berries}")
    elif choice == "walk forward":
        print("  You walk forward. ")

def roll_dice():
    """Fantasii rolls the Dice of Destiny. Returns 1-6."""
    global dice_rolls
    dice_rolls += 1
    result = random.randint(1, 6) # 1-6 matches with the scroll dictionary keys
    print_slow(f"\n  Fantasii drops the dice... {result} glows!")
    return result

def garble_text(text):
    """
    Shuffle characters in each word and returns garbled text.

    Parameters:
        text (str): The original string of text to be scrambled.

    Returns:
        (str): The fully scrambled text.

    """
    words = text.split()
    garbled = []
    for word in words:
        letters = list(word)
        random.shuffle(letters)             # randomises letters
        garbled.append("".join(letters))    # rejoins garbled words as strings
    return " ".join(garbled)                # Citaiton_10

def crow_rescue():
    """
    Restores heart by eating a berry or crow rescues and give berries.
    """
    global hearts, berries, crow_rescues, berries_acquired, berries_eaten
    if berries > 0:
        berries -= 1
        hearts = 3
        berries_eaten += 1
        print("  You eat a berry. Hearts is restored.")
    else:
        crow_rescues += 1               # when no berries left, crow saves player
        print("  Crows appear and fly to you")
        print("  they drop berries and fly away.")
        berries += 3                    # crow gives 3 berries
        berries_acquired += 3           # eats a berry
        berries -= 1
        berries_eaten += 1
        hearts = 3
        print(f"  Heart restored. Berries: {berries}")

def lose_hearts(amount):
    """
    Lose hearts stats by amount and triggers a crow_rescue() if at 0.
    Does not show or go below 0.

    Parameters:
        amount(int): The number of hearts the player will lose.
    """
    global hearts, berries
    hearts = max(0, hearts - amount)       # so hearts don't go negative
    print("|" + f"You lose Hearts: {hearts}/3".center(48) + "|")
    if hearts <= 0:
        crow_rescue()                      # automatic rescue

def divider(lines):
    """ """
    if lines == 1:
        print("|-.,_____..¬¬¬¬¬¬=======<3=======¬¬¬¬¬¬.._____,.-|")
        print("|                                                |")
    elif lines == 2:
        print("|                                                |")
        print("|-.,_____..¬¬¬¬¬¬=======<3=======¬¬¬¬¬¬.._____,.-|")
    elif lines == 3:
        print("|                                                |")


#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|##########
#--MAIN_GAME_CONTENT----------------------------------------------------------## START #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|##########

#-----------------------------------------------------------------------------#
#--TRANSITION_ANIMATION-------------------------------------------------------#
#-----------------------------------------------------------------------------#
# For a classic, old text-base adventure game feel.
# Like running a game on a retro device outputted on a screen
# Using loops to print line by line delayed by time.sleep (time module)

def transition_1():
    """Opening transition animation with HEARTS title."""
    #Frame_1
    clear()
    for line in ["#"*60, "#"*60,"#" * 25 + "  HEARTS  " + "#" * 25, "#"*60, "#"*60]:
        print(line)
        time.sleep(0.25)

    time.sleep(1)
    #Frame_2
    clear()
    for line in ["#"*60, "#"*60, "#"*60, "#"*60, "#"*60]:
        print(line)
        time.sleep(0.25)
    return hearts_meow

#-----------------------------------------------------------------------------#
#--TITLE_SCREEN---------------------------------------------------------------#
#-----------------------------------------------------------------------------#

def hearts_meow():
    """Title screen, takes player's name and shows intructions and commands."""
    global player_name
    clear()
    time.sleep(0.3)

    divider(1)
    print_slow("|" + "Hearts <3".center(48) + "|")
    divider(3)
    time.sleep(0.3)
    input("""|           Press enter to start game...         |
|                                                |
|-.,_____..¬¬¬¬¬¬=======<3=======¬¬¬¬¬¬.._____,.-|""")

    clear()
    divider(1)
    print_slow("|                Enter your name:                |")
    divider(2)
    player_name = input("\n--<3-->> ")
    print()
    time.sleep(0.3)

    clear()
    print()
    print_slow(f"\n  Welcome {player_name} to Hearts   =^w^= <3 \n\n")
    time.sleep(2)
    print("  [ Commands: type out commands : eat berries or P ] \n\n")
    print("  [ Objective: Get up, head to the Night Castle, follow your destiny... ] \n\n")
    input("  Press enter to to play... > ")
    time.sleep(0.3)

    return node_1_wake

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ACT_1_WAKE-----------------------------------------------------------------#  ONE  #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_1_wake():
    """Act 1 scene wake up on grass, receive berries, restore hearts"""
    global hearts, berries, berries_acquired, berries_eaten
    clear()
########
    divider(1)
    print_slow("|               You open your eyes...            |")
    print_slow("|      Lying on grass, with trees all around.    |  ")
    print("|            Rusty sword by your side            |")
    print("|    Crows circle you above, and drop berries    |  ")
    print("|    They are curious of you... they fly away.   |  ")
    divider(2)
    print()

    berries = 3
    berries_acquired += 3
    print_slow(f"  Gain Berries: {berries}")
    print()
    stand_count = 0
    crow_special = False
    while True:
        choice = typed_input("  What do you do? --<3-->> ",
                             ["eat berries", "stand", "rest"])
        if choice == "eat berries":
            berries -= 1
            hearts = 3
            berries_eaten += 1
            print("\n  You eat a berry")
            print(f"  Heart is restored: {hearts}/3\n")
            input("  Press enter to continue... > ")
            time.sleep(1)
            break

        elif choice == "stand":
            stand_count += 1
            print("\n  You can't stand, you are weak\n")
            if stand_count >= 3 and not crow_special:
                crow_special = True
                clear()
                divider(1)

                # (c)raw string  x_x
                print_slow("|        You close your eyes and rest...         |")
                print_slow("|                       ...                      |")
                print("|     You feel something on your arm. *Caws*     |")
                print("|            You open your eyes a crow.          |")
                print(r"|                      <0\_                      |")
                print(r"|                       \ \\                     |")
                print(r"|                     *  ||                      |")
                print("|    Crows surround you and drop more berries,   |")
                print("|                  and fly away.                 |" )
                divider(2)
                print()
                print_slow("\n  Gain more Berries: 3\n")
                berries = 6
        elif choice == "rest":
            if not crow_special:
                crow_special = True
                clear()
                divider(1)

                # (c)raw string  x_x
                print_slow("|        You close your eyes and rest...         |")
                print_slow("|                       ...                      |")
                print("|     You feel something on your arm. *Caws*     |")
                print("|            You open your eyes a crow.          |")
                print(r"|                      <0\_                      |")
                print(r"|                       \ \\                     |")
                print(r"|                     *  ||                      |")
                print("|    Crows surround you and drop more berries,   |")
                print("|                  and fly away.                 |" )
                divider(2)
                print_slow("\n  Gain more Berries: 3\n")
                berries = 6
                berries_acquired += 3
            else:
                print("\n  You rest for a moment. \n")

    print()
    clear()
    show_stats()
    print("\n  You hear noise towards the path ahead ")
    typed_input("  What do you do? --<3-->> ", ["walk forward"])
    time.sleep(1)
    return node_2_fantasii

def node_2_fantasii():
    """Act 1 scene: Introduced to Fantasii the cat, get Dice and Scroll Destiny"""
    global Fantasii, berries
    clear()
    divider(1)
    print_slow("|" + "Tree ahead, movement in the branches".center(48) + "|")
    print_slow("|" + "You hear weak meows...".center(48) + "|")
    divider(2)
    choice = typed_input("\n  What do you do? --<3-->> ", ["save cat", "wait"])
    time.sleep(2)

    if choice == "save cat":
        clear()
        divider(1)
        print_slow("|" + "You climb the tree and gently grab the cat".center(48) + "|")
        print_slow("|" + "You bring it down safely in your arms".center(48) + "|")
        print("|" + "mew".center(48) + "|")
        divider(2)
        input("\n  Press enter to continue... > ")
        time.sleep(1)

    elif choice == "wait":
        clear()
        divider(1)
        print_slow("|" + "The cat sees you and drops".center(48) + "|")
        print_slow("|" + "meeeeeeeeoooOoOwww".center(48) + "|")
        print("|" + "You catch the cat!".center(48) + "|")
        divider(2)
        input("\n  Press enter to continue... > ")
        time.sleep(1)

    clear()
    divider(1)
    print_slow("|" + "The cat has a Dice in its mouth".center(48) + "|")
    print_slow("|" + "and a Scroll on its back attached".center(48) + "|")
    print("|" + "You unfurl the Scroll and read...".center(48) + "|")
    print_slow("|" + "Fantasii the Cat!".center(48) + "|")
    print_slow("|" + "Bearer of the ".center(48) + "|")
    divider(3)
    print("|" + "Scroll of Destiny!".center(48) + "|")
    print("|" + "and".center(48) + "|")
    print("|" + "Dice of Destiny!".center(48) + "|")
    divider(2)
    berries -= 1
    print_slow("\n  You feed weak Fantasii a berry")
    print(f"  Berries: {berries}")
    input("\n  Press enter to continue... > ")
    time.sleep(1)

    clear()
    divider(1)
    print_slow("|" + "Fantasii is restored!!!".center(48) + "|")
    print_slow("|" + "MEOW :3".center(48) + "|")
    divider(2)

    choice = typed_input("\n  What do you do? --<3-->> ", ["pet cat", "walk forward"])
    if choice == "pet cat":
        pet_fantasii()
        print_slow("\n  Fantasii follows you.")
    elif choice == "walk forward":
        print_slow("\n  Fantasii follows you.")
    Fantasii = True         # Fantasii now follows player for rest of game :3
    options_menu()
    input("\n  Press enter to continue... > ")
    time.sleep(1)

    clear()
    divider(1)
    print_slow("|" + "A figure with a long sword stands".center(48) + "|")
    print_slow("|" + "on the path ahead.".center(48) + "|")
    print_slow("|" + "You and Fantasii walk forward.".center(48) + "|")
    divider(2)
    input("\n  Press enter to continue... > ")
    time.sleep(1)
    return node_3_sword_warrior

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ACT_2_THE_SWORD_WARRIOR----------------------------------------------------## TWO ##
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_3_sword_warrior():
    """Act 2 scene: The Sword Warrior fight, get sword, chess note, and map."""
    global attack_strength

    clear()
    divider(1)
    print_slow("|" + "The Sword Warrior:".center(48) + "|")
    print_slow("|" + "You there! you are blocking my path".center(48) + "|")
    print("|" + "You must fight me!!".center(48) + "|")
    divider(2)
    print()
    options_menu()

    clear()
    divider(1)
    print_slow("|" + "Fantasii drops The Dice of Destiny!".center(48) + "|")
    print_slow("|" + "and starts to roll...".center(48) + "|")
    print("|" + "The Scroll of Destiny unfurls...".center(48) + "|")
    divider(2)

    result = roll_dice()

    input("\n  Press enter to continue... > ")
    time.sleep(1)

    clear()
    scroll_results.append(("The Sword Warrior", result))
    divider(1)
    print_slow("|" + SWORD_SCROLL[result].center(48) + "|")
    divider(3)
    if result <= 3:
        lose_hearts(1)
        print_slow("|" + "The Sword Warrior bests in you battle.".center(48) + "|")
    if result >= 4:
        print_slow("|" + "You best The Sword Warrior in battle.".center(48) + "|")

    warriors_faced.append("The Sword Warrior")
    divider(3)
    print("|" + "The battle ends.".center(48) + "|")
    divider(3)
    print("|" + "The Sword Warrior:".center(48) + "|")
    print("|" + "You have strength Warrior!".center(48) + "|")
    print("|" + "Take my sword...".center(48) + "|")
    attack_strength = 4                     # upgraded player's sword 1 to 4
    print("|" + f"Sword: {attack_strength}".center(48) + "|")
    divider(2)

    print()
    offer_berries("The Sword Warrior")

    divider(1)
    print_slow("|" + "Sword Warrior:".center(48) + "|")
    print_slow("|" + "Take this note.".center(48) + "|")
    divider(3)
    print("|" + "The note has chess moves and a torn map".center(48) + "|")
    print("|" + "E4 > QH5".center(48) + "|")
    print("|" + "*Torn Map*".center(48) + "|")
    divider(3)
    print("|" + "You obtain the note in inventory".center(48) + "|")
    print("|" + "The Sword Warrior leaves".center(48) + "|")
    inventory.append("E4 > QH5")            # chess moves for later act
    inventory.append("Torn Map")            # for secret ending map
    divider(2)
    options_menu()

    clear()
    divider(1)
    print_slow("|" + "You see two paths ahead...".center(48) + "|")
    divider(2)
    input("\n  Press enter to continue... > ")
    time.sleep(1)

    return node_4_left_or_right

def node_4_left_or_right():
    """Act 2 scene: Path splits left or right, Fantasii chooses opposite path."""
    global cat_went_right

    clear()
    divider(1)
    print_slow("|" + "Two paths ahead of you".center(48) + "|")
    print_slow("|" + "Left and right.".center(48) + "|")
    print("|" + "Fantasii meows looking at you.".center(48) + "|")
    divider(2)
    choice = typed_input("\n  What do you do? --<3-->> ", ["left", "right"])
    if choice == "left":
        cat_went_right = True
        clear()
        divider(1)
        print_slow("|" + "You walk to the Left path".center(48) + "|")
        print_slow("|" + "Fantasii runs to the Right path".center(48) + "|")
        print("|" + "You follow Fantasii...".center(48) + "|")
        print("|" + "MEEEOOOoooowwww ".center(48) + "|")
        divider(2)

    elif choice == "right":
        cat_went_right = False
        clear()
        divider(1)
        print_slow("|" + "You walk to the Right path".center(48) + "|")
        print_slow("|" + "Fantasii runs to the Left path".center(48) + "|")
        print("|" + "You follow Fantasii...".center(48) + "|")
        print("|" + "MEEEOOOoooowwww ".center(48) + "|")
        divider(2)

    input("\n  Press enter to continue... > ")
    time.sleep(1)
    # cat goes opposite direction, determines which Act_3 warrior is first
    return node_5_ghost if cat_went_right else node_6_shield_warrior

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ACT_3_THE_GHOST_THE_SHIELD_WARRIOR_THE_CHESS_WARRIOR-----------------------# THREE #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_5_ghost():
    """Act 3 scene: The Ghost riddles, get gesture 'sunrise'."""
    clear()
    divider(1)
    print_slow("|" + "Something appears on your path...".center(48) + "|")
    print_slow("|" + "The Ghost glowing dimly...".center(48) + "|")
    print("|" + "The Ghost:".center(48) + "|")
    print("|" + "Answer my Riddles Warrior...".center(48) + "|")
    divider(3)
    print("|" + "*mew* Fantasii hides behind you".center(48) + "|")
    divider(2)
    print()
    options_menu()

    riddle = random.sample(RIDDLES, 3)    # picks 3 random riddles from full list
    correct_answer = 0

    clear()
    for question, answer in riddle:    # unpacks tuple, each riddle (question: answer)
        divider(1)
        print_slow("|" + "The Ghost asks:".center(48) + "|")
        divider(2)
        print(f"\n  '{question}'")
        player_answer = input("\n  --<3-->> ").strip().upper()
        if player_answer == answer:
            correct_answer += 1
            divider(1)
            print_slow("|" + "The Ghost: Correct".center(48) + "|")
            divider(2)
            break
        else:
            divider(1)
            print_slow("|" + f"Ghost: Wrong, the answer was: {answer}".center(48) + "|")
            divider(2)
        input("\n  Press enter to continue... > ")
        time.sleep(1)

    if correct_answer > 0:
        print()
        divider(1)
        print_slow("|" + "Ghost: You have the wisdom within you".center(48) + "|")
        divider(2)

    else:
        print()
        divider(1)
        print_slow("|" + "Ghost: You lack wisdom, but you have courage...".center(48) + "|")
        divider(2)
    warriors_faced.append("The Ghost")

    print()
    offer_berries("The Ghost")
    print()
    input("  Press enter to continue... > ")
    time.sleep(1)

    clear()
    divider(1)
    print_slow("|" + '"In music, the lowest note of a scale is the'.center(48) + "|")
    print_slow("|" + "the keynote and gives its name to the scale".center(48) + "|")
    print_slow("|" + "or key itself. Hence the phrases in key or".center(48) + "|")
    print_slow("|" + "out of key meaning in or out of harmony with.".center(48) + "|")
    print_slow("|" + "My key to you, a gesture...".center(48) + "|")
    divider(2)
    input("  ...")

    clear()
    divider(1)
    inventory.append("Sunrise")                # gesture key needed for Night Queen later
    print_slow("|" + '"...sunrise..."'.center(48) + "|")
    divider(2)

    print("\n  (Gain the gesture in your inventory)")
    print()
    input("  ...")

    divider(1)
    print_slow("|" + "Suddenly thunder roars, You turn around".center(48) + "|")
    print_slow("|" + "violent noise above The Night Castle ahead".center(48) + "|")
    divider(3)
    print("|" + "You turn to the ghost, she dissapeared".center(48) + "|")
    print("|" + "Fantasii with a confused look: meow?".center(48) + "|")
    print("|" + "You walk to the next path...".center(48) + "|")
    divider(2)

    print()
    input("  Press enter to continue... > ")
    time.sleep(1)

    # continues to next warrior based on which taken before
    return node_6_shield_warrior if cat_went_right else node_7_chess_warrior

def node_6_shield_warrior():
    """Act 3 scene: The Shield Warrior, get fire armour."""
    clear()
    divider(1)
    print_slow("|" + "A warrior with a huge shield".center(48) + "|")
    print_slow("|" + "stands in front of you.".center(48) + "|")
    print("|" + "The Shield Warrior:".center(48) + "|")
    print("|" + "You SHALL not pass!".center(48) + "|") # LOTR?
    divider(3)
    print("|" + "Battle ensues...".center(48) + "|")
    divider(2)
    print()
    options_menu()

    clear()
    divider(1)
    print_slow("|" + "Fantasii drops The Dice of Destiny!".center(48) + "|")
    print_slow("|" + "and starts to roll...".center(48) + "|")
    print("|" + "The Scroll of Destiny unfurls...".center(48) + "|")
    divider(2)

    result = roll_dice()

    input("\n  Press enter to continue... > ")
    time.sleep(1)

    clear()
    scroll_results.append(("The Shield Warrior", result))
    divider(1)
    print_slow("|" + SHIELD_SCROLL[result].center(48) + "|")
    divider(3)
    if result <= 3:
        lose_hearts(1)
        print_slow("|" + "The Shield Warrior blocks all your attacks".center(48) + "|")
        print_slow("|" + "and bests you in battle.".center(48) + "|")
    else:
        print_slow("|" + "You break through the".center(48) + "|")
        print_slow("|" + "Slavinn Shield!".center(48) + "|")
        print("|" + "and best The Shield Warrior in battle.".center(48) + "|")

    warriors_faced.append("The Shield Warrior")
    divider(3)
    print("|" + "The battle ends.".center(48) + "|")
    divider(3)
    print("|" + "The Shield Warrior:".center(48) + "|")
    print("|" + "You have worthiness Warrior!".center(48) + "|")
    print("|" + "Take this Fire Armour...".center(48) + "|")
    inventory.append("Fire Armour")
    divider(2)

    print("\n  Fire Armour obtained in the inventory\n")
    offer_berries("The Shield Warrior")

    print("\n  You and Fantasii are let past towards The Night Castle\n")
    input("  Press enter to continue... > ")
    time.sleep(1)
    # continues to next warrior based on which taken before
    return node_7_chess_warrior if cat_went_right else node_5_ghost

def node_7_chess_warrior():
    """Act 3 scene: The Chess Warrior, with puzzle, get Sword of Destiny in cave."""
    global attack_strength

    clear()
    divider(1)
    print_slow("|" + "You almost reach entrance of The Night Castle".center(48) + "|")
    print_slow("|" + "Everything is dark and hard to see...".center(48) + "|")
    divider(3)
    print("|" + "Then you see a faint glowing lamp ahead.".center(48) + "|")
    print("|" + "A Warrior, with a Chess Board and a Cube.".center(48) + "|")
    divider(3)
    print("|" + "Chess Warrior:".center(48) + "|")
    print("|" + "Warrior... do you have the whits about you?".center(48) + "|")
    print("|" + "Chess or Rubiks Cube?".center(48) + "|")
    divider(3)
    print("|" + "Fantasii rolls The Dice of Destiny...".center(48) + "|")
    print("|" + "and proceeds to chase and catch the dice...".center(48) + "|")
    print("|" + "Fantasii plays and leaves.".center(48) + "|")
    divider(2)

    choice = typed_input("\n  Chess or Rubiks Cube? --<3-->> ", ["chess", "rubiks"])
    if choice == "chess":
        clear()
        divider(1)
        print_slow("|" + "Chess Warrior: You play white, your move...".center(48) + "|")
        divider(3)
    elif choice == "rubiks":
        divider(1)
        print_slow("|" + "Chess Warrior: Rubiks Cube is broken.".center(48) + "|")
        print_slow("|" + "...you look at the Chess board instead".center(48) + "|")
        print("|" + "Chess match begins.".center(48) + "|")
        divider(3)

    for line in [
        " 8 |R_K_B_Q_K_B_K_R|",
        " 7 |P_P_P_P_P_P_P_P|",
        " 6 | _ _ _ _ _ _ _ |",
        " 5 | _ _ _ _ _ _ _ |",
        " 4 | _ _ _ _ _ _ _ |",
        " 3 | _ _ _ _ _ _ _ |",
        " 2 |P_P_P_P_P_P_P_P|",
        " 1 |R_K_B_Q_K_B_K_R|",
        "    A B C D E F G H"
    ]:
        print("|" + line.center(48) + "|")
    divider(2)

    while True:
        # hide_options: player must remember chess moves from the note in inventory
        choice2 = typed_input("\n  Enter chess move or options --<3-->> ", ["options", "e4"],hide_options=True)
        if choice2 == "options":
            options_menu()
        else:
            break

    clear()
    divider(1)
    for line in [
        " 8 |R_K_B_Q_K_B_K_R|",
        " 7 |P_P_P_P_P_P_P_P|",
        " 6 | _ _ _ _ _ _ _ |",
        " 5 | _ _ _ _ _ _ _ |",
        " 4 | _ _ _ _ _ _ _ |",
        " 3 | _ _ _ _P_ _ _ |",
        " 2 |P_P_P_P_ _P_P_P|",
        " 1 |R_K_B_Q_K_B_K_R|",
        "    A B C D E F G H"
    ]:
        print("|" + line.center(48) + "|")
    divider(3)
    print_slow("|" + "Chess Warrior: make your next move.".center(48) + "|")
    divider(2)

    while True:
        choice3 = typed_input("\n  Enter chess move or options --<3-->> ", ["options", "qh5"],hide_options=True)
        if choice3 == "options":
            options_menu()
        else:
            break

    clear()
    divider(1)
    for line in [
        " 8 |R_K_B_Q_K_B_K_R|",
        " 7 |P_P_P_P_P_ _P_P|",
        " 6 | _ _ _ _ _P_ _ |",
        " 5 | _ _ _ _ _ _ _Q|",
        " 4 | _ _ _ _ _ _ _ |",
        " 3 | _ _ _ _P_ _ _ |",
        " 2 |P_P_P_P_ _P_P_P|",
        " 1 |R_K_B_ _K_B_K_R|",
        "    A B C D E F G H"
    ]:
        print("|" + line.center(48) + "|")

    divider(3)
    print_slow("|" + "Checkmate! The Chess Warrior is impressed.".center(48) + "|")
    divider(2)
    warriors_faced.append("The Chess Warrior")

    print()
    offer_berries("The Chess Warrior")
    print()

    divider(1)
    print_slow("|" + "The Chess Warrior takes chess pieces and leaves".center(48) + "|")
    divider(3)
    print("|" + "A cave reveals itself...a glow eminates".center(48) + "|")
    print("|" + "You walk into the cave...".center(48) + "|")
    divider(3)
    print("|" + "The Sword of Destiny on the ground glows bright.".center(48) + "|")
    divider(2)
    attack_strength = 10
    inventory.append("Sword of Destiny")    # Sword of Destiny: major upgrade from 4 to 10
    print("\n  The Sword of Destiny obtained!")

    input("  Press enter to continue... > ")
    time.sleep(1)

    clear()
    divider(1)
    print_slow("|" + "You exit the cave, Fantasii waiting for you...".center(48) + "|")
    print_slow("|" + "MEOWWWW! =^w^=".center(48) + "|") # surprised meow
    divider(3)
    print("|" + "You head together to The Night Castle.".center(48) + "|")
    divider(2)

    print()
    input("  Press enter to continue... > ")
    time.sleep(1)
    return node_8_night_castle

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ACT_4_THE_NIGHT_QUEEN------------------------------------------------------## FOUR #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_8_night_castle():
    """Act 4 scene: Enter Night Castle, recieving berries from crows."""
    global berries, berries_acquired

    clear()
    divider(1)
    print_slow("|" + "You enter the castle. Cathedral walls rise.".center(48) + "|")
    print_slow("|" + "Your Sword glows and lights the path forward.".center(48) + "|")
    print("|" + "Crows line the walls... Silent.".center(48) + "|")
    divider(3)
    print("|" + "One flies down and drops berries.".center(48) + "|")
    divider(2)
    print()
    berries += 3                # crows give berries before the final fights
    berries_acquired += 3
    print(f"\n  Berries: {berries}")
    options_menu()
    print()
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "You walk towards the throne.".center(48) + "|")
    print_slow("|" + "The Night Queen sits by the window.".center(48) + "|")
    print_slow("|" + "Not on the throne.".center(48) + "|")
    print("|" + "She stares into the darkness...".center(48) + "|")
    divider(2)

    input("\n  Press enter to continue... > ")
    time.sleep(1)
    return node_9_night_queen

def node_9_night_queen():
    """
    Act 4 scene: The Night Queen, garbled speech, type gesture 'sunrise'
    restore the Queen, fight alongside.
    """
    global queen_restored, queen_fights, berries

    clear()
    divider(1)
    print_slow("|" + "The Night Queen speaks".center(48) + "|")
    print_slow("|" + "with a calm soft voice...".center(48) + "|")
    divider(3)
    for line in QUEEN_LINES:
        # Night Queen's speech is garbled until player uses gesture
        print("|" + f'"{garble_text(line)}"'.center(48) + "|")

    divider(3)
    print_slow("|" + "You cannot understand her words.".center(48) + "|")
    divider(2)

    while True:
        print()
        choice = typed_input("Say gesture or options --<3-->> ", ["options", "sunrise"], hide_options=True)
        # player must remember gesture "sunrise" from ghost
        if choice == "options":
            options_menu()
        else:
            break

    if "Sunrise" in inventory:
        print()
        print_slow('  "sunrise"')
        print_slow("...")

        divider(1)
        print("|" + "The Queen's words become clear:".center(48) + "|")
        divider(3)
        for line in QUEEN_LINES:
            print_slow("|" + line.center(48) + "|")
        divider(2)
    else:
        print("  Her words remain garbled.")
    print()
    offer_berries("The Dawn Queen")
    if "The Dawn Queen" in berries_offered_to:
        queen_restored = True   # unlocks option for queen to fight alongside in dragon battle
        print("  The Night Queen is restored.")
    if queen_restored:
        divider(1)
        print_slow("|" + "Night Queen: The dragon is coming.".center(48) + "|")
        print_slow("|" + "Night Queen: Will you fight alongside me?".center(48) + "|")
        divider(2)
        print()
        choice_2 = typed_input("  Yes or No? --<3-->> ", ["yes", "no"])
        if choice_2 == "yes":
            queen_fights = True
            print("  The Queen nods. You fight together.")
        else:
            print("  You will face the dragon alone.")
    print()
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "The ceiling crashes down!".center(48) + "|")
    print_slow("|" + "The Dragon descends...".center(48) + "|")
    divider(2)

    print()
    input("  Press enter to continue... > ")
    time.sleep(1)
    return node_10_the_dragon

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ACT_5_THE_DRAGON-----------------------------------------------------------## FIVE #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_10_the_dragon():
    """
    Act 5: The Dragon Fight.
    Sequence:
        1. Darkness offer berry for secret ending
        2. Dragon awakens, and attacks first with fiire breath
        3. Fantasii rolls dice, scroll buffs attack_strength
        4. Fantasii attacks once (damage = times petted)
        5. Turn loop:
              player attacks or defends
              queen attacks every round if queen_fights
              dragon retaliates every round
        6. Dragon defeated returns next node_11
    """
    global hearts, berries, attack_strength
    clear()
    divider(1)
    print("|" + "#"*48 + "|")
    print("|" + "#"*48 + "|")
    print("|" + "#"*48 + "|")
    print("|" + "#"*48 + "|")
    print("|" + "#"*48 + "|")
    print("|" + "#"*48 + "|")
    divider(3)
    print_slow("|" + "(Everything turns dark... pitch black.)".center(48) + "|")
    divider(2)
    print()
    berries_choice = input("  --<3-->> ").strip().lower()
    # deliberate, player must "give berries" in the dark, no options will be shown
    time.sleep(1)

    if berries_choice == "give berries":     # ends fight sooner
        if berries > 0:
            berries -= 1
            berries_offered_to.append("The Dragon")
            clear()
            divider(1)
            print_slow("|" + "The dragon opens its eyes...".center(48) + "|")
            print_slow("|" + "It sees the berry in your hand...".center(48) + "|")
            print_slow("|" + "And gently takes it from you...".center(48) + "|")
            divider(2)
            time.sleep(1)
            return node_11_the_dragon_end
        else:
            print("  You have no berries to offer.")
            print_slow("  ...")
    else:
        print_slow("  ...")

    clear()
    divider(1)
    print_slow("|" + "The dragon opens its eyes...".center(48) + "|")
    print_slow("|" + "A dim, faint glow.".center(48) + "|")
    print("|" + "You look beside you.".center(48) + "|")
    print("|" + "The Queen's heart glows.".center(48) + "|")
    print("|" + "Fantasii and the Dice glow...".center(48) + "|")
    divider(2)
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "The dragon's eyes focus on you...".center(48) + "|")
    print_slow("|" + "It opens its mouth...".center(48) + "|")
    print_slow("|" + "A thunderous roar!".center(48) + "|")
    print("|" + "Flames erupt towards you!".center(48) + "|")
    divider(3)

    if "Fire Armour" in inventory:      # fire armour blocks dragon's fire breath
        print_slow("|" + "... you brace for impact.".center(48) + "|")
        print_slow("|" + "The dragon's eyes focus on you...".center(48) + "|")
        print("|" + "Your Fire Armour deflects it completely!".center(48) + "|")
        print("|" + "The Dragon stops, exhausted of its force.".center(48) + "|")
        print("|" + "A fear in its eyes..".center(48) + "|")
        divider(2)
    else:
        print_slow("|" + "The flame hits you hard....".center(48) + "|")
        print_slow("|" + "The heat trickles away your armour.".center(48) + "|")
        lose_hearts(2)

    print()
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "Fantasii drops The Dice of Destiny!".center(48) + "|")
    print_slow("|" + "and starts to roll...".center(48) + "|")
    print("|" + "The Scroll of Destiny unfurls...".center(48) + "|")
    divider(2)

    result = roll_dice()

    input("\n  Press enter to continue... > ")
    time.sleep(1)

    clear()
    scroll_results.append(("The Dragon", result))
    divider(1)
    print_slow("|" + DRAGON_SCROLL[result].center(48) + "|")
    divider(3)

    scroll_armour_crack = 0      # stored seperately, applied to armour before turn loop

    if result <= 2:
        attack_strength += 5
        print_slow("|" + "Your Sword surges with immense power!".center(48) + "|")
        print("|" + f"Sword: {attack_strength}".center(48) + "|")
    elif result == 3:
        scroll_armour_crack = 15
        print_slow("|" + "Your Sword Strikes a Light at The Dragon!".center(48) + "|")
        print("|" + "The Dragon loses 15 armour!".center(48) + "|")
    elif result <= 5:
        attack_strength += 1
        print_slow("|" + "Your Sword lights up... a faint strength.".center(48) + "|")
        print("|" + f"Sword: {attack_strength}".center(48) + "|")
    else:
        print_slow("|" + "The Scroll corrupts and becomes dark.".center(48) + "|")
    divider(3)

    dragon_armour = 60          # The Dragon's health
    dragon_armour -= scroll_armour_crack
    dragon_armour -= fantasii_pets           # Fantasii pets = total times player petted into damage!
    dragon_armour = max(0, dragon_armour)    # Dragon's armour doesn't go negative

    print("|" + "Fantasii pounces and jumps at the dragon.".center(48) + "|")
    print("|" + "(PURR BUFF) Paw slaps!".center(48) + "|")
    print("|" + f"  Fantasii dealt {fantasii_pets} damage!".center(48) + "|")
    print("|" + f"  Dragon armour: {dragon_armour}".center(48) + "|")
    divider(2)

    input("\n  Press enter to continue... >")

    if dragon_armour <= 0:
        warriors_faced.append("The Dragon")
        clear()
        divider(1)
        print_slow("|" + "Fantasii strikes down The Dragon!".center(48) + "|")
        print_slow("|" + "With all their might!".center(48) + "|")
        divider(2)
        time.sleep(1)
        return node_11_the_dragon_end

    clear()
    print("\n  Attack or Defend?")
    print()

    # Turn Loop Fight
    while dragon_armour > 0:     # fight continues until The Dragon's armour is at 0

        print(f"  Dragon armour: {dragon_armour}  |  Hearts: {hearts}/3  |  Berries: {berries}")
        choice = typed_input("  --<3-->> ", ["attack", "defend"])
        print()

        if choice == "attack": # attacking risks 2 heart damage from The Dragon
            damage = attack_strength
            dragon_armour -= damage
            dragon_armour = max(0, dragon_armour)
            print(f"  You deal {damage} damage!")
            print(f"  Dragon armour: {dragon_armour}")

        elif choice == "defend": # defends reduces risk, lose 1 heart damage from The Dragon
            print("  You hold the sword in front of you and brace!")
        print()

        if queen_fights and dragon_armour > 0:    # Night Queen attacks every round, accepted alliance :)
            queen_damage = random.randint(3, 6)   # Night Queen attacks deal 3-6 random damage per round
            dragon_armour -= queen_damage
            dragon_armour = max(0, dragon_armour)
            print("  The Night Queen strikes at the dragon")
            print(f"  Night Queen dealt {queen_damage} damage!")
            print(f"  Dragon armour: {dragon_armour}")
            print()

        if dragon_armour <= 0:    # when The Dragon's Armour goes 0, ends loop
            break

        if choice == "attack":
            print("  The Dragon swipes their dark claws at you!")
            lose_hearts(2)
        elif choice == "defend":
            print("  The Dragon throws their spiked tail at you!")
            print("  ... you defend with your Sword!")
            print("  you take some damage")
            lose_hearts(1)
        print()

    warriors_faced.append("The Dragon")

    clear()
    divider(1)
    print_slow("|" + "The Dragon roars painfully...".center(48) + "|")
    print_slow("|" + "Their energy becomes weak.".center(48) + "|")
    print_slow("|" + "It falls to the ground, everything shakes.".center(48) + "|")
    print("|" + "It closes its eyes...".center(48) + "|")
    divider(2)

    print()
    time.sleep(1)
    return node_11_the_dragon_end

def node_11_the_dragon_end():
    """
    Act 5 scene: The Dragon falls, restore the dragon, sunrises.
    The Night Queen is now The Dawn Queen.
    """
    global berries, berries_acquired, berries_eaten
    if "The Dragon" not in berries_offered_to: # another chance to offer berries after fight
        if berries > 0:
            divider(1)
            print("|" + "The dragon lies still...".center(48) + "|")
            divider(2)
            print()
            offer_berries("The Dragon")
        else:
            divider(1)
            print("|" + "The Queen kneels and offers a berry.".center(48) + "|")
            divider(2)
            berries_offered_to.append("The Dragon")

    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "The Dragon's dark armour starts to shed".center(48) + "|")
    print_slow("|" + "Gold light pierces through".center(48) + "|")
    print_slow("|" + "The never-ending night starts to fade".center(48) + "|")
    print("|" + "The Dragon looks at you and the Queen...".center(48) + "|")
    print("|" + "It looks to the sky and rises...".center(48) + "|")
    divider(2)
    print()
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "A sunrise ascends".center(48) + "|")
    print_slow("|" + "The land is restored".center(48) + "|")
    print_slow("|" + "Warmth and light returns".center(48) + "|")
    divider(3)

    print_slow("|" + "Crows of the castle flock in the air...".center(48) + "|")
    if hearts == 1 and berries == 0:   # if player is at 1 hearts, cows gives one last berry :))
        berries += 1
        berries_acquired += 1
        print_slow("|" + "They drop one more berry".center(48) + "|")
        divider(2)
        print()
        eat_berry()
        berries_eaten += 1
    print()
    divider(1)
    print_slow("|" + "...in unison they fly into the sky...".center(48) + "|")
    print_slow("|" + "...and turn into stars...".center(48) + "|")
    divider(2)

    if queen_restored:
        print()
        input("\n  Press enter to continue... > ")
        clear()
        divider(1)
        print_slow("|" + "The Dawnn Queen takes off her helmet.".center(48) + "|")
        print_slow("|" + "Red Autumn hair flows free.".center(48) + "|")
        print_slow("|" + "She walks out into the light.".center(48) + "|")
        print("|" + "The Night Queen is now The Dawn Queen.".center(48) + "|")
        divider(2)

    print()
    input("\n  Press enter to continue... > ")
    time.sleep(1)
    return node_12_rest

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--ENDING_REST----------------------------------------------------------------## END ##
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def node_12_rest():
    """Ending scene: Final rest with Fantasii. Win game"""
    clear()
    divider(1)
    print_slow("|" + "You lie on the ground looking at the stars".center(48) + "|")
    print_slow("|" + "Fantasii climbs on to your chest".center(48) + "|")
    print("|" + "and rests...".center(48) + "|")
    divider(3)
    print("|" + "<3".center(48) + "|")
    divider(3)
    print("|" + "Fantasii looks into your eyes, then closes them.".center(48) + "|")
    print("|" + "Pet Fantasii one more time?".center(48) + "|")
    divider(2)


    choice = typed_input("  --<3-->> ", ["pet cat", "rest"])
    print()
    if choice == "pet cat":
        pet_fantasii()
        print("  Fantasii starts purring ")
    elif choice == "rest":
        print("  Fantasii starts purring ")

    print()
    input("\n  Press enter to continue... > ")

    clear()
    divider(1)
    print_slow("|" + "You close your eyes...".center(48) + "|")
    print_slow("|" + "You rest with warmth in your heart".center(48) + "|")
    divider(3)
    print_slow("|" + f"The Hero Warrior! {player_name}".center(48) + "|")
    divider(2)
    time.sleep(1)
    print_slow("\n  YOU WIN!")

    print()
    # obligatory game soundtrack
    print_slow("  [Blue Foundation - Eyes On Fire] song starts playing...")

    time.sleep(2)
    input("\n  Press enter to continue... > ")
    time.sleep(1)
    return ending_stats

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#############
#--ENDING_AND_STATISTICS------------------------------------------------------# END STATS #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#############

def ending_stats():
    """
    Displays end of the game statistics. Secret ending check.
    Option to play again.
    """
    clear()
    divider(1)
    print_slow("|" + "FINAL STATISTICS".center(48) + "|")
    divider(3)
    print_slow("|" + f"The Hero Warrior: {player_name}".center(48) + "|")
    print_slow("|" + f"Times you pet Fantasii: {fantasii_pets}".center(48) + "|")
    print_slow("|" + f"Dice rolled: {dice_rolls}".center(48) + "|")
    print_slow("|" + f"Crow rescues: {crow_rescues}".center(48) + "|")
    print_slow("|" + f"Berries acquired: {berries_acquired}".center(48) + "|")
    print_slow("|" + f"Berries eaten: {berries_eaten}".center(48) + "|")
    print_slow("|" + f"Berries offered: {len(berries_offered_to)}/6".center(48) + "|")
    print_slow("|" + f"Queen restored: {queen_restored}".center(48) + "|")
    divider(2)

    print()
    print("  Warriors faced:                   Berries offered to:")
    max_len = max(len(warriors_faced), len(berries_offered_to))
    for i in range(max_len):
        w_faced = f"- {warriors_faced[i]}" if i < len(warriors_faced) else ""
        b_offered = f"- {berries_offered_to[i]}" if i < len(berries_offered_to) else ""
        print(f"  {w_faced:<32}  {b_offered}")

    print()
    print("  Scroll results:")
    for enemy, roll in scroll_results:
        if "Sword" in enemy:
            narrative = SWORD_SCROLL.get(roll, "")
        elif "Shield" in enemy:
            narrative = SHIELD_SCROLL.get(roll, "")
        elif "Dragon" in enemy:
            narrative = DRAGON_SCROLL.get(roll, "")
        else:
            narrative = ""
        print(f"  - {enemy.replace('The ', '')} : {roll} : {narrative}")
    print()

    secret_names = ["The Sword Warrior", "The Ghost",
                    "The Shield Warrior", "The Chess Warrior",
                    "The Dawn Queen", "The Dragon"]
    offered_count = 0
    for name in secret_names:
        if name in berries_offered_to:
            offered_count += 1

    if offered_count >= 6:
        divider(1)
        print_slow("|" + "SECRET ENDING UNLOCKED!".center(48) + "|")
        print_slow("|" + "Torn map has puzzled back together...".center(48) + "|")
        print_slow("|" + "A complete matrix.".center(48) + "|")
        divider(3)
        print_slow("|" + "You showed compassion to every soul you met.".center(48) + "|")
        print_slow("|" + "All hearts restored.".center(48) + "|")
        divider(2)
    else:
        missing = []
        for name in secret_names:
            if name not in berries_offered_to:
                missing.append(name)
        print("  Secret Ending: Not unlocked")  # all 6 offered = Secret Ending Unlocked
        print(f"  Berries offered to {offered_count}/6 warriors")
        print(f"  You missed: {', '.join(missing)}")

    print()
    print_slow(f"  Thank you for playing, {player_name}")
    print("       =^w^= <3 ")
    print()
    print("  Play again?")
    choice = typed_input("  --<3-->> ", ["play again", "end game"])

    if choice == "play again":
        return reset_game

    if choice == "end game":
        clear()
        print("\n  Fantasii: meow :3\n")
        return None

def reset_game():
    """Reset all global variables before game loop restarts."""
    global player_name, hearts, berries, attack_strength
    global fantasii_pets, cat_went_right, inventory, dice_rolls
    global crow_rescues, berries_offered_to, scroll_results
    global queen_restored, queen_fights, warriors_faced
    global berries_acquired, berries_eaten, Fantasii

    # all global variables reset to starting values for fresh start
    player_name = ""
    hearts = 1
    berries = 0
    attack_strength = 1
    fantasii_pets = 0
    cat_went_right = True
    Fantasii = False
    inventory = []
    dice_rolls = 0
    crow_rescues = 0
    warriors_faced = []
    berries_offered_to = []
    queen_restored = False
    queen_fights = False
    scroll_results = []
    berries_acquired = 0
    berries_eaten = 0

    return transition_1

#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########
#--MAIN_LOOP------------------------------------------------------------------## MAIN #
#\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/|\|/\|/|\|/|\|/|\|/|\|/|\|#########

def main():
    """Main game loop. Runs the engine of function chain, or story scenes."""
    current_node = transition_1 # first scene function maain() calls
    while current_node is not None: # loop ends when a scene returns None
        current_node = current_node() # calls current scene, stores next node/scene/function

if __name__ == "__main__":
    main()
