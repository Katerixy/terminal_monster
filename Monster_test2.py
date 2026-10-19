import random
import sys
#CHANGES BANDAGES TO MEDKIT
#When added back to project, make the item under and item change after a condition (ie in thing_found)
def get_input(line, choices=["y","n"]):   #ADDED TRY EXCEPT BLOCKS
    try:
        answer = input(line)
    except KeyboardInterrupt:
        msg = "\nNo input given"
        sys.exit(msg)
    while not answer in choices:
        print("Please choose from the following:", choices)
        try:
            answer = input(line)
        except KeyboardInterrupt:
            msg = "\nNo input given"
            sys.exit(msg)
    return answer
class Player: #ADDED TURNS, KILLED
    def __init__(self):
        self.max_health = 100
        self.health = 100
        self.dmg = 100
        self.turns = 1
        self.player = "o"
        self.item_under = ""
        self.inventory = {"medkit": 1,
                        "bluebell flower": 1,
                        "lily flower": 0,
                        "lion's tongue flower": 1,
                        "knife": 2,
                        "pistol": 1,
                        "shotgun": 1,
                          }
        self.found = {"medkit": 1,
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
                       "bug":0,
                       "Johnny":0,
                       "Alicia":0,
                       "Dominique":0,
                       "Ella":0}
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
        choice = get_input("Which item do you use? (input whole name) ", list(possible_choices.keys()))
        data = Item.inv_effect(self, choice)
        data = data[0], data[1], choice
        if fight:
            return data




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
    path_stats = {"path": [path_monsters, [7,7,7,7,72]],
                  "road": [path_monsters, [2,2,2,2,92]]}
    room_items = {"train cabin": [["medkit", "knife", "suitcase", "hat", "bug"], [20,10,39,30, 1]],
                    "room": [["lily flower", "pistol", "picture frame", "food", "cat"],[20,10,39,30,1]],
                    "building": [["lily flower", "pistol", "phone","papers", "slime"],[20,10,39,30,1]]
                    }
    flower_effects = {"bluebell flower": ["speed", 1],
                     "lily flower": ["percent_heal", 5],
                     "lion's tongue flower": ["strength", 2]}

    def __init__(self, char, player): #ADDED NAME
        self.char = char
        self.player = player

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
        self.name = self.char_decode[self.char]
        if self.name == "flower":
            self.name = random.choice(list(Item.flower_effects.keys()))
        elif self.name == "gun":
            self.name = random.choice(["shotgun","pistol"])
        elif self.name == "ally":
            self.name = random.choice(list(Item.ally_stats.keys()))

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
            if choice == "y":
                self.enter()
        elif self.name in Item.path_stats.keys():
            monster = random.choices(Item.path_stats[self.name][0], Item.path_stats[self.name][1])[0]
            if monster != None:
                Item.dialogue_effect(f"{monster}_{self.name}")
                self.fight(monster)
        elif self.name in Item.ally_stats.keys():
            choice = get_input("[F]ight or [T]alk to them? ", ["F", "T"])
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
            if choice == "y":
                lookup+="_y"
            else:
                lookup+="_n"
            if Item.dialogue_effect(lookup) == False:
                break

    def enter(self):
        lookup = f"{self.name}_enter"
        Item.dialogue_effect(lookup)
        population = Item.room_items[self.name][0]
        weights = Item.room_items[self.name][1]
        room_item = random.choices(population,weights,k=1)[0]
        choice = get_input("[E]xamine or [L]eave? ", ["E", "L"])
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
                        if pickup_choice == "y":
                            print(f"{room_item} added to inventory.")
                            room_item = "nothing"
                    else:
                        more_examine = get_input("Examine closer? [y/n] ")
                        if more_examine == "y":
                            Item.dialogue_effect(f"{room_item}_examine_{self.name}")
            choice = get_input("[E]xamine again or [L]eave? ", ["E", "L"])



    def found_thing(self): #ADD MAP CONDITIONS
        self.player.found[self.name] += 1
        choices = ["E", "A"]
        if not self.name in Item.fight_items:
            sentence = "[U]se now, [E]xamine, or [A]dd to inventory? "
            choices.append("U")
        else:
            sentence = "[E]xamine item or [A]dd to inventory? "
        choice = get_input(sentence, choices)
        if choice == "U":
            Item.inv_effect(player=self.player, item_name=self.name)
        elif choice == "E":
            lookup = f"{self.name}_examine{self.player.found[self.name]}"
            self.dialogue_effect(lookup)
            print("You place the item back on the ground")
        elif choice == "A":
            self.player.inventory[self.name] += 1
            print(f"{self.name} added to inventory. {self.name}s in inventory: {self.player.inventory[self.name]}")


    def fight(self, name = "given"):
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
                       "dmg": round(Item.monster_stats[name][0]+(Item.monster_stats[name][0]*(self.player.max_health-100))/200),
                       "max_health": round(Item.monster_stats[name][1]+(Item.monster_stats[name][1]*self.player.dmg)/400),
                       "health": 0,
                       "special":Item.monster_stats[name][2],
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
            choice = get_input("Try to [R]un, use [I]tem, [E]xamine, or [A]ttack? ", ["R", "I", "E", "A"])
            if choice == "R":
                fail_percent =  (2/3)+ ((monster["health"]/monster["max_health"])/3)
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
                        self.player.health -= monster["dmg"]*2
                    elif monster["special"][0] == "steal":
                        possible_list = []
                        for key, value in self.player.inventory.items():
                            if value > 0:
                                possible_list.append(key)
                        taken = possible_list[random.randint(0,len(possible_list))]
                        self.player.inventory[taken] -= 1
                        print(f"{monster['name']} takes one {taken}")
                    elif monster["special"][0] == "copy":
                        if choice == "R":
                            print(f"You take {monster["dmg"]+run_punishment} damage")
                            self.player.health -= monster["dmg"]+run_punishment
                        elif choice == "E":
                            monster["dmg"] += 2
                        elif choice == "I":
                            self.dialogue_effect(f"'you'_{data[2]}")
                            if data[0] == "turn":
                                monster["turns"] += data[1]
                            elif data[0] == "dmg":
                                self.player.health -= data[1]
                ph = self.player.health
                monster["turns"] -=1
            monster["turns"] = monster["max_turns"]
        end = False
        if ph <= 0:
            lookup = f"{monster["name"]}_kill"
        else:
            self.player.killed[monster["name"]] += 1
            lookup = f"{monster["name"]}_death"
            if name == "'you'":
                end = True
        self.dialogue_effect(lookup)
        if end:
            ending_type1 = self.player.found["bluebell flower"]  > 0 + self.player.found["lion's tongue flower"] > 0 + self.found["lily flower"] > 0 + self.player.found["ally"] >= 4
            self.killed = {"ant": 0,
                           "cat": 0,
                           "slime": 0,
                           "bug": 0,
                           "Johnny": 0,
                           "Alicia": 0,
                           "Dominique": 0,
                           "Ella": 0}
            ending_type2 = (self.player.killed["Johnny"] or self.player.killed["Alicia"] or self.player.killed["Dominique"] or
                            self.player.killed["Ella"]) + 10*(self.killed["ant"] or self.player.killed["slime"] or self.player.killed["cat"] or self.player.killed["bug"])
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
    self.dialogue_effect(lookup)
    end_game("The End")


def main():
    player = Player()
    i_list = []
    char_decode = [     "_",
                        " ",
                        ".",
                        "=",
                        "|",
                        "\\",
                        "#",
                        "-",
                        ":",
                        "?",
                        "!",
                        "@",
                        "L",
                        "^",
                        "&",
                        "*",
                        "(",
                        "+",
                        "U",
                        "P",
                        "[",
                        "I",
                        ",",
                        ">",
                        "X"]
    for i in char_decode:
        var = Item(i, player)
        i_list.append(var)
        print(var.name)
        var.start_effect()


if __name__== "__main__":
    main()