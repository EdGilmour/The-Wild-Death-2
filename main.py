import asciiart
import save_system
import math
from enum import Enum

# Misc ideas: different backgrounds? easter eggs? Place Ideas(gremlin gulch, crack canyon, bandit bog), 

# professions: Craftsman(Armorer, Gun Smith), Gunslinger(Sheriff, Outlaw), Moneymaker(Investor, Entrepreneur)

# TODO: profession starting items

welcome_message = "Welcome to the Wild Death 2, Scumbag! You start in the wild deserts of Daleville, Kentucky and your goal is to escape to Ohio. But there is a problem the only way to Ohio is to get smuggled in due to the tough immigration laws of the Divided States of America (DSA). But it costs $1,000,000, which you don't have because your a broke loser. You must explore and gather the funds to escape. You wake up in an inn and think that today is the day for you to start collecting the dough you need. Good luck Scumbag!"

instructions_message = "\n" + "You can always enter help to see where you are, in case you get lost, and get your available options. You pathetic idiot!"

places_art = [
[[asciiart.daleville_west],
[asciiart.dale_bank],
[asciiart.sheriff_office, "Sheriff Etedin", "Jail Cell"],
[asciiart.gun_smith],
[asciiart.armorer],
[asciiart.tumbleweed_inn, "Barkeeper"],
[asciiart.smuggler_den],
[None], # Path to east
[None]], # Path to outskirts

[[asciiart.daleville_east],
[None], # Path to west
[asciiart.convenience_store],
[asciiart.church],
[asciiart.stable],
[asciiart.nine_lives_inn],
[None]], # Path to outskirts

[[asciiart.daleville_outskirts],
[None], # Path to west
[None], # Path to east
]]

# n- for if the place is a name
# num- if it is a general place change
places = [
[["Daleville West"],
["Dale Bank"],
["Sheriff's Office", "n- Sheriff Etedin", "Jail Cell"],
["Gun Smith"],
["Armorer"],
["Tumbleweed Inn", "n- Barkeep \"Doorknob\""],
["Smuggler's Den"],
["1- Daleville East"],
["2- Daleville Outskirts"]],

[["Daleville East"],
["0- Daleville West"],
["Convenience Store"],
["Church"],
["Stable"],
["Nine Lives Inn"],
["2- Daleville Outskirts"]],

[["Daleville Outskirts"],
["0- Daleville West"],
["1- Daleville East"]
]]

class Profession(Enum):
  _None = -1
  Gunslinger = 0
  Craftsman = 1
  Moneymaker = 2

playing = True
player_name = str()
max_name_length = 25
user_general_place = 0
user_place = 5
cash = 0
inventory = []
available_input = []
max_lvl = 10
player_lvl = 1
player_xp = 0
xp_4_lvls = [10, 25, 50, 100, 200, 300, 500, 750, 1000]
profession = Profession._None
profession_str = str()

def check_int(string_2_int, min_value = -math.inf, max_value = math.inf):
  try:
    s_int = int(string_2_int)
    if s_int >= min_value and s_int <= max_value:
      return True
    else:
      return False
  except(TypeError, ValueError):
    return False

def get_valid_int(prompt1, prompt2, valid_answers):
  valid = False
  ans = input(prompt1)
  while valid == False:
    if check_int(ans) and valid_answers.count(int(ans)) > 0:
      valid = True
    else:
      ans = input(prompt2)
  return int(ans)

def contains_space(value):
  for char in value:
    if char.isspace():
      return True
  return False

def set_profession_by_num(num):
  global profession
  global profession_str
  for prof in Profession:
    if prof.value == int(num):
      profession = prof
      profession_str = prof.name
      break

def add_xp(increase):
  global player_xp
  global player_lvl
  player_xp += increase
  while player_lvl < max_lvl and player_xp > xp_4_lvls[player_lvl - 1]:
    if player_xp > xp_4_lvls[player_lvl - 1]:
      new_increase = player_xp - xp_4_lvls[player_lvl - 1]
      player_xp = 0
      player_xp += new_increase
      player_lvl += 1
  save_system.save_value(player_lvl, "player_lvl")
  save_system.save_value(player_xp, "player_xp")

def add_inventory_item(item):
  inventory.append(item)
  save_system.save_value(save_system.inv_pre + str(len(inventory)), "player_inventory", inventory)

def remove_inventory_item(item):
  save_system.delete_value("player_inventory" + str(len(inventory)))
  inventory.remove(item)

def change_cash(change):
  global cash
  cash += change
  save_system.save_value(cash, "player_cash")

def get_player_name():
  global player_name
  print()
  player_name = input("But first scumbag, what is your name? ")
  while contains_space(player_name) or len(player_name) == 0 or len(player_name) > max_name_length:
    player_name = input("Enter a valid name (is not empty, has no spaces, and less than " + str(max_name_length) + " letters) ")

def get_player_profession():
  global profession
  global profession_str
  print()
  print("Enter 0 if you're a Gunslinger")
  print("Enter 1 if you're a Craftsman")
  print("Enter 2 if you're a Moneymaker")
  print()
  player_profession = get_valid_int("And what is your proffesion? ", "Enter 0, 1, or 2 ", [0, 1, 2])
  set_profession_by_num(player_profession)

def quit():
  global playing
  playing = False
  print("\n" + "Thanks for playing The Wild Death 2! (The game autosaves so return anytime to pick up right where you left off)")

