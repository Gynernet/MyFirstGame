import curses
import msvcrt
import time

current_map = []
win_levels = {"main": 2, "lvl1": 2, "lvl2": 0, "lvl3": 0, "lvl4": 0}
current_enemies = []

def Screen(map_list, c_item, last_action):
    # What is shown on the screen

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    # Creates the play area
    for line in range(0, 11):
        line_to_create = ""
        if line <= int(map_list[0]-1):
            for i in range(0, map_list[1]):
                x = int((line*int(map_list[1]))+i+3)
                line_to_create += str(map_list[x])
        else:
            for i in range(0, map_list[1]):
                line_to_create += "   "
        # Creates the insturctions
        if line == 0:
            line_to_create += "  Use arrow keys or WASD to move.      H to restart.              Esc to exit.                   "
        #elif line == 1:
        #    line_to_create += "  Press V or 4 to make an action. Press X or 2 to switch what action you make.                   "
        #elif line == 2:
        #    line_to_create += "  Press C 3 to use an item. Press Z or 1 to switch which item you use.                        "
        elif line == 3:
            line_to_create += "  Keys: {0}  Latest action: {1}                           ".format(c_item, last_action)
        else:
            line_to_create += "                                                                                                          "
        stdscr.addstr(int(line), 0, line_to_create)

    stdscr.refresh()
def Make_map(map_list):
    # First value is to be in range 1-11
    # 0 = empty, 1 = player, 2 = wall, 3 = enemy, 4 = door, 5 = key, 6 = goal, 80-99 = room_switch
    x = int(3+(map_list[0]*map_list[1]))
    i = 3
    for v in map_list[3:x]:
        if len(v) == 3:
            if map_list[i] == "000":
                map_list[i] = " _ "
                i += 1
            elif map_list[i][0] == "1":
                map_list[i] = " :D"
                i += 1
            elif map_list[i] == "002":
                map_list[i] = "###"
                i += 1
            elif map_list[i] == "004":
                map_list[i] = "I#I"
                i += 1
            elif map_list[i] == "005":
                map_list[i] = "o-+"
                i += 1
            elif map_list[i] == "006":
                map_list[i] = "^l "
                i += 1
            else:
                map_list[i] = "/@\\"
                i += 1
        elif len(v) == 5:
            if map_list[i][3] == "3":
                if map_list[i][4] == "0":
                    map_list[i] = "¤o_"
                elif map_list[i][4] == "1":
                    map_list[i] = "_o¤"
                elif map_list[i][4] == "2":
                    map_list[i] = " ¤p"
                elif map_list[i][4] == "3":
                    map_list[i] = "d¤ "
                i += 1
            elif map_list[i][4] == "1":
                map_list[i] = "/1\\"
                i += 1
            elif map_list[i][4] == "2":
                map_list[i] = "/2\\"
                i += 1
            elif map_list[i][4] == "3":
                map_list[i] = "/3\\"
                i += 1
            elif map_list[i][4] == "4":
                map_list[i] = "/4\\"
                i += 1
            else:
                map_list[i] = "?"
                i += 1
    return map_list
def Update_map(map_list, c_item, last_action):
    Screen(Make_map(map_list.copy()), c_item, last_action)

    # how often the map updates on screen.
    time.sleep(0.05)

def Lose(level):
    global win_levels
    if win_levels[level["lvl"]] == 2:
        win_levels[level["lvl"]] = 4
    else:
        win_levels[level["lvl"]] = 3
def Keys(inv):
    key_slots = ""
    if inv == 0:
        key_slots = "           "
    elif inv == 1:
        key_slots = "o-+        "
    elif inv == 2:
        key_slots = "o-+ o-+    "
    elif inv == 3:
        key_slots = "o-+ o-+ o-+"
    else:
        key_slots = str("o-+ X" + str(inv) + "      ")
    return key_slots

