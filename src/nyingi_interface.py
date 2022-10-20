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
    board = []
    hand = []

    for event_id, timestamp, object in objects:
        if event_id == event_types["game_start"]:
            pass
        elif event_id == event_types["card_draw"]:
            print(object.card_value)
        elif event_id == event_types["board_init"]:
            pass
        elif event_id == event_types["player_input"]:
            pass
        elif event_id == event_types["player_swap"]:
            pass
        elif event_id == event_types["player_move"]:
            pass
        elif event_id == event_types["game_over"]:
            pass
        elif event_id == event_types["deck_refresh"]:
            pass
        else:
            pass

