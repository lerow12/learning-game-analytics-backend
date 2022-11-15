"""Unpacks game events into objects"""

from math import isqrt
import src.nyingi_event_structure as ne
import src.database_calls as dc
from json import loads as jsonLoad
from datetime import datetime


class SQLGameStart():
    def __init__(self):
        self.board_area = 0
        self.max_value = 0
        self.computer_difficulty = ""
        self.game_name = ""
        self.board_state = []
        self.winner = 0
        self.computer_hand = []
        self.player_hand = []

    def __str__(self) -> str:
        return f"{vars(self)}"


class SQLPlayerEvent():
    def __init__(self):
        self.player_num = 0
        self.player_id = -1
        self.is_swap = 0
        self.is_successful = 1
        self.timestamp = ""
        self.play_time = 0
        self.card_diff_id = 0
        self.board_diff_id = 0
        self.game_id = 0
        self.inputs = []


class SQLBoardDiff():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.val = 0
        self.taken_matrix = []
        self.player_num = 0


event_classes = {
    0: ne.MetadataStruct,
    2: ne.GameStartStruct,
    3: ne.CardDrawnStruct,
    4: ne.BoardInitStruct,
    5: ne.PlayerInputStruct,
    6: ne.PlayerSwapStruct,
    7: ne.PlayerMoveStruct,
    8: ne.GameOverStruct,
    9: ne.DeckRefreshStruct
}

event_types = {
    "game_start": 2,
    "card_draw": 3,
    "board_init": 4,
    "player_input": 5,
    "player_swap": 6,
    "player_move": 7,
    "game_over": 8,
    "deck_refresh": 9
}


def value_convert(value):
    if (value == "Prime"):
        return 'P'
    elif (value == "Wild"):
        return 'W'
    else:
        return value


def get_timestamp_difference(early, late):
    fmt = '%m/%d/%Y %I:%M:%S %p'
    earlystamp = datetime.strptime(early, fmt)
    latestamp = datetime.strptime(late, fmt)
    time_elapsed = latestamp-earlystamp
    time_elapsed = str(time_elapsed)
    if len(time_elapsed) == 7:
        time_elapsed = "0" + time_elapsed
    print(time_elapsed)
    return time_elapsed


def convert_to_SQL_timestamp(time):
    fmt = '%m/%d/%Y %I:%M:%S %p'
    raw_time = datetime.strptime(time, fmt)
    return raw_time


def generate_board_dif(play, last_board_state, board_size):
    diff = SQLBoardDiff()
    diff.x = play.square_id[0]
    diff.y = play.square_id[1]
    diff.player_num = play.player_num
    diff.taken_matrix = last_board_state.copy()
    offset = diff.y*isqrt(board_size)+diff.x
    diff.taken_matrix[offset] = 1
    return diff


def unpack_nyingi_events(events):
    global event_classes
    objects = []
    for event in events:
        class_type = event_classes[event.event_id]
        objects.append((event.event_id, event.timestamp,
                       class_type(**jsonLoad(event.json_string))))
    rebuild_game(objects)


def rebuild_game(objects):
    game_start_events = []
    player_events = []
    for event in objects:
        event_type = event[0]
        if (event_type in [0, 2, 8, 3, 4]):
            game_start_events.append(event)
        if (event_type in [7, 3, 5, 2, 6]):
            player_events.append(event)
    game_structures = extract_games(game_start_events)
    game_ids = []
    for game in game_structures:
        game_ids.append(dc.save_game_table(game.board_area, game.max_value, game.computer_difficulty,
                        game.game_name, game.board_state, game.winner, game.computer_hand, game.player_hand))
    player_events = extract_player_events(player_events, game_ids)
    for player_event in player_events:
        dc.save_player_events(player_event.player_num, player_event.player_id, player_event.is_swap, player_event.is_successful,
                              player_event.timestamp, player_event.play_time, player_event.inputs, player_event.card_diff_id, player_event.board_diff_id, player_event.game_id)


def extract_games(event_queue):
    games = []
    # Fun fact: Lists evaluate to true in python while they are not empty!
    # This may be the worst piece of code I've ever written.
    current_game = SQLGameStart()
    in_game = False
    while (event_queue):
        cur_event = event_queue.pop(0)
        event_type = cur_event[0]
        event_object = cur_event[2]
        if (event_type == 0):
            if (in_game):
                games.append(current_game)
                current_game = SQLGameStart()
                current_game.game_name = event_object.game_name
            else:
                current_game.game_name = event_object.game_name
                in_game = True
        if (event_type == 2):
            current_game.computer_difficulty = event_object.difficulty
            current_game.board_area = event_object.board_size[0] * \
                event_object.board_size[1]
            current_game.max_value = event_object.number_range[0] * \
                event_object.number_range[1]
            for x in range(7):
                player_draw_event = event_queue.pop(0)
                if (player_draw_event[0] == 3):
                    card_value = value_convert(player_draw_event[2].card_value)
                    current_game.player_hand.append(card_value)
                else:
                    # If we don't even draw all the cards
                    # the data can't possibly be that useful.
                    current_game = SQLGameStart()
                computer_draw_event = event_queue.pop(0)
                if (computer_draw_event[0] == 3):
                    card_value = value_convert(player_draw_event[2].card_value)
                    current_game.computer_hand.append(card_value)
                else:
                    current_game = SQLGameStart()
        if (event_type == 4):
            current_game.board_state = event_object.board_tiles
        if (event_type == 8):
            in_game = False
            current_game.winner = event_object.winner_num
            games.append(current_game)
            current_game = SQLGameStart()
    if (in_game):
        games.append(current_game)
    return games