def help(n):
  if user_place == 0:
    print(n + "You are in " + name_without_attr(places[user_general_place][user_place][0]) + "\n")
  else:
    print(n + "You are in the " + places[user_general_place][user_place][0] + "\n")
  print(places_art[user_general_place][user_place][0])
  print_view_options()
  print_available_options()

def print_view_options():
  print("Enter 'quit' to exit the game (Data autosaves)")
  print("Enter 'xp' to view your current profession experience")
  print("Enter 'inventory' to view the items in your inventory")
  print()

def print_available_options():
  if user_place == 0:
    for i in range(len(places[user_general_place])):
      if i > 0:
        if is_general_place_change(places[user_general_place][i][0]):
          print("Enter " + str(i) + " to go to " + name_without_attr(places[user_general_place][i][0]))
        else:
          print("Enter " + str(i) + " to go to the " + places[user_general_place][i][0])
  else:
    print("Enter 0 to leave the " + places[user_general_place][user_place][0])
    for i in range(len(places[user_general_place][user_place])):
      if i > 0:
        if is_name(places[user_general_place][user_place][i]):
          print("Enter " + str(i) + " to go to " + name_without_attr(places[user_general_place][user_place][i]))
        else:
          print("Enter " + str(i) + " to go to the " + places[user_general_place][user_place][i])
  print()

def set_available_input():
  global available_input
  new_input = []
  if user_place == 0:
    for i in range(len(places[user_general_place])):
      new_input.append(i)
  else:
    for i in range(len(places[user_general_place][user_place])):
      new_input.append(i)
  available_input = new_input

def is_name(string_2_check):
  return string_2_check[0:2] == "n-"

def is_general_place_change(general_place_string):
  try:
    int(general_place_string[0])
    return True
  except:
    return False

def general_place_num(general_place_string):
  try:
    return int(general_place_string[0])
  except:
    return False

def name_without_attr(string_2_remove):
  if string_2_remove[1] == "-":
    return string_2_remove[3:]
  else:
    return string_2_remove

def view_xp():
  global profession_str
  print()
  print("--- " + profession_str + " ---")
  if player_lvl < max_lvl:
    print("Level: " + str(player_lvl))
    print("XP: " + str(player_xp) + "/" + str(xp_4_lvls[player_lvl - 1]))
  else:
    print("Level: MAX (" + str(max_lvl) + ")")
  add_inventory_item("new item")
  print()

def view_inventory():
  print()
  print("Cash: $" + str(cash))
  if len(inventory) > 0:
    print("\n" + "Inventory")
    print("--")
    for item in inventory:
      print("• " + str(item))
    print("--")
  else:
    print("Your inventory is empty loser")
  print()

def move_action(action):
  print()
  global user_place
  global user_general_place
  if action != 0 and is_general_place_change(places[user_general_place][action][0]):
    user_general_place = general_place_num(places[user_general_place][action][0])
    save_system.save_value(user_general_place, "player_general_place")
    print("You enter " + name_without_attr(places[user_general_place][0][0]))
    print(places_art[user_general_place][0][0])
  else:
    if action == 0:
      print("You left the " + places[user_general_place][user_place][0] + " and you are now in " + name_without_attr(places[user_general_place][0][0]))
      print(places_art[user_general_place][action][0])
    elif user_place == 0:
      print("You enter the " + places[user_general_place][action][0])
      print(places_art[user_general_place][action][0])
    else:
      if is_name(places[user_general_place][user_place][action]):
        print("You go to " + name_without_attr(places[user_general_place][user_place][action]))
      else:
        print("You go to the " + places[user_general_place][user_place][action])
      print(places_art[user_general_place][user_place][action])
      return
    user_place = action
    save_system.save_value(action, "player_place")
  print_available_options()
  set_available_input()

def save_name_and_profession():
  save_system.save_value(player_name, "player_name")
  save_system.save_value(Profession(profession).value, "player_profession")

def set_local_data():
  global player_name
  global profession
  global player_lvl
  global player_xp
  global cash
  global user_place
  global user_general_place
  global inventory
  player_name = save_system.get_value("player_name")
  set_profession_by_num(save_system.get_value("player_profession"))
  player_lvl = int(save_system.get_value("player_lvl", 1))
  player_xp = int(save_system.get_value("player_xp", 0))
  cash = int(save_system.get_value("player_cash", 0))
  user_place = int(save_system.get_value("player_place", 5))
  user_general_place = int(save_system.get_value("player_general_place", 0))
  inventory = save_system.get_value("player_inventory", [], save_system.inv_pre)

def main():
  if save_system.get_value("player_name") == False:
    print(welcome_message)
    print(instructions_message)
    get_player_name()
    get_player_profession()
    save_name_and_profession()
  else:
    set_local_data()
  set_available_input()
  help("")
  
  while playing:
    user_input = input("What would you like to do? You runt. ")
    if user_input.lower() == "help":
      help("\n")
    elif user_input.lower() == "quit":
      quit()
    elif user_input.lower() == "xp":
      view_xp()
    elif user_input.lower() == "inventory":
      view_inventory()
    elif check_int(user_input, min(available_input), max(available_input)):
      for i in available_input:
        if int(user_input) == i:
          move_action(i)
          break
    else:
      print("\n" + str(user_input) + " is not a valid command you idiot. Enter help to look at the available options." + "\n")

main()