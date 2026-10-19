import random
global biome_weights
Fake_biome_weights = {"b": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],}
biome_weights = {"City":     [5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0],
                 "Field":    [0, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 "Trains":   [0, 0, 0, 90,0, 0, 0,45, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "Tech":     [0, 2, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 "Junkyard": [8, 9, 2, 2, 8, 8, 5, 0, 9, 0, 0, 9, 9, 9, 9, 0, 0, 9, 2, 9, 9, 1, 9, 9, 1],
                 "Swamp":    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 2, 0, 0, 0, 0, 0, 0],
                 "Firest":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                 "Forest":   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 9, 0, 0, 1, 0, 0],
                 "Army base":[0, 3, 0, 0, 0, 0, 15,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], }
#                             _     .  =  |  \  #  -  :  ?  !  @  L  ^  &  *  (  +  U  P  [  I  ,  >  X
def biome_maker():
    biome = random.choice(list(biome_weights.keys()))
    if biome == "Junkyard":
            biome = random.choice(list(biome_weights.keys()))
    return biome

def first_gen_rows():  # generate starting map
    Old_biome_weights = {"grassland":   [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                     "forest":      [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                     "city":        [0, 9, 9, 0, 0, 0, 0, 0, 7, 1],
                     "badlands":    [0, 0, 0, 6, 0, 0, 0, 1, 0, 0],
                     "swamp":       [0, 0, 0, 1, 9, 0, 0, 0, 2, 0],
                     "desert":      [0, 0, 0, 0, 0, 1, 2, 0, 0, 0],
                     "town":        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
                     }
    height = 31
    width = 190
    cur_rows = (0, height)
    cur_cols = (0, width)
    chunk_length = 24
    chunk_height = 8
    obj_list = ["_", " ", ".", "=", "|", "\\", "#", "-", ":", "?", "!", "@", "L", "^", "&", "*", "(", "+", "U", "P", "[", "I", ",", ">", "X"]
    row_list = []
    starting = True
    for row in range(0, height, chunk_height): #make each column of the rows
        for col in range(0, width, chunk_length): #make each chunk of a column
            if not starting:
                biome = biome_maker()
            else:
                biome = "Field"
                starting = False
            for chunk_row in range(row, row+chunk_height): #make each row of a chunk
                new_row = random.choices(obj_list, weights=biome_weights[biome], k=chunk_length) #make one row of a chunk
                if len(row_list) - 1 < chunk_row:
                    row_list.append([])
                row_list[chunk_row].extend(new_row)
    return row_list

def gen_rows(row_list, gen_type, num):
    #takes in either a new column or row to generate
    height = 200
    width = 600
    cur_rows = (0, height)
    cur_cols = (0, width)
    chunk_length = 10
    chunk_height = 4
    obj_list = ["_", " ", ".", "/", "|", "\\", "#"]
    print("generating a row/column")
    #if the row or column exists, don't add. If it doesn't, make a chunk.
    if gen_type == "column":
        biome = biome_maker()
        if len(row_list[0]) < num + 1: #if len == 1, then the index is 0. So length is +1 of number
            print(len(row_list[0]), num)
            for row_i in range(0, len(row_list)):
                if row_i % chunk_height == 0 or row_i == 0:
                    biome = biome_maker()
                new_row = random.choices(obj_list, weights=biome_weights[biome], k=chunk_length)
                row_list[row_i].extend(new_row)
    elif gen_type == "row":
        if len(row_list) < num + 1: #same here
            for row in range(len(row_list), len(row_list) + chunk_height, chunk_height):  # make each column of the rows
                for col in range(0, width, chunk_length):  # make each chunk of a column
                    biome = biome_maker()
                    for chunk_row in range(row, row + chunk_height):  # make each row of a chunk
                        new_row = random.choices(obj_list, weights=biome_weights[biome],
                                                 k=chunk_length)  # make one row of a chunk
                        if len(row_list) - 1 < chunk_row:
                            row_list.append([])
                        row_list[chunk_row].extend(new_row)
    return row_list


def test_first_gen():
    row_list = first_gen_rows()
    print("_" * len(row_list[0]))
    for row in row_list[::-1]:
        print("|", sep="", end="")
        for i in range(len(row)):
            print(row[i], sep="", end="")
        print("|")
    print("_" * len(row_list[0]))

def test_gen():
    gen_type = "row"
    num = 60
    row_list = gen_rows(row_list, gen_type, num)
    for row in row_list[::-1]:
        for i in range(len(row)):
            print(row[i], sep="", end="")
        print()

def get_input(line, choices=["y","n"]):
    answer = input(line)
    while not answer in choices:
        print("Please choose from the following:", choices)
        answer = input(line)
    return answer

class Item:
    def __init__(self, char, player):
        self.char = char
        self.player = player
        self.monster_stats = {"ant": [10, 10],
                              "cat": [90, 50],
                              "bug": [20, 10],
                              "slime": [40,70]}

        self.thing_effects = {"medkit": ["heal", 15],
                              "pistol": ["damage", 20],
                              "shotgun": ["damage", 40],
                              "bluebell flower": ["speed", 2],
                              "lily flower": ["percent_heal", 5],
                              "lion's tongue flower": ["strength", 10]}

        self.char_decode = {"_" : "road",
                            " " : "path",
                            "." : "ant",
                            "=" : "train cabin",
                            "|" : "wall",
                            "\\": "leaning wall",
                            "#" : "barbed wire",
                            "-" : "train couple",
                            ":" : "mech",
                            "?" : "'you'",
                            "!" : "ally",
                            "@" : "engine coil",
                            "L" : "gun",
                            "^" : "pine tree",
                            "&" : "ship cog",
                            "*" : "flower",
                            "(" : "water",
                            "+" : "medkit",
                            "U" : "slime",
                            "P" : "tree",
                            "[" : "room",
                            "I" : "building",
                            "," : "bug",
                            ">" : "cat",
                            "X" : "grave"}

    @classmethod
    def dialogue_effect(cls, item_name): #RENAME
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
    def chance_effect(self, percent = 25, effect_type = ["health", -5]):
        if percent > 100:
            percent = 100
        elif percent < 0: #don't be silly. A percentage can't be negative.
            percent = 0
        result = random.choices([True, False], weights=[percent, 100-percent], k=1)
        if result:
            if effect_type[0] == "health":
                self.player.health += effect_type[1]
                self.dialogue_effect(f"{self.char}_chance")

    def found_effect(self):
        choice = get_input("[c]ollect or [d]iscard?", ["c", "d"])
        if choice == "c":
            self.player.inventory[self.char_decode[self.char]] += 1
            print(f"item added to inventory")
        else:
            print("item left behind")
    def fight_effect(self):
        stats = self.monster_stats[self.char] #stats of this specific monster
        if stats[0] <= (self.player.health * 0.1):
            line = "[f]ight, [u]se item, or [r]un?"
            choices = ["f","u","r"]
        else:
            line = "[f]ight or [u]se item?"
            choices = ["f", "u"]
        choice = get_input(line, choices)
        if choice == "f":
            pass
        elif choice == "u":
            self.inventory_effect()
        else: # choice is r
            pass

    def inventory_effect(self, items = "all"):
        possible_list = []
        if items == "all":
            for thing, amount in self.player.inventory.items():
                if amount > 0:
                    possible_list.append(thing)
        elif items == "good":
            for thing in ["flower", "medkit"]:
                amount = self.player.inventory[thing]
                if amount > 0:
                    possible_list.append(thing)
        else:
            print("Unsure what else I would use")
        if len(possible_list) == 0:
            print("No items to use at this moment.")
            return
        print(f"You have: {possible_list}")
        object = get_input("Which item would you like to use?", possible_list)
        #by now, player has selected which item to use from allowed items (ie, a gun isn't allowed when not in combat)
        self.dialogue_effect(f"{choice}_use")
        #now, do the effect of the selected item
        effect, amount = self.thing_effects[object]
        if effect == "heal":
            if self.player.health < self.player.max_health:
                self.player.health += amount
                print(f"Healed for {amount}. You now have {self.player.health} health.")
                self.player.inventory[object] -= 1
            else:
                print("At max health already")
        elif effect == "percent_heal":
            if self.player.health < self.player.max_health:
                self.player.health += round((self.player.max_health * amount)/100)
                if self.player.health > self.player.max_health:
                    self.player.health = self.player.max_health
                print(f"Healed for {amount}. You now have {self.player.health} health.")
        elif effect == "damage":
            pass
        elif effect == "strength":
            pass


class Old_Item:
    def __init__(self, char, player):
        self.char = char
        self.player = player
        self.effect_dict = {"path": self.path_effect,
                            "enemy": self.enemy_effect,
                            "ally": self.ally_effect,
                            "item": self.item_effect,
                            }
        self.type_dict = {" ": ["path", "empty"],
                          "#": ["path", "hidden"],
                          ".": ["enemy", "small"],
                          "%": ["enemy", "big"],
                          ",": ["ally", "none"],
                          "+": ["item", "good"],
                          "-": ["item", "bad"],
                          }
        try:
            self.group = self.type_dict[char][0]
            self.subgroup = self.type_dict[char][1]
            self.effect = self.effect_dict[self.group]
        except KeyError:
            sys.exit("Object not in type list")
    @classmethod
    def first_effect(cls, item_name): #RENAME
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

    def path_effect(self): #if adding more path types, change item_name to reflect dict like in other effects.
        sub = self.subgroup
        if sub == "hidden":
            item_name = "hidden path"
            self.first_effect(item_name)

            type_list = [["path", "empty"],
                         ["enemy", "small"],
                         ["enemy", "big"],
                         ["ally", "none"],
                         ["item", "good"],
                         ["item", "bad"],
                        ]
            self.group, self.subgroup = random.choice(type_list)
            self.effect = self.effect_dict[self.group]
            self.effect()
        else:
            item_name = "empty path"
            self.first_effect(item_name)


    def enemy_effect(self):
        enemy_dict = {"small":
                          [("ant", 1, 1),
                           ("slime", 50, 75)],
                      "medium": [()],
                      "big":
                          [("you", 100, 100),
                           ("cat", 50, 75),
                           ("golem", 75, 50)]}


        enemy_subtype = random.choice(enemy_dict[self.subgroup])
        self.first_effect(enemy_subtype)
        h_total = 50 * math.log((0.076*self.player.health), math.e)
        d_total = 50 * math.log((0.076*self.player.dmg), math.e)
        h_percent = enemy_subtype[1] / 100
        d_percent = enemy_subtype[2] / 100
        enemy_health = round(h_total * h_percent)
        enemy_dmg = 1 if round(d_total * d_percent) < 1 else round(d_total * d_percent)
        self.fight((enemy_subtype, enemy_health, enemy_dmg))

    def fight(self, enemy):
        player = self.player
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
                    for item in player.inventory:
                        print(item, end="", sep=", ")
                    print("")
                    item_choice = input("What item do you want to use? (Input name)")
                    if item_choice in player.inventory:
                        break
                    else:
                        print("Not valid")
                dmg_boost = self.item_effect(item_choice)
    def ally_effect(self):
        ally_dict = ["Johnny", "Alison Trout", "Barry M. Barrel", "Figure", "Emery Trout"]
        ally = random.choice(ally_dict)
        self.first_effect(ally)
        with open("text", "r") as text, open("art.txt", "r") as art:
            #no use of art yet.
            prompt1 = "Talk to them? READLINES"
            if get_input(prompt1) == False:
                return




    def item_effect(self, item = None):
        item_list = {"good":
                         {
                        "bandages": (5, 0, 3, 1),
                        "bluebell flower": (5, 0, 1, 5),
                        "lily flower": (-1,0, 1, 5),
                        "lion's tongue flower": (0,2, 1, 10)
                    },
                     "bad":
                    {
                        "knife": (0,2,5, 2),
                        "pistol": (0,4,4, 2),
                        "shotgun": (0,10,2, 3)
                    }}

        choices_list = ["use", "examine"]
        if item == None:
            item_type = self.subgroup
            item = random.choice(item_list[item_type].keys())
            self.first_effect(item)
            self.player.inventory[item] += item_list[item_type][item][2]
            string = f"Would you like to [use] now, [examine], or [store] the {item} for later?\n"
            choices_list.append("store")
            if item_type == "bad":
                choices_list.remove("use")
        else:
            if item in item_list["good"]:
                item_type = "good"
            else:
                item_type = "bad"
            string = f"Would you like to [use] now or [examine] the {item}?\n"
        self.player.found[item] += 1
        while True:
            choice = input(string)
            if choice in choices_list:
                break
            else:
                print("Invalid")
        if choice == "examine":
            if self.player.found[item] > item_list[item_type][item][3]:
                num = item_list[item_type][item][3]
            else:
                num = self.player.found[item]

            find_string = f"{item}_{choice}{num}" #ie bandages_use, bandages_examine, etc
        else:
            find_string = f"{item}_{choice}"
        self.first_effect(find_string)
        if choice == "use":
            self.player.health += item_list[item_type][item][0]
            dmg_boost = item_list[item_type][item][1]
            self.player.inventory[item] -= 1
            return dmg_boost
        return 0

test_first_gen()