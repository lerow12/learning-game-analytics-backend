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

def save_game_table(board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor()
    board_state = list_to_varbinary(board_state)
    computer_hand = ''.join(computer_hand)
    player_hand = ''.join(player_hand)
    cur.execute(f"""
        INSERT INTO GameTable(board_area, max_value, computer_difficulty, game_name, board_state, winner, computer_hand, player_hand)
        VALUES({board_area}, {max_value}, '{computer_difficulty}', '{game_name}', '{board_state}', {winner}, '{computer_hand}', '{player_hand}');
    """)
    con.commit()
    con.close()

def save_board_diff(x, y, val, taken_matrix, player_num):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor()
    taken_matrix = list_to_varbinary(taken_matrix)
    cur.execute(f"""
        INSERT INTO BoardDiff(x, y, val, taken_matrix, player_num)
        VALUES({x}, {y}, {val}, '{taken_matrix}', {player_num});
    """)
    con.commit()
    con.close()

def save_card_diff(hand, cards_used, cards_gained, player_num):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor()
    hand = ''.join(hand)
    cards_used = ''.join(cards_used)
    cards_gained = ''.join(cards_gained)
    cur.execute(f"""
        INSERT INTO CardDiff(hand, cards_used, cards_gained, player_num)
        VALUES('{hand}', '{cards_used}', '{cards_gained}', {player_num});
    """)
    con.commit()
    con.close()

def save_player_events(player_num, player_id, is_swap, is_successful, timestamp, play_time, card_diff_id, board_diff_id, game_id):
    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    cur = con.cursor()
    cur.execute(f"""
        INSERT INTO PlayerEvents(player_num, player_id, is_swap, is_successful, timestamp, play_time, card_diff_id, board_diff_id, game_id)
        VALUES({player_num}, {player_id}, {is_swap}, {is_successful}, '{timestamp}', '{play_time}', {card_diff_id}, {board_diff_id}, {game_id});
    """)
    con.commit()
    con.close()