def extract_player_events(event_queue, game_ids):
    # Here there be dragons
    player_events = []
    active_event = SQLPlayerEvent()
    last_timestamp = ""
    player_hand = []
    computer_hand = []
    current_board_state = []
    game_id = 0
    board_size = 0
    requeue = []
    while (event_queue):
        cur_event = event_queue.pop(0)
        event_type = cur_event[0]
        event_object = cur_event[2]
        event_TS = cur_event[1]
        if (event_type == 2):
            last_timestamp = event_TS
            board_size = event_object.board_size[0] * \
                event_object.board_size[1]
            current_board_state = [0]*board_size
            game_id = game_ids.pop(0)
            player_hand = []
            computer_hand = []
            for x in range(7):
                player_draw_event = event_queue.pop(0)
                if (player_draw_event[0] == 3):
                    card_value = value_convert(player_draw_event[2].card_value)
                    player_hand.append(card_value)
                computer_draw_event = event_queue.pop(0)
                if (computer_draw_event[0] == 3):
                    card_value = value_convert(computer_draw_event[2].card_value)
                    computer_hand.append(card_value)
        elif ((event_type == 3 and event_object.description.__contains__('2')) or event_type == 5):
            requeue.append(cur_event)
        elif (event_type == 7):
            active_event.game_id = game_id
            active_event.is_swap = 0
            active_event.timestamp = convert_to_SQL_timestamp(event_TS)
            active_event.play_time = get_timestamp_difference(
                last_timestamp, event_TS)
            active_event.player_num = event_object.player_num
            last_timestamp = event_TS
            if (event_object.is_successful):
                active_event.is_successful = 1
                diff = generate_board_dif(
                    event_object, current_board_state, board_size)
                current_board_state = diff.taken_matrix
                board_diff_id = dc.save_board_diff(
                    diff.x, diff.y, diff.taken_matrix, diff.player_num)
                active_event.board_diff_id = board_diff_id
                if (event_object.player_num == 1):
                    hand = player_hand
                else:
                    hand = computer_hand
                    for event in requeue:
                        event_queue.insert(0, event)
                    requeue = []
                cards_drawn = []
                cards_played = []
                previous_hand = hand.copy()
                for card in event_object.cards_played:
                    card_event = event_queue.pop(0)
                    value = value_convert(card_event[2].card_value)
                    played = value_convert(card)
                    cards_drawn.append(value)
                    cards_played.append(played)
                    hand.append(value)
                    hand.remove(played)
                card_diff_id = dc.save_card_diff(previous_hand, cards_played, cards_drawn, event_object.player_num)
                active_event.card_diff_id = card_diff_id
            else:
                if (event_object.player_num == 1):
                    hand = player_hand
                else:
                    hand = computer_hand
                cards_drawn = []
                cards_played = []
                for card in event_object.cards_played:
                    cards_played.append(value_convert(card))
                card_diff_id = dc.save_card_diff(hand, cards_played, [], event_object.player_num)
                active_event.card_diff_id = card_diff_id
            inputs = []
            for event in requeue:
                inputs.append(event[2].value)
            active_event.inputs = inputs
            requeue = []
            player_events.append(active_event)
            active_event = SQLPlayerEvent()
        elif (event_type == 6):
            if (event_object.player_num == 1):
                hand = player_hand
            else:
                hand = computer_hand
            active_event.game_id = game_id
            active_event.is_swap = 1
            active_event.timestamp = convert_to_SQL_timestamp(event_TS)
            active_event.play_time = get_timestamp_difference(
                last_timestamp, event_TS)
            active_event.player_num = event_object.player_num
            last_timestamp = event_TS
            active_event.is_successful = 1
            cards_drawn = []
            cards_swapped = []
            previous_hand = hand.copy()
            for card in event_object.swapped_cards:
                card_event = event_queue.pop(0)
                value = value_convert(card_event[2].card_value)
                swapped = value_convert(card)
                cards_drawn.append(value)
                cards_swapped.append(swapped)
                hand.append(value)
                hand.remove(swapped)
            card_diff_id = dc.save_card_diff(previous_hand, cards_swapped, cards_drawn, event_object.player_num)
            active_event.card_diff_id = card_diff_id
            player_events.append(active_event)
            active_event = SQLPlayerEvent()
    return player_events
