"""Pulls a game from the database corresponsing to the game_id passed."""
import mysql.connector

database_name = "testing"

host = "localhost"
user = "root"
password = "firegrate"

event_dict_fields = [
    "player_num", "player_id", "is_swap", "is_successful",
    "timestamp", "play_time", "inputs", "hand", "cards_used",
    "cards_gained", "x", "y", "val", "taken_matrix"
]

game_table_dict_fields = [
    "board_area", "max_value", "computer_difficulty",
    "game_name", "board_state", "winner", "computer_hand",
    "player_hand"
]

PLAYER_COLUMNS = """PlayerEvents.player_num, PlayerEvents.player_id,
                    PlayerEvents.is_swap, PlayerEvents.is_successful,
                    PlayerEvents.timestamp, PlayerEvents.play_time,
                    PlayerEvents.inputs"""

CARDDIFF_COLUMNS = """CardDiff.hand, CardDiff.cards_used,
                      CardDiff.cards_gained"""

BOARDDIFF_COLUMNS = """BoardDiff.x, BoardDiff.y, BoardDiff.val,
                       BoardDiff.taken_matrix"""

# returns a dictionary corresponding to an SQL table row
def get_query_dict(query_tuple, dict_fields):
    result = {}
    for index, column in enumerate(query_tuple):
        result[dict_fields[index]] = column
    return result

def pull_game(game_id):
    game_dict = {
        "game_table": None,
        "events": []
    }

    con = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )

    event_cursor = con.cursor()
    event_cursor.execute(
        f"""SELECT {PLAYER_COLUMNS}, {CARDDIFF_COLUMNS}, {BOARDDIFF_COLUMNS}
        FROM PlayerEvents
        JOIN CardDiff  on PlayerEvents.card_diff_id=CardDiff.card_diff_id
        JOIN BoardDiff on PlayerEvents.board_diff_id=BoardDiff.board_diff_id
        WHERE PlayerEvents.game_id={game_id};
    """)
    # adding every game event dictionary to the events array
    for row in event_cursor:
        game_dict["events"].append(get_query_dict(row, event_dict_fields))

    game_table_cursor = con.cursor()
    game_table_cursor.execute(f"SELECT * FROM GameTable WHERE game_id={game_id}")

    game_table = game_table_cursor.fetchone()
    # slicing game_table to skip past game_id
    game_dict["game_table"] = get_query_dict(game_table[1:], game_table_dict_fields)

    con.commit()
    con.close()

    return game_dict
