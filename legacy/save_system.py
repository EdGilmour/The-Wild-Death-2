import os

inv_pre = "i"

def read_data():
  return open("playerData.cache.txt", "r").read()

def write_data(append):
  if append:
    return open("playerData.cache.txt", "a")
  else:
    return open("playerData.cache.txt", "w")

def write_list(v_list):
  list_str = str()
  for value in v_list:
    list_str += value + "\n"
  return list_str

# fix inventory item saving (to do with inventory count not updating)
def save_value(value, name, v_list = None):
  if os.path.isfile("playerData.cache.txt") == False:
    open("playerData.cache.txt", "x")
  if get_value(name):
    new_v = str(value)
    if v_list != None:
      new_v = write_list(v_list)
    print(write_list(v_list))
    print(write_list(get_value(name, prefix = inv_pre)))
    new_data = read_data().replace(write_list(get_value(name, prefix = inv_pre)), new_v)
    if v_list != None:
      new_data = new_data.replace(get_value("player_inventory")[1:], len(v_list))
    data_txt_w = write_data(False)
    data_txt_w.write(new_data)
  else:
    data_txt_w = write_data(True)
    data_txt_w.write(name + " " + str(value) + "\n")
    if v_list != None:
      data_txt_w.write(write_list(v_list))

def get_value(name, default_value = False, prefix = ""):
  if os.path.isfile("playerData.cache.txt") == False:
    return default_value
  data = read_data().splitlines()
  for i in range(len(data)):
    for word in data[i].split():
      data_strs = data[i].split()
      if word == name:
        if data_strs[1][0] == prefix:
          item_count = int(data_strs[1][1:])
          item_list = []
          for j in range(item_count):
            item_list.append(data[i + j + 1])
          return item_list
        else:
          return data[i].split()[1]
  return default_value

def delete_value(name): # implement deleting specific list items
  new_data = read_data().replace(get_value(name), "")
  data_txt_w = write_data(False)
  data_txt_w.write(new_data)