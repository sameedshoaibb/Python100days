""" Yalla Sameed """

#!/usr/bin/python3

# 1- Enumerate is a fucntion which correspond list in list

NAMES = ["Peter Parker", "Wilson"]
HEROES = ["Spider Man", "BatMan"]
UNIVERSE = ["Marvel", "Zoom"]
INDEX = None
NAME = None
for INDEX, NAME in enumerate(NAMES):
    print(INDEX, NAME)
    hero = HEROES[INDEX]
    Univers = UNIVERSE[INDEX]
print("{} is the Hero of {}. The production company is {}{}".format(NAME, hero, Univers, INDEX))





