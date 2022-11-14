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
    cur = con.cursor()
    board_state = delimit(board_state)
    computer_hand = delimit(computer_hand)
    player_hand = delimit(player_hand)
    cur.execute(f"""
        INSERT INTO GameTable(board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand)
        VALUES({board_area}, {max_value}, '{computer_difficulty}', '{game_name}', '{board_state}', {winner}, '{computer_hand}', '{player_hand}');
    """)
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
    cur = con.cursor()
    taken_matrix = list_to_varbinary(taken_matrix)
    cur.execute(f"""
        INSERT INTO BoardDiff(x, y, taken_matrix, player_num)
        VALUES({x}, {y}, '{taken_matrix}', {player_num});
    """)
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
    cur = con.cursor()
    hand = delimit(hand)
    cards_used = delimit(cards_used)
    cards_gained = delimit(cards_gained)
    cur.execute(f"""
        INSERT INTO CardDiff(hand, cards_used, cards_gained, player_num)
        VALUES('{hand}', '{cards_used}', '{cards_gained}', {player_num});
    """)
    con.commit()
    diff_id = cur.lastrowid
    con.close()
    return diff_id


def save_player_events(player_num, player_id, is_swap, is_successful, timestamp, play_time, card_diff_id, board_diff_id, game_id):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor()
    if (card_diff_id == 0):
        card_diff_id = "NULL"
    if (board_diff_id == 0):
        board_diff_id = "NULL"
    cur.execute(f"""
        INSERT INTO PlayerEvents(player_num, player_id, is_swap, is_successful, timestamp, play_time, card_diff_id, board_diff_id, game_id)
        VALUES({player_num}, {player_id}, {is_swap}, {is_successful}, '{timestamp}', '{play_time}', {card_diff_id}, {board_diff_id}, {game_id});
    """)
    con.commit()
    con.close()
