import random
import os
import sys
#import math

#1. Make the text for pathes appear after redrawing, because otherwise it's two click each time to move
#2. Make sure that examining past 4 takes you back to number 3. Also only count examinations if examined, not if found.
#3. Don't show how much health a monster has if attack. Only show if it is high, mid, or low health. Make examining it actually useful.
#4. Remove items from map once used. remove monsters, too. Don't remove settings.
#5. Finish writing endings and whatever else is missing.
#6. Finally, make the story coherent.

# no seed implementation yet
# four things happen when move:
# 1. move down a path, nothing happens
# 2. find an item, good can be used instantly or stored, 'bad' always stored
# good:
# 2a. bandages heal you
# 2b. flowers explain the world
# 2c. photos explain you
# bad:
# 2a. knife adds to dmg
# 2b. gun adds to dmg, 5 uses
# 2c. shotgun adds to dmg, 2 uses
# 3.fight an enemy (stats = player stats under a logarithm)
# 3a. draw the scene
# 3b. text of how and what you meet
# 3c. options of fight, run, or use item
# 3d. enemy fights you
# 3e. repeat you choose, enemy fights until someone dies
# 3f. if you die, print text and end game
# 3g. if enemy dies, upgrade either health or dmg, then draw map
# 4. meet ally
# 4a. fight ally similar to enemy fight except at end you get ally's items in
# 4b. talk to ally, about their life and such
# 4c. help ally if dying, sacrifice items. get nothing in return
# need to create health/dmg stats and inventory for player
# need to create somewhere to store all text: each item text, each enemy text, each ally dialogue tree
# use file?


# create effect that can change player stats
# finds whether enemy, item, or ally
# rolls to find what enemy, item or ally it is
# finds the text for

def end_game(msg = "Some Error Occurred: Game Ended"):
    sys.exit(msg)


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') #clear system
        map = Map() #generate map
        player = Player(map)
        placeholder_for_game = game(map, player)
        if placeholder_for_game == "EXIT":
            end_game("   --The End!--   ")
        elif placeholder_for_game == "RESTART":
            continue
        else:
            end_game()