def E_move(position, move_to):
    global current_map
    move_to_pos = current_map[move_to]
    move_result = 0
    if len(move_to_pos) == 3:
        if move_to_pos == "002" or move_to_pos == "006" or move_to_pos == "004":
            move_result = 2
        elif move_to_pos[0] == "1" or move_to_pos == "000" or move_to_pos == "005":
            current_map[move_to] = current_map[move_to] + current_map[position][3:]
            current_map[position] = current_map[position][0:3]
            move_result = 0
        else:
            move_result = 2
    else:
        if move_to_pos[3] == "3":
            move_result = 2
    return move_result
def Simple_enemy_ud(emc, move_direction):
    global current_enemies
    global current_map
    enemy_count = current_enemies[emc+1]
    enemies = {}
    x = 3
    for i in range(0,enemy_count):
        enemy = [i, int(current_enemies[emc+i+2]), int(emc+i+2)]
        position = 0
        while position == 0:
            if len(current_map[x]) == 5:
                if current_map[x][3] == "3" and (current_map[x][4] == "2" or current_map[x][4] == "3"):
                    position = x
            x += current_map[1]
            if x > int((current_map[0]*current_map[1])+2):
                x = int(x+1-(current_map[0]*current_map[1]))
        enemy.append(position)
        enemies.update({str(i):enemy})
    for e in enemies:
        if enemies[e][1] == 1:
            current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "2"
            move_to = int(enemies[e][3]-current_map[1])
            if move_to < 3:
                move_result = 2
            else:
                if move_direction == "down":
                    if int(current_map[move_to][0]) == 1:
                        move_result = 2
                    else:
                        move_result = E_move(enemies[e][3], move_to)
                else:
                    move_result = E_move(enemies[e][3], move_to)
            if move_result == 2:
                current_enemies[enemies[e][2]] = 0
                current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "3"
        elif enemies[e][1] == 0:
            current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "3"
            move_to = int(enemies[e][3]+current_map[1])
            if move_to > int((current_map[0]*current_map[1])+3):
                move_result = 2
            else:
                if move_direction == "up":
                    if int(current_map[move_to][0]) == 1:
                        move_result = 2
                    else:
                        move_result = E_move(enemies[e][3], move_to)
                else:
                    move_result = E_move(enemies[e][3], move_to)
            if move_result == 2:
                current_enemies[enemies[e][2]] = 1
                current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "2"
    return int(enemy_count + 2)
