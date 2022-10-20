"""Unpacks game events into objects"""

import src.nyingi_event_structure as ne
import src.database_calls as dc
from json import loads as jsonLoad

event_classes = {
    2: ne.GameStartStruct,
    3: ne.CardDrawnStruct,
    4: ne.BoardInitStruct,
    5: ne.PlyaerInputStruct,
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


def unpack_nyingi_events(events):
    global event_classes
    objects = []
    for event in events:
        class_type = event_classes[event.event_id]
        objects.append((event.event_id, event.timestamp, class_type(**jsonLoad(event.json_string))))
    rebuild_game(objects)


def rebuild_game(objects):
    global event_types
    game_start_db = []
    board = []
    player_hand = []
    computer_hand = []

    for event_id, timestamp, object in objects:
        if event_id == event_types["game_start"]:
            game_start_db.append(object.board_size[0] * object.board_size[1])
            game_start_db.append(object.number_range[0] * object.number_range[1])
            game_start_db.append(object.difficulty)
            game_start_db.append("Nyingi")
        elif event_id == event_types["card_draw"]:
            if "1" in object.description:
                player_hand.append(object.card_value)
            else:
                computer_hand.append(object.card_value)
        elif event_id == event_types["board_init"]:
            game_start_db.append(object.board_tiles)
        elif event_id == event_types["player_input"]:
            pass
        elif event_id == event_types["player_swap"]:
            if object.player_num == 1:
                for card in object.swapped_cards:
                    player_hand.remove(card)
            else:
                for card in object.swapped_cards:
                    computer_hand.remove(card)
        elif event_id == event_types["player_move"]:
            pass
        elif event_id == event_types["game_over"]:
            pass
        elif event_id == event_types["deck_refresh"]:
            pass
        else:
            pass