class Map:
    def __init__(self, seed="rand", dimensions=(60, 20), max_rc=10000): #seed type, row by column, max stored character data
        self.chunk_list = []
        self.chunk_length = 24
        self.chunk_height = 8
        if dimensions[0] < 3 or dimensions[1] < 3: #makes sure map isn't less than 3x3
            end_game("Map too small")
        self.biome_weights = {"City":     [5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0],
                 "Field":    [0, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 "Trains":   [0, 0, 0, 90,0, 0, 0,45, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "Tech":     [0, 2, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "Junkyard": [8, 9, 2, 2, 8, 8, 5, 0, 9, 0, 0, 9, 9, 9, 9, 0, 0, 9, 2, 9, 9, 1, 9, 9, 1],
                 "Swamp":    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 2, 0, 0, 0, 0, 0, 0],
                 "Firest":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                 "Forest":   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 9, 0, 0, 1, 0, 0],
                 "Army base":[0, 3, 0, 0, 0, 0, 15,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], }
        self.obj_list = ["_", " ", ".", "=", "|", "\\", "#", "-", ":", "?", "!", "@", "L", "^", "&", "*", "(", "+", "U", "P",
                    "[", "I", ",", ">", "X"]

        if seed == "rand":
            self.seed = self.gen_seed() #create a random seed (DOES NOTHING YET)
        else:
            self.seed = seed
        if not isinstance(self.seed, int) or len(str(self.seed)) != 4:  # seed is int and 4 parts
            end_game("Cannot generate map with given seed")
        if not (isinstance(dimensions[0], int) and isinstance(dimensions[1], int)): #dimensions are ints
            end_game("Invalid dimensions")
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.cur_rows = (0, self.height) #rows that will first show are from 0 till end of "map" height
        self.cur_cols = (0, self.width) #columns that will first show are from 0 till end of "map" height
        self.midx = (self.cur_cols[1] - self.cur_cols[0]) // 2 + self.cur_cols[0] #the middle x position
        self.midy = (self.cur_rows[1] - self.cur_rows[0]) // 2 + self.cur_rows[0] #the middle y position
        self.row_list = [] #history list of all rows. Makes moving back possible.
        self.rc_count = 0 #total char counter. Stops generating map once hits close to it.
        self.last_row = max_rc #last POSSIBLE row
        self.last_col = max_rc #last POSSIBLE column
        rows = create_range((0, self.height)) #quite literally 0,1,2,3... until height
        cols = create_range((0, self.width)) #idk why im creating a range tho
        self.first_gen_rows()

    def gen_seed(self): #THIS CHANGES NOTHING YET
        return random.randint(1000, 9999)


    def draw(self, player):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("   --Game--   ")
        draw_row_list = [r[:] for r in self.row_list]
        draw_row_list[player.pos_y][player.pos_x] = player.player
        for rn in create_range(self.cur_rows)[::-1]:
            print("|", sep="", end="")
            for cn in create_range(self.cur_cols):
                print(draw_row_list[rn][cn], sep="", end="")
            print("|")

    def biome_maker(self):
        biome = random.choice(list(self.biome_weights.keys()))
        if biome == "Junkyard":
            biome = random.choice(list(self.biome_weights.keys()))
        return biome

    def first_gen_rows(self):
        row_list = []
        starting = True
        for row in range(0, self.height, self.chunk_height):  # make each column of the rows
            for col in range(0, self.width, self.chunk_length):  # make each chunk of a column
                if not starting:
                    biome = self.biome_maker()
                else:
                    biome = "Field"
                    starting = False
                for chunk_row in range(row, row + self.chunk_height):  # make each row of a chunk
                    new_row = random.choices(self.obj_list, weights=self.biome_weights[biome],
                                             k=self.chunk_length)  # make one row of a chunk
                    if len(row_list) - 1 < chunk_row:
                        row_list.append([])
                    row_list[chunk_row].extend(new_row)
        self.row_list = row_list



    def gen_rows(self, gen_type, num):
        # takes in either a new column or row to generate
        # if the row or column exists, don't add. If it doesn't, make a chunk.
        if gen_type == "column":
            biome = self.biome_maker()
            if len(self.row_list[0]) < num + 1:  # if len == 1, then the index is 0. So length is +1 of number
                print(len(self.row_list[0]), num)
                for row_i in range(0, len(self.row_list)):
                    if row_i % self.chunk_height == 0 or row_i == 0:
                        biome = self.biome_maker()
                    new_row = random.choices(self.obj_list, weights=self.biome_weights[biome], k=self.chunk_length)
                    self.row_list[row_i].extend(new_row)
        elif gen_type == "row":
            if len(self.row_list) < num + 1:  # same here
                for row in range(len(self.row_list), len(self.row_list) + self.chunk_height,
                                 self.chunk_height):  # make each column of the rows
                    for col in range(0, self.width, self.chunk_length):  # make each chunk of a column
                        biome = self.biome_maker()
                        for chunk_row in range(row, row + self.chunk_height):  # make each row of a chunk
                            new_row = random.choices(self.obj_list, weights=self.biome_weights[biome],
                                                     k=self.chunk_length)  # make one row of a chunk
                            if len(self.row_list) - 1 < chunk_row:
                                self.row_list.append([])
                            self.row_list[chunk_row].extend(new_row)
        return self.row_list

    def update_rc_count(self):
        self.rc_count = len(self.row_list) * len(self.row_list[0])
        if self.rc_count >= 10000:
            self.last_row = len(self.row_list) - 1
            self.last_col = len(self.row_list[0]) - 1

    def CHECK_create(self):
        for row in self.row_list:
            for i in range(len(row)):
                print(row[i], sep="", end="")
            print()


class Item:
    thing_effects = {"medkit": ["heal", 15],
                     "pistol": ["damage", 20],
                     "shotgun": ["damage", 40],
                     "knife": ["damage", 10],
                     "bluebell flower": ["speed", 1],
                     "lily flower": ["percent_heal", 5],
                     "lion's tongue flower": ["strength", 2]}
    fight_items = ["knife", "shotgun", "pistol"]
    monster_stats = {"ant": [5, 10, ["none", 0]],
                          "cat": [20, 45, ["double", 0]],
                          "bug": [15, 10, ["steal", 0]],
                          "slime": [20, 80, ["heal", 3]]}
    ally_stats = {"Johnny": [10, 20, ["steal", 0]],
                  "Alicia": [10, 20, ["double", 0]],
                  "Dominique": [10, 20, ["heal", 10]],
                  "Ella": [10, 20, ["steal", 0]]}
    path_monsters = list(monster_stats.keys())
    path_monsters.append(None)
    path_stats = {"path": [path_monsters, [2,0,0,1,97]],
                  "road": [path_monsters, [2,2,2,2,92]]}
    room_items = {"train cabin": [["medkit", "knife", "suitcase", "hat", "bug"], [20,10,39,30, 1]],
                    "room": [["lily flower", "pistol", "picture frame", "food", "cat"],[20,10,39,30,1]],
                    "building": [["lily flower", "pistol", "phone","papers", "slime"],[20,10,39,30,1]]
                    }
    flower_effects = {"bluebell flower": ["speed", 1],
                     "lily flower": ["percent_heal", 5],
                     "lion's tongue flower": ["strength", 2]}

    def __init__(self, char, player):
        self.char = char
        self.player = player

        self.char_decode = {"_": "road",
                            " ": "path",
                            ".": "ant",
                            "=": "train cabin",
                            "|": "wall",
                            "\\": "leaning wall",
                            "#": "barbed wire",
                            "-": "train couple",
                            ":": "mech",
                            "?": "'you'",
                            "!": "ally",
                            "@": "engine coil",
                            "L": "gun",
                            "^": "pine tree",
                            "&": "ship cog",
                            "*": "flower",
                            "(": "water",
                            "+": "medkit",
                            "U": "slime",
                            "P": "tree",
                            "[": "room",
                            "I": "building",
                            ",": "bug",
                            ">": "cat",
                            "X": "grave"}
        self.name = self.char_decode[self.char]
        if self.name == "flower":
            self.name = random.choice(list(Item.flower_effects.keys()))
        elif self.name == "gun":
            self.name = random.choice(["shotgun", "pistol"])
        elif self.name == "ally":
            self.name = random.choice(list(Item.ally_stats.keys()))

    @classmethod
    def dialogue_effect(cls, item_name):  # RENAME
        lookup = item_name
        with open("text", "r") as text_f:
            started = False
            for _, line in enumerate(text_f, 0):
                stripped_line = line.strip('\n')
                if lookup == stripped_line:
                    started = True
                elif started:
                    if line == "\n":
                        break
                    else:
                        print(stripped_line)
        if started == False:
            print("NOTHING FOUND FOR:", lookup)
            return False

    @classmethod
    def inv_effect(cls, player, item_name):
        result = None
        item_type = Item.thing_effects[item_name][0]
        item_amount = Item.thing_effects[item_name][1]
        if item_type == "heal":
            new_health = item_amount + player.health
            if new_health > player.max_health:
                new_health = player.max_health
            print("Healed for " + str(new_health - player.health))
            player.health = new_health
            print("Health:", player.health)
        elif item_type == "damage":
            print("You take away", item_amount, "health")
            result = ["dmg", item_amount]
        elif item_type == "speed":
            player.turns += item_amount
            print(f"You can now do {player.turns} moves per turn")
            result = ["turn", item_amount]
        elif item_type == "strength":
            player.dmg += item_amount
            print(f"You now do {player.dmg} damage")
        elif item_type == "percent_heal":
            new_health = player.health + round(player.max_health * (item_amount / 100))
            if new_health > player.max_health:
                new_health = player.max_health
            print("Healed for " + str(new_health - player.health))
            player.health = new_health
            print("Health:", player.health)
        player.inventory[item_name] -= 1
        return result

    def start_effect(self):
        Item.dialogue_effect(self.name)
        if self.name in Item.monster_stats.keys():
            self.fight()
        elif self.name in Item.thing_effects.keys():
            self.found_thing()
        elif self.name in Item.room_items.keys():
            choice = get_input(f"Do you enter the {self.name}? [y/n] ")
            if choice == "Y":
                self.enter()
        elif self.name in Item.path_stats.keys():
            monster = random.choices(Item.path_stats[self.name][0], Item.path_stats[self.name][1])[0]
            if monster != None:
                Item.dialogue_effect(f"{monster}_{self.name}")
                self.fight(monster)
        elif self.name in Item.ally_stats.keys():
            choice = get_input("[F]ight or [T]alk to them? ", choices=["F", "T"])
            if choice == "F":
                self.fight(self.name)
            else:
                self.talk()

    def talk(self):
        self.player.found["ally"] += 1
        ally = self.name
        Item.dialogue_effect(f"{ally}_start")
        input("")
        if self.player.found["ally"] > 1:
            print("You shake your head at them, and point at your mouth. They seem to understand.")
        else:
            print("You try to speak, but no words come out. You shake your head at them.")
        lookup = f"{ally}_a"
        Item.dialogue_effect(lookup)
        lookup = ""
        while True:
            choice = get_input("")
            if choice == "Y":
                lookup += "_y"
            else:
                lookup += "_n"
            if Item.dialogue_effect(lookup) == False:
                break

    def enter(self):
        lookup = f"{self.name}_enter"
        Item.dialogue_effect(lookup)
        population = Item.room_items[self.name][0]
        weights = Item.room_items[self.name][1]
        room_item = random.choices(population, weights, k=1)[0]
        choice = get_input("[E]xamine or [L]eave? ", choices = ["E", "L"])
        while choice != "L":
            lookup = f"{self.name}_examine"
            Item.dialogue_effect(lookup)
            Item.dialogue_effect(f"{room_item}_{self.name}")
            if room_item in Item.monster_stats.keys():
                self.fight(name=room_item)
                room_item = f"{room_item}_dead"
            else:
                if room_item in Item.thing_effects.keys():
                    pickup_choice = get_input("Pick it up? [y/n] ")
                    if pickup_choice == "Y":
                        print(f"{room_item} added to inventory.")
                        room_item = "nothing"
                else:
                    more_examine = get_input("Examine closer? [y/n] ")
                    if more_examine == "Y":
                        Item.dialogue_effect(f"{room_item}_examine_{self.name}")
            choice = get_input("[E]xamine again or [L]eave? ", choices = ["E", "L"])

    def found_thing(self):  # ADD MAP CONDITIONS
        self.player.found[self.name] += 1
        choices = ["E", "A"]
        if not self.name in Item.fight_items:
            sentence = "[U]se now, [E]xamine, or [A]dd to inventory? "
            choices.append("U")
        else:
            sentence = "[E]xamine item or [A]dd to inventory? "
        choice = get_input(sentence, choices=choices)
        if choice == "U":
            Item.inv_effect(player=self.player, item_name=self.name)
        elif choice == "E":
            lookup = f"{self.name}_examine{self.player.found[self.name]}"
            self.dialogue_effect(lookup)
            print("You place the item back on the ground")
        elif choice == "A":
            self.player.inventory[self.name] += 1
            print(f"{self.name} added to inventory. {self.name}s in inventory: {self.player.inventory[self.name]}")

    def fight(self, name="given"):
        run_punishment = 5
        if name == "given":
            name = self.name
        if name == "'you'":
            monster = {"name": name,
                       "dmg": self.player.dmg,
                       "max_health": self.player.max_health,
                       "health": self.player.health,
                       "special": "copy",
                       "turns": self.player.turns,
                       "max_turns": self.player.turns}
        elif name in Item.monster_stats.keys():
            monster = {"name": name,
                       "dmg": round(Item.monster_stats[name][0] + (
                                   Item.monster_stats[name][0] * (self.player.max_health - 100)) / 200),
                       "max_health": round(
                           Item.monster_stats[name][1] + (Item.monster_stats[name][1] * self.player.dmg) / 400),
                       "health": 0,
                       "special": Item.monster_stats[name][2],
                       "turns": 1,
                       "max_turns": 1}
            monster["health"] = monster["max_health"]
        else:
            monster = {"name": name,
                       "dmg": round(Item.ally_stats[name][0] + (
                               Item.ally_stats[name][0] * (self.player.max_health - 100)) / 200),
                       "max_health": round(
                           Item.ally_stats[name][1] + (Item.ally_stats[name][1] * self.player.dmg) / 400),
                       "health": 0,
                       "special": Item.ally_stats[name][2],
                       "turns": 2,
                       "max_turns": 2}
            monster["health"] = monster["max_health"]
        ph = self.player.health
        pd = self.player.dmg
        turns = self.player.turns
        while ph > 0 and monster["health"] > 0:
            choice = get_input("Try to [R]un, use [I]tem, [E]xamine, or [A]ttack? ", choices=["R", "I", "E", "A"])
            if choice == "R":
                fail_percent = (2 / 3) + ((monster["health"] / monster["max_health"]) / 3)
                success_percent = 1 - fail_percent
                success = random.choices([True, False], [success_percent, fail_percent], k=1)
                if success[0]:
                    print("You succeeded in running away")
                    if monster["health"] < pd:
                        print("(coward)")
                    return
                else:
                    print("You couldn't run away. ")
            elif choice == "E":
                string = f"{monster["name"]}'s health: {monster["health"]}\n{monster["name"]} dmg: {monster["dmg"]}\n"
                print(string)
                choice2 = get_input("Examine closer? (y/n) ")
                if choice2 == "y":
                    lookup = f"{monster["name"]}_data{self.player.killed[monster["name"]]}"
                    self.dialogue_effect(lookup)
            elif choice == "I":
                print("You have:")
                if not self.player.print_inventory(fight=True):
                    print("nothing")
                else:
                    data = self.player.use_inventory(fight=True)
                    if data is not None:
                        if data[0] == "turn":
                            turns += data[1]
                        elif data[0] == "dmg":
                            monster["health"] -= data[1]
                            if monster["health"] > 0:
                                print(f"{monster["name"]} now has {monster["health"]} health.")
                            else:
                                monster["health"] = 0
                                continue
            elif choice == "A":
                print("You take away", self.player.dmg, "health")
                monster["health"] -= self.player.dmg
                if monster["health"] > 0:
                    print(f"{monster["name"]} now has {monster["health"]} health.")
                else:
                    monster["health"] = 0
                    continue
            turns -= 1
            print()
            if turns > 0:
                print(turns, "turns left")
                continue
            turns = self.player.turns
            while monster["turns"] > 0:
                monster_choice = random.choices(["attack", "special"], [0.75, 0.25], k=1)[0]
                if monster["name"] == "'you'":
                    if choice == "A" or monster["turns"] < monster["max_turns"]:
                        monster_choice = "attack"
                    else:
                        lookup = f"{monster["name"]}_{choice}"
                else:
                    lookup = f"{monster["name"]}_{monster_choice}"
                self.dialogue_effect(lookup)
                if monster_choice == "attack":
                    print(f"You take {monster["dmg"]} damage")
                    self.player.health -= monster["dmg"]
                else:
                    if monster["special"][0] == "heal":
                        monster["health"] += monster["special"][1]
                        print(f"{monster['name']}: {monster["health"]} health")
                    elif monster["special"][0] == "double":
                        self.player.health -= monster["dmg"] * 2
                    elif monster["special"][0] == "steal":
                        possible_list = []
                        for key, value in self.player.inventory.items():
                            if value > 0:
                                possible_list.append(key)
                        if possible_list:
                            taken = possible_list[random.randint(0, len(possible_list))]
                            self.player.inventory[taken] -= 1
                            print(f"{monster['name']} takes one {taken}")
                        else:
                            print(f"{monster['name']} tries to steal, but you have nothing.")
                    elif monster["special"][0] == "copy":
                        if choice == "R":
                            print(f"You take {monster["dmg"] + run_punishment} damage")
                            self.player.health -= monster["dmg"] + run_punishment
                        elif choice == "E":
                            monster["dmg"] += 2
                        elif choice == "I":
                            self.dialogue_effect(f"'you'_{data[2]}")
                            if data[0] == "turn":
                                monster["turns"] += data[1]
                            elif data[0] == "dmg":
                                self.player.health -= data[1]
                ph = self.player.health
                monster["turns"] -= 1
            monster["turns"] = monster["max_turns"]
        end = False
        if ph <= 0:
            lookup = f"{monster["name"]}_kill"
            self.dialogue_effect(lookup)
            end_game("Game Over.")
        else:
            self.player.killed[monster["name"]] += 1
            lookup = f"{monster["name"]}_death"
            if name == "'you'":
                end = True
        self.dialogue_effect(lookup)
        if end:
            ending_type1 = self.player.found["bluebell flower"] > 0 + self.player.found["lion's tongue flower"] > 0 + \
                           self.found["lily flower"] > 0 + self.player.found["ally"] >= 4
            self.killed = {"ant": 0,
                           "cat": 0,
                           "slime": 0,
                           "bug": 0,
                           "Johnny": 0,
                           "Alicia": 0,
                           "Dominique": 0,
                           "Ella": 0}
            ending_type2 = (self.player.killed["Johnny"] or self.player.killed["Alicia"] or self.player.killed[
                "Dominique"] or
                            self.player.killed["Ella"]) + 10 * (
                                       self.killed["ant"] or self.player.killed["slime"] or self.player.killed["cat"] or
                                       self.player.killed["bug"])
            ending(ending_type1, ending_type2)

def ending(knowledge, kills):
    if knowledge == 3:
        lookup = "wise_"
    elif knowledge == 0:
        lookup = "empty_"
    else:
        lookup = "sly_"
    if kills == 11:
        lookup += "all"
    elif kills == 10:
        lookup += "own"
    elif kills == 1:
        lookup += "others"
    elif kills == 0:
        lookup += "none"
    Item.dialogue_effect(lookup)
    end_game("The End")

class Player:
    def __init__(self, map):
        self.map = map
        self.max_health = 100
        self.health = 100
        self.turns = 1
        self.dmg = 1
        self.set_pos()
        self.player = "o"
        self.item_under = ""
        self.inventory = {"medkit": 0,
                          "bluebell flower": 0,
                          "lily flower": 0,
                          "lion's tongue flower": 0,
                          "knife": 0,
                          "pistol": 0,
                          "shotgun": 0,
                          }
        self.found = {"medkit": 0,
                      "bluebell flower": 0,
                      "lily flower": 0,
                      "lion's tongue flower": 0,
                      "knife": 0,
                      "pistol": 0,
                      "shotgun": 0,
                      "ally": 0,
                      }
        self.killed = {"ant": 0,
                       "cat": 0,
                       "slime": 0,
                       "bug": 0,
                       "Johnny": 0,
                       "Alicia": 0,
                       "Dominique": 0,
                       "Ella": 0}

    def print_inventory(self, fight = False):
        result = ""
        for key,value in self.inventory.items():
            if value > 0 and (fight == True or not key in ["knife", "shotgun", "pistol"]):
                result += key + ": " + str(value) + "\n"
        if result:
            print(result, end="")
            return True
        return False

    def use_inventory(self, fight = False):
        possible_choices = {}
        for key, value in self.inventory.items():
            if value > 0:
                if fight or not key in ["knife", "pistol", "shotgun"]:
                    possible_choices[key] = value
        choice = get_input("Which item do you use? (input whole name) ", choices=list(possible_choices.keys()))
        data = Item.inv_effect(self, choice)
        if data:
            data = data[0], data[1], choice
        if fight:
            return data

    def set_pos(self):
        self.pos_x = self.map.chunk_length//2 -1
        self.pos_y = self.map.chunk_height//2


def move(player, dir):  # if player.pos_x <
    m = player.map
    p = player
    m.midx = (m.cur_cols[1] - m.cur_cols[0]) // 2 + m.cur_cols[0]
    m.midy = (m.cur_rows[1] - m.cur_rows[0]) // 2 + m.cur_rows[0]
    if dir == "w":
        if m.rc_count > 10000 and m.last_row == m.cur_rows[1]:
            p.pos_y += 1
        elif p.pos_y != m.midy:
            p.pos_y += 1
        else:
            m.cur_rows = (m.cur_rows[0] + 1, m.cur_rows[1] + 1)
            m.gen_rows("rows", m.cur_rows[1])
            p.pos_y += 1
    elif dir == "a":
        if m.cur_cols[0] == 0:
            if p.pos_x != 0:
                p.pos_x -= 1
        elif p.pos_x != m.midx:
            p.pos_x -= 1
        else:
            m.cur_cols = (m.cur_cols[0] - 1, m.cur_cols[1] - 1)
            p.pos_x -= 1
    elif dir == "s":
        if m.cur_rows[0] == 0:
            if p.pos_y != 0:
                p.pos_y -= 1
        elif p.pos_y != m.midy:
            p.pos_y -= 1
        else:
            m.cur_rows = (m.cur_rows[0] - 1, m.cur_rows[1] - 1)
            p.pos_y -= 1
    elif dir == "d":
        if m.rc_count > 10000 and m.last_cols == m.cur_cols[1]:
            p.pos_x += 1
        elif p.pos_x != m.midx:
            p.pos_x += 1
        else:
            m.cur_cols = (m.cur_cols[0] + 1, m.cur_cols[1] + 1)
            m.gen_rows("columns", m.cur_cols[1])
            p.pos_x += 1
    return Item(m.row_list[p.pos_y][p.pos_x], p)   #object under player


def get_input(line, prompt2=None, choices=["y","n"]):   #ADDED TRY EXCEPT BLOCKS
    lower_list(choices)
    if prompt2 == None:
        prompt2 = line
    try:
        answer = input(line).lower()
    except KeyboardInterrupt or EOFError:
        end_game("\nNo input given")
    while not answer in choices:
        print("Please choose from the following:", choices)
        try:
            answer = input(prompt2).lower()
        except KeyboardInterrupt or EOFError:
            msg = "\nNo input given"
            sys.exit(msg)
    return answer.upper()

def lower_list(l):
    for i in range(0, len(l)):
        l[i] = l[i].lower()


def create_range(tup):
    return list(range(tup[0], tup[1]))

def fight(enemy, player):
    bad_type = enemy[0]
    bad_health = enemy[1]
    bad_dmg = enemy[2]
    good_health = player.health
    good_dmg = player.dmg
    map = player.map
    w = map.width
    print("starting fight")
    while bad_health > 0:
        choice = input("[A]ttack or use [I]tem?")
        if choice == "A":
            bad_health -= good_dmg
        if choice == "I":
            while True:
                print("You have: ")
                print(", ".join(player.inventory.key()))
                item_choice = input("What item do you want to use? (Input name)")
                if item_choice in player.inventory:
                    break
                else:
                    print("Not valid")
            Item.item_effect(item_choice)






def game(map, player):
    #os.system('cls' if os.name == 'nt' else 'clear')
    map.draw(player)
    print("Press and Enter WASD to move.")

    while True:
        #print(map.cur_rows, map.cur_cols)
        try:
            pressed_key = input()
        except KeyboardInterrupt or EOFError:
            print("Interrupted.")
            return "EXIT"
        if pressed_key == "r":
            if get_input("Are you sure you want to restart?", "Restart?") == "Y":
                return "RESTART"
        elif pressed_key == "e":
            if get_input("Are you sure you want to end game?", "Exit?") == "Y":
                return "EXIT"
        elif pressed_key in ["w"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            obj = move(player, pressed_key)
            map.draw(player)
            obj.start_effect()
            print("Press and Enter WASD to move.")



if __name__ == "__main__":
    main()
