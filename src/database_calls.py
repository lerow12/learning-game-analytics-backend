import mysql.connector

database_name = "NyingiDatabase"
host = "localhost"
user = "test"
password = "password"


#  Converts a list of ints into a hexadecimal string representation
def list_to_varbinary(arr):
    varbinary = ["0x"]
    for num in arr:
        varbinary.append(hex(num)[2:].rjust(3,"0"))
    string = ''.join(varbinary)
    return string


def delimit(list):
    charlist = ""
    for x in list:
        charlist += str(x)
        charlist += " "
    charlist = charlist[:-1]
    return charlist


def save_game_table(board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor(prepared=True)
    board_state = delimit(board_state)
    computer_hand = delimit(computer_hand)
    player_hand = delimit(player_hand)
    args_tuple = (board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand)
    cur.execute(f"""
        INSERT INTO GameTable(board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
    """, args_tuple)
    con.commit()
    game_id = cur.lastrowid
    con.close()
    return game_id


def save_board_diff(x, y, taken_matrix, player_num):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor(prepared=True)
    taken_matrix = list_to_varbinary(taken_matrix)
    args_tuple = (x, y, taken_matrix, player_num)
    cur.execute("""
        INSERT INTO BoardDiff(x, y, taken_matrix, player_num)
        VALUES(%s, %s, %s, %s);
    """, args_tuple)
    con.commit()
    diff_id = cur.lastrowid
    con.close()
    return diff_id


def save_card_diff(hand, cards_used, cards_gained, player_num):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor(prepared=True)
    hand = delimit(hand)
    cards_used = delimit(cards_used)
    cards_gained = delimit(cards_gained)
    arg_tuple = (hand, cards_used, cards_gained, player_num)
    cur.execute("""
        INSERT INTO CardDiff(hand, cards_used, cards_gained, player_num)
        VALUES(%s, %s, %s, %s);
    """, arg_tuple)
    con.commit()
    diff_id = cur.lastrowid
    con.close()
    return diff_id


def save_player_events(player_num, player_id, is_swap, is_successful, timestamp, play_time, inputs, card_diff_id, board_diff_id, game_id):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor(prepared=True)
    if (card_diff_id == 0):
        card_diff_id = None
    if (board_diff_id == 0):
        board_diff_id = None
    if (inputs == []):
        inputs = None
    else:
        inputs = delimit(inputs)
    arg_tuple = (player_num, player_id, is_swap, is_successful, timestamp, play_time, inputs, card_diff_id, board_diff_id, game_id)
    cur.execute("""
        INSERT INTO PlayerEvents(player_num, player_id, is_swap, is_successful, timestamp, play_time, inputs, card_diff_id, board_diff_id, game_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, arg_tuple)  
    con.commit()
    con.close()