def Simple_enemy_lr(emc, move_direction):
    global current_enemies
    global current_map
    enemy_count = current_enemies[emc+1]
    enemies = {}
    x = 3
    for i in range(0,enemy_count):
        enemy = [i, int(current_enemies[emc+i+2]), int(emc+i+2)]
        position = 0
        while position == 0:
            if len(current_map[x]) == 5:
                if current_map[x][3] == "3" and (current_map[x][4] == "0" or current_map[x][4] == "1"):
                    position = x
                x += 1
            else:
                x += 1
        enemy.append(position)
        enemies.update({str(i):enemy})

    for e in enemies:
        if enemies[e][1] == 1:
            current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "1"
            move_to = int(enemies[e][3]+1)
            if int((enemies[e][3]-2)%current_map[1]) == 0:
                move_result = 2
            else:
                if move_direction == "left":
                    if int(current_map[move_to][0]) == 1:
                        move_result = 2
                    else:
                        move_result = E_move(enemies[e][3], move_to)
                else:
                    move_result = E_move(enemies[e][3], move_to)
            if move_result == 2:
                current_enemies[enemies[e][2]] = 0
                current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "0"
        elif enemies[e][1] == 0:
            current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "0"
            move_to = int(enemies[e][3]-1)
            if move_to < int((((enemies[e][3]-2)//current_map[1])*current_map[1])+3) and int((enemies[e][3]-2)%current_map[1]) != 0:
                move_result = 2
            else:
                if move_direction == "right":
                    if int(current_map[move_to][0]) == 1:
                        move_result = 2
                    else:
                        move_result = E_move(enemies[e][3], move_to)
                else:
                    move_result = E_move(enemies[e][3], move_to)
            if move_result == 2:
                current_enemies[enemies[e][2]] = 1
                current_map[enemies[e][3]] = current_map[enemies[e][3]][:4] + "1"
    return int(enemy_count + 2)

def Move_enemies(move_direction):
    enemy_types = current_enemies[0]
    ce_type = 0 # current enemy type
    emc = 1 # counter used to read the enemy list
    while enemy_types > 0:
        ce_type = current_enemies[emc]
        if ce_type == 1:
            emc += Simple_enemy_lr(emc, move_direction)
        elif ce_type == 2:
            emc += Simple_enemy_ud(emc, move_direction)
        enemy_types -= 1

def Move_to(level, player_pos, move_to):
    global current_map
    global current_enemies
    move_to_pos = current_map[move_to]

    if len(move_to_pos) == 3:
        if move_to_pos == "002":
            pass

        elif move_to_pos == "006":
            global win_levels
            win_levels[level["lvl"]] = 1

        elif move_to_pos == "004":
            if level["inv"][0] >= 1:
                level["inv"][0] -= 1
                current_map[move_to] = "100"
                current_map[player_pos] = "0" + current_map[player_pos][1:]
            else:
                pass

        elif move_to_pos == "000":
            current_map[move_to] = "1" + move_to_pos[1:]
            current_map[player_pos] = "0" + current_map[player_pos][1:]

        elif move_to_pos == "005":
            level["inv"][0] += 1
            current_map[move_to] = "100"
            current_map[player_pos] = "0" + current_map[player_pos][1:]

        else:
            portal_to = int(move_to_pos[1:3])
            portal_from = current_map[2]
            current_map[player_pos] = "0" + current_map[player_pos][1:]
            move_to_map = level[portal_to]
            x = 0
            i = 3
            while x == 0:
                if move_to_map[i][1:3] == str(portal_from):
                    move_to_map[i] = "1" + move_to_map[i][1:]
                    x = 1
                else:
                    i += 1
            current_map = move_to_map
            current_enemies = level[str(str(current_map[2])+"e")]

    elif len(move_to_pos) == 5:
        if move_to_pos[3] == "3":
            Lose(level)
            current_map[player_pos] = "0" + current_map[player_pos][1:]
        if move_to_pos == "00001":
            Run_a_level(Level_1())
            current_map = main_menu[80]
            current_enemies = main_menu["80e"]
        elif move_to_pos == "00002":
            Run_a_level(Level_2())
            current_map = main_menu[80]
            current_enemies = main_menu["80e"]
        elif move_to_pos == "00003":
            Run_a_level(Level_3())
            current_map = main_menu[81]
            current_enemies = main_menu["81e"]
        elif move_to_pos == "00004":
            Run_a_level(Level_4())
            current_map = main_menu[81]
            current_enemies = main_menu["81e"]
def Move_up(level):
    player_pos = 0
    i = 3
    while player_pos == 0:
        if current_map[i][0] == "1":
            player_pos = i
        else:
            i += 1
    move_to_pos = int(player_pos-current_map[1])
    if move_to_pos < 3:
        pass
    else:
        Move_to(level, player_pos, move_to_pos)
def Move_down(level):
    player_pos = 0
    i = 3
    while player_pos == 0:
        if current_map[i][0] == "1":
            player_pos = i
        else:
            i += 1
    move_to_pos = int(player_pos+current_map[1])
    if move_to_pos > int((current_map[0]*current_map[1])+3):
        pass
    else:
        Move_to(level, player_pos, move_to_pos)
def Move_left(level):
    player_pos = 0
    i = 3
    while player_pos == 0:
        if current_map[i][0] == "1":
            player_pos = i
        else:
            i += 1
    move_to_pos = int(player_pos-1)
    if move_to_pos < int((((player_pos-2)//current_map[1])*current_map[1])+3) and int((player_pos-2)%current_map[1]) != 0:
        pass
    else:
        Move_to(level, player_pos, move_to_pos)
def Move_right(level):
    player_pos = 0
    i = 3
    while player_pos == 0:
        if current_map[i][0] == "1":
            player_pos = i
        else:
            i += 1
    move_to_pos = int(player_pos+1)
    if int((player_pos-2)%current_map[1]) == 0:
        pass
    else:
        Move_to(level, player_pos, move_to_pos)

def Reset_level(level):
    if level["lvl"] == "main":
        level = Main_menu()
    if level["lvl"] == "lvl1":
        level = Level_1()
    if level["lvl"] == "lvl2":
        level = Level_2()
    if level["lvl"] == "lvl3":
        level = Level_3()
    if level["lvl"] == "lvl4":
        level = Level_4()
    return level
def Run_main_menu(level):
    global current_map
    global current_enemies
    global win_levels
    if win_levels[level["lvl"]] == 1:
        win_levels[level["lvl"]] = 2
    current_map = level[80]
    current_enemies = level["80e"]
    key = "i"
    break_time = 1
    start_msg = "               "
    escapeKey = 27
    while ord(key) != escapeKey and win_levels[level["lvl"]] != 1:
        Update_map(current_map, Keys(level["inv"][0]), start_msg)
        while break_time == 0:
            # Key Binds
            key = msvcrt.getch()
            
            if (win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2) or ord(key) == 104:
                break_time = 1
                if win_levels[level["lvl"]] == 2:
                    win_levels[level["lvl"]] = 4
                break
            if ord(key) == 27:
                if win_levels[level["lvl"]] == 2:
                    win_levels[level["lvl"]] = 1
                break
            # Movement keys
            if ord(key) == 72 or ord(key) == 119:
                Move_up(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved up       ")
            elif ord(key) == 80 or ord(key) == 115:
                Move_down(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved down     ")
            elif ord(key) == 75 or ord(key) == 97:
                Move_left(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved left     ")
            elif ord(key) == 77 or ord(key) == 100:
                Move_right(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved right    ")
            if win_levels["lvl1"] == 1 and level["80e"][1] == 1:
                level[80][12] = "005"
                level["80e"][1] = 0
            if win_levels["lvl2"] == 1 and level["80e"][2] == 1:
                level[80][14] = "005"
                level["80e"][2] = 0
            if win_levels["lvl3"] == 1 and level["81e"][1] == 1:
                level[81][12] = "005"
                level["81e"][1] = 0
            if win_levels["lvl4"] == 1 and level["81e"][2] == 1:
                level[81][14] = "005"
                level["81e"][2] = 0
        if win_levels[level["lvl"]] == 4:
            level = Reset_level(level)
            current_map = level[80]
            current_enemies = level["80e"]
            win_levels[level["lvl"]] = 2
            key = "i"
        break_time = 0
def Run_a_level(level):
    global current_map
    global current_enemies
    global win_levels
    if win_levels[level["lvl"]] == 1:
        win_levels[level["lvl"]] = 2
    current_map = level[80]
    current_enemies = level["80e"]
    key = "i"
    break_time = 1
    start_msg = "               "
    while ord(key) != 27 and win_levels[level["lvl"]] != 1:
        Update_map(current_map, Keys(level["inv"][0]), start_msg)
        while break_time == 0:
            # Key Binds
            key = msvcrt.getch()
            
            if (win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2) or ord(key) == 104:
                break_time = 1
                if win_levels[level["lvl"]] == 0:
                    win_levels[level["lvl"]] = 3
                elif win_levels[level["lvl"]] == 2:
                    win_levels[level["lvl"]] = 4
                break
            if ord(key) == 27:
                if win_levels[level["lvl"]] == 2:
                    win_levels[level["lvl"]] = 1
                break
            # Movement keys
            if ord(key) == 72 or ord(key) == 119:
                Move_enemies("up")
                Move_up(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved up       ")
                if win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2:
                    break
            elif ord(key) == 80 or ord(key) == 115:
                Move_enemies("down")
                Move_down(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved down     ")
                if win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2:
                    break
            elif ord(key) == 75 or ord(key) == 97:
                Move_enemies("left")
                Move_left(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved left     ")
                if win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2:
                    break
            elif ord(key) == 77 or ord(key) == 100:
                Move_enemies("right")
                Move_right(level)
                Update_map(current_map, Keys(level["inv"][0]), "moved right    ")
                if win_levels[level["lvl"]] != 0 and win_levels[level["lvl"]] != 2:
                    break

            # Action keys
            #elif ord(key) == 122 or ord(key) == 49:
            #    Update_map(current_map, Keys(level["inv"][0]), "switched item  ")
            #elif ord(key) == 120 or ord(key) == 50:
            #    Update_map(current_map, Keys(level["inv"][0]), "not implemented")
            #elif ord(key) == 99 or ord(key) == 51:
            #    Update_map(current_map, Keys(level["inv"][0]), "used an item   ")
            #elif ord(key) == 118 or ord(key) == 52:
            #    Update_map(current_map, Keys(level["inv"][0]), "made an action ")
            #elif ord(key) == 98 or ord(key) == 53:
            #    Update_map(current_map, Keys(level["inv"][0]), "made an action ")
        if win_levels[level["lvl"]] == 3:
            level = Reset_level(level)
            current_map = level[80]
            current_enemies = level["80e"]
            win_levels[level["lvl"]] = 0
            key = "i"
            start_msg = "you died       "
        elif win_levels[level["lvl"]] == 4:
            level = Reset_level(level)
            current_map = level[80]
            current_enemies = level["80e"]
            win_levels[level["lvl"]] = 2
            key = "i"
            start_msg = "you died       "
        break_time = 0

def Main_menu():
    # the start position of a level
    # "x00x" = empty, "1xxx" = player, "x02x" = wall, "xxx3" = enemy, "x04x" = door, "x05x" = key, "x06x" = goal, "x80"-"x99" = room_switch
    level_dict = {}
    
    level_dict.update({"lvl": "main"})
    inventory = [0, 0]
    start_room80 = [7, 7, 80, 
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "000",  "100",  "000",  "000",  "000",  "002",
                    "002",  "000",  "000",  "000",  "000",  "004",  "081",
                    "002",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "000","00001",  "000","00002",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies80 = [0, 1, 1]
    up_room81 = [7, 7, 81,
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "004",  "002",
                    "002",  "000",  "000",  "000",  "002",  "004",  "002",
                    "080",  "000",  "000",  "000",  "002",  "004",  "082",
                    "002",  "000",  "000",  "000",  "000",  "002",  "002",
                    "002",  "002","00003",  "002","00004",  "002",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies81 = [0, 1, 1]
    left_room82 = [3, 4, 82,
                    "000",  "000",  "000",  "000",
                    "081",  "000",  "000",  "006",
                    "000",  "000",  "000",  "000"]
    enemies82 = [0]
    level_dict.update({80: start_room80})
    level_dict.update({81: up_room81})
    level_dict.update({82: left_room82})
    level_dict.update({"80e": enemies80})
    level_dict.update({"81e": enemies81})
    level_dict.update({"82e": enemies82})
    level_dict.update({"inv": inventory})
    return level_dict

def Level_1():
    # the start position of a level
    # "x00x" = empty, "1xxxx" = player, "x02" = wall, "xxx3x" = enemy, "x04" = door, "x05xx" = key, "x06" = goal, "x80"-"x99" = room_switch
    # enemy move 0 = left, 1 = right, 2 = up, 3 = down
    level_dict = {}
    
    level_dict.update({"lvl": "lvl1"})
    inventory = [0, 0]
    start_room80 = [7, 8, 80, # room size
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "002",  "002",
                    "002",  "000",  "100",  "000",  "000",  "000",  "004",  "081",
                    "002",  "000",  "000",  "000",  "000",  "000",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "000",  "000",  "000",  "005",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies80 = [0]
    up_room81 = [9, 11, 81,
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "080",  "000",  "002","00031",  "000",  "000",  "000","00030",  "002","00033",  "002",
                    "002",  "000",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "000",  "002",
                    "002",  "000",  "000",  "000",  "002","00031",  "000",  "000",  "002",  "000",  "002",
                    "002",  "002",  "002",  "000",  "002",  "002",  "002",  "002",  "002",  "000",  "002",
                    "002","00032",  "002",  "000",  "000",  "000",  "000",  "000",  "002","00032",  "002",
                    "002",  "000",  "002",  "000",  "000","00031",  "000",  "000",  "002",  "002",  "002",
                    "002",  "000",  "002",  "000",  "000",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "082",  "002"]
    enemies81 = [2, 1, 4, 1, 0, 1, 1, 2, 3, 1, 0, 1]
    left_room82 = [7, 7, 82,
                    "002",  "002",  "002",  "081",  "002",  "002",  "002",
                    "002","00033",  "002",  "000",  "000",  "000",  "002",
                    "002",  "000",  "002",  "000",  "000",  "000",  "002",
                    "002",  "000",  "002",  "002",  "002",  "000",  "002",
                    "002",  "005",  "000",  "000",  "000",  "000",  "002",
                    "002",  "000",  "002",  "000",  "002",  "004",  "002",
                    "002",  "002",  "002",  "002",  "002",  "083",  "002"]
    enemies82 = [1, 2, 1, 0]
    down_room83 = [5, 5, 83,
                    "002",  "002",  "082",  "002",  "002",
                    "002",  "000",  "000",  "000",  "002",
                    "002",  "000",  "006",  "000",  "002",
                    "002",  "000",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002"]
    enemies83 = [0]
    level_dict.update({80: start_room80})
    level_dict.update({81: up_room81})
    level_dict.update({82: left_room82})
    level_dict.update({83: down_room83})
    level_dict.update({"80e": enemies80})
    level_dict.update({"81e": enemies81})
    level_dict.update({"82e": enemies82})
    level_dict.update({"83e": enemies83})
    level_dict.update({"inv": inventory})
    return level_dict

def Level_2():
    # the start position of a level
    # "x00x" = empty, "1xxx" = player, "x02x" = wall, "xxx3" = enemy, "x04x" = door, "x05x" = key, "x06x" = goal, "x80"-"x99" = room_switch
    level_dict = {}
    
    level_dict.update({"lvl": "lvl2"})
    inventory = [0, 0]
    start_room80 = [11, 11, 80, # room size
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "002",  "002",  "002",  "002",  "000",  "000",  "002",  "085",  "002",  "002",
                    "002",  "002",  "002",  "002",  "002",  "000",  "000",  "002",  "000",  "002",  "002",
                    "002",  "083",  "000",  "084",  "002",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "002",  "000",  "002",  "002",  "000",  "000",  "000",  "002",  "004",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "100",  "000",  "002",  "004",  "002",
                    "002",  "000",  "002",  "002",  "000",  "000",  "000",  "000",  "002",  "004",  "002",
                    "002",  "000",  "002",  "082",  "000",  "002",  "002",  "002",  "002",  "004",  "002",
                    "002",  "000",  "002",  "002",  "000",  "081",  "002",  "002",  "002",  "004",  "002",
                    "002",  "000",  "000",  "000",  "000",  "002",  "002",  "002",  "002",  "006",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies80 = [0]
    up_room81 = [7, 7, 81,
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "002",  "000",  "000","00033",  "002",
                    "002",  "000",  "000",  "000",  "002",  "000",  "002",
                    "080",  "000",  "000",  "000",  "002",  "005",  "002",
                    "002",  "000",  "000",  "000",  "002",  "000",  "002",
                    "002",  "000",  "002","00032",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies81 = [1, 2, 2, 1, 0]
    left_room82 = [7, 5, 82,
                    "002",  "002",  "002",  "002",  "002",
                    "002",  "002",  "000",  "000",  "002",
                    "002",  "000","00031",  "000",  "002",
                    "002",  "005",  "002",  "000",  "080",
                    "002",  "000","00030",  "000",  "002",
                    "002",  "002",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002"]
    enemies82 = [1, 1, 2, 1, 0]
    down_room83 = [7, 5, 83,
                    "002",  "002",  "002",  "002",  "002",
                    "002","00033",  "005","00033",  "084",
                    "002",  "000",  "000",  "000",  "002",
                    "002",  "000",  "002",  "000",  "002",
                    "002",  "000",  "000",  "002",  "002",
                    "002",  "000",  "000",  "000",  "080",
                    "002",  "002",  "002",  "002",  "002"]
    enemies83 = [1, 2, 2, 0, 0]
    right1_room84 = [7, 5, 84,
                    "002",  "002",  "002",  "002",  "002",
                    "083",  "000",  "002",  "005",  "002",
                    "002",  "000",  "000","00033",  "002",
                    "002",  "000",  "002",  "000",  "002",
                    "002",  "002",  "002",  "000",  "002",
                    "080",  "000",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002"]
    enemies84 = [1, 2, 1, 0]
    right2_room85 = [3, 5, 85,
                    "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "005",  "002",
                    "002",  "002",  "080",  "002",  "002"]
    enemies85 = [0]
    level_dict.update({80: start_room80})
    level_dict.update({81: up_room81})
    level_dict.update({82: left_room82})
    level_dict.update({83: down_room83})
    level_dict.update({84: right1_room84})
    level_dict.update({85: right2_room85})
    level_dict.update({"80e": enemies80})
    level_dict.update({"81e": enemies81})
    level_dict.update({"82e": enemies82})
    level_dict.update({"83e": enemies83})
    level_dict.update({"84e": enemies84})
    level_dict.update({"85e": enemies85})
    level_dict.update({"inv": inventory})
    return level_dict

def Level_3():
    # the start position of a level
    # "x00x" = empty, "1xxx" = player, "x02x" = wall, "xxx3" = enemy, "x04x" = door, "x05x" = key, "x06x" = goal, "x80"-"x99" = room_switch
    level_dict = {}
    
    level_dict.update({"lvl": "lvl3"})
    inventory = [0, 0]
    start_room80 = [5, 5, 80, # room size
                    "000",  "000",  "081",  "000",  "000",
                    "000",  "000",  "000",  "000",  "000",
                    "083",  "000",  "100",  "000",  "082",
                    "000",  "000",  "000",  "000",  "000",
                    "000",  "000",  "084",  "000",  "000"]
    enemies80 = [0]
    up_room81 = [5, 5, 81,
                    "000",  "000",  "080",  "000",  "000",
                    "000",  "000",  "000",  "000",  "000",
                    "085",  "000",  "000",  "000",  "084",
                    "000",  "000",  "000",  "000",  "000",
                    "000",  "000",  "083","00032",  "000"]
    enemies81 = [1, 2, 1, 1]
    left_room82 = [5, 5, 82,
                    "000",  "000",  "083",  "000",  "000",
                    "000","00033",  "000",  "000",  "000",
                    "084",  "000",  "000",  "000",  "080",
                    "000",  "000",  "000",  "000",  "000",
                    "000",  "000",  "085",  "000",  "000"]
    enemies82 = [1, 2, 1, 0]
    down_room83 = [5, 5, 83,
                    "000",  "000",  "082",  "000",  "000",
                    "000",  "000",  "000",  "000",  "000",
                    "080",  "000",  "000",  "000",  "085",
                    "000",  "000","00031",  "000",  "000",
                    "000",  "000",  "081",  "000",  "000"]
    enemies83 = [1, 1, 1, 1]
    right1_room84 = [5, 5, 84,
                    "000",  "000",  "085",  "000",  "000",
                    "000","00031",  "000",  "000",  "000",
                    "082",  "000",  "000",  "000",  "081",
                    "000",  "000",  "000",  "000",  "000",
                    "000",  "000",  "080",  "000",  "000"]
    enemies84 = [1, 1, 1, 1]
    right2_room85 = [5, 5, 85,
                    "000",  "000",  "084",  "000",  "000",
                    "000",  "000",  "000",  "000",  "000",
                    "081",  "000",  "006",  "000",  "083",
                    "000",  "000",  "000",  "000",  "000",
                    "000",  "000",  "082",  "000",  "000"]
    enemies85 = [0]
    level_dict.update({80: start_room80})
    level_dict.update({81: up_room81})
    level_dict.update({82: left_room82})
    level_dict.update({83: down_room83})
    level_dict.update({84: right1_room84})
    level_dict.update({85: right2_room85})
    level_dict.update({"80e": enemies80})
    level_dict.update({"81e": enemies81})
    level_dict.update({"82e": enemies82})
    level_dict.update({"83e": enemies83})
    level_dict.update({"84e": enemies84})
    level_dict.update({"85e": enemies85})
    level_dict.update({"inv": inventory})
    return level_dict

def Level_4():
    # the start position of a level
    # "x00x" = empty, "1xxx" = player, "x02x" = wall, "xxx3" = enemy, "x04x" = door, "x05x" = key, "x06x" = goal, "x80"-"x99" = room_switch
    level_dict = {}
    
    level_dict.update({"lvl": "lvl4"})
    inventory = [0, 0]
    start_room80 = [5, 8, 80, # room size
                    "002",  "002",  "081",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "002",  "002",  "002",  "002",
                    "082",  "000",  "100",  "000",  "004",  "004",  "004",  "084",
                    "002",  "000",  "000",  "000",  "002",  "002",  "002",  "002",
                    "002",  "002",  "083",  "002",  "002",  "002",  "002",  "002"]
    enemies80 = [0]
    up_room81 = [9, 11, 81,
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "002",  "002",  "005",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "000","00031",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "000",  "002",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "000",  "000",  "002",  "002",
                    "002",  "000","00030",  "000",  "000",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "002",  "002",  "000",  "002",  "002",  "002",  "002",  "002",  "002",  "002",
                    "002",  "000",  "000",  "000",  "000",  "000",  "000",  "000",  "000",  "000",  "002",
                    "002",  "082",  "002",  "002",  "002",  "080",  "002",  "002",  "002",  "002",  "002"]
    enemies81 = [1, 1, 2, 1, 0]
    left_room82 = [5, 11, 82,
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "081",  "002",
                    "002","00031",  "000",  "000","00031",  "000",  "000","00031",  "000",  "000",  "002",
                    "002",  "005",  "002",  "000",  "002",  "000",  "002",  "000",  "002",  "000",  "080",
                    "002",  "000","00030",  "000",  "000","00030",  "000",  "000","00030",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002",  "002"]
    enemies82 = [1, 1, 6, 1, 1, 1, 0, 0, 0]
    down_room83 = [5, 6, 83,
                    "002",  "002",  "002",  "002",  "080",  "002",
                    "002",  "002",  "002",  "002",  "000",  "002",
                    "002","00031",  "000",  "000",  "000",  "002",
                    "002",  "002",  "005",  "002",  "002",  "002",
                    "002",  "002",  "002",  "002",  "002",  "002"]
    enemies83 = [1, 1, 1, 1]
    right1_room84 = [6, 5, 84,
                    "002",  "002",  "002",  "002",  "002",
                    "080",  "000",  "002",  "000",  "085",
                    "002",  "000",  "002",  "000",  "002",
                  "00030",  "000",  "000",  "000","00031",
                    "002",  "000",  "000",  "000",  "002",
                    "002",  "002",  "002",  "002",  "002"]
    enemies84 = [1, 1, 2, 0, 1]
    right2_room85 = [3, 4, 85,
                    "002",  "002",  "002",  "002",
                    "084",  "000",  "000",  "006",
                    "002",  "002",  "002",  "002"]
    enemies85 = [0]
    level_dict.update({80: start_room80})
    level_dict.update({81: up_room81})
    level_dict.update({82: left_room82})
    level_dict.update({83: down_room83})
    level_dict.update({84: right1_room84})
    level_dict.update({85: right2_room85})
    level_dict.update({"80e": enemies80})
    level_dict.update({"81e": enemies81})
    level_dict.update({"82e": enemies82})
    level_dict.update({"83e": enemies83})
    level_dict.update({"84e": enemies84})
    level_dict.update({"85e": enemies85})
    level_dict.update({"inv": inventory})
    return level_dict

main_menu = Main_menu()
Run_main_menu(main_menu)